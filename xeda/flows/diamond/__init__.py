# © 2020 [Kamyar Mohajerani](mailto:kamyar@ieee.org)

from ..flow import Flow, SynthFlow


class Diamond(Flow):
    reports_subdir_name = 'diamond_impl'


class DiamondSynth(Diamond, SynthFlow):
    default_settings = {**SynthFlow.default_settings,
                        'impl_folder': 'diamond_impl',
                        'impl_name': 'Implementation0',
                        'syn_cmdline_args': None}

    def run(self):
        constraint_exts = ['ldc'] if self.settings.flow["synthesis_engine"] == "lse" else ['sdc', 'fdc']
        constraints = [f'constraints.{ext}' for ext in constraint_exts]
        for constraint in constraints:
            self.copy_from_template(constraint)
        script_path = self.copy_from_template(f'synth.tcl')
        self.run_process('diamondc', [str(script_path)])

    def parse_reports(self):
        self.results = dict()
        reports_dir = self.flow_run_dir / 'diamond_impl'
        design_name = self.settings.design['name']
        impl_name = self.settings.flow['impl_name']

        period_pat = r'''^\s*Preference:\s+PERIOD\s+PORT\s+\"(?P<clock_port>\w+)\"\s+(?P<clock_period>\d+\.\d+)\s+ns.*HIGH\s+\d+\.\d+\s+ns\s*;\s*
\s*\d+\s+items\s+\S+\s+(?P<_timing_errors>\d+)\s+timing\s+errors?'''
        freq_pat = r'^\s*Preference:\s+FREQUENCY\s+PORT\s+\"(?P<clock_port>\w+)\"\s+(?P<clock_frequency>\d+\.\d+)\s+MHz\s*;\s*\n\s*\d+\s+items\s+\S+\s+(?P<_timing_errors>\d+)\s+timing\s+errors?'
        self.parse_report(reports_dir / f'{design_name}_{impl_name}.twr', [period_pat, freq_pat])

        print(self.results)
        if 'clock_frequency' in self.results:
            frequency = self.results['clock_frequency']
            period = 1000.0/frequency
            self.results['clock_period'] = period

        else:
            period = self.results['clock_period']
            frequency = 1000.0/period
            self.results['clock_frequency'] = frequency

        slice_pat = r'^Device\s+utilization\s+summary:\s*.*^\s+SLICE\s+(?P<slice>\d+)\/(?P<_slice_avail>\d+).*^Number\s+of\s+Signals'
        time_pat = r'''Level\s*/\s+Number\s+Worst\s+Timing\s+Worst\s+Timing\s+Run\s+NCD\s*
\s*Cost\s+\[ncd\]\s+Unrouted\s+Slack\s+Score\s+Slack\(hold\)\s+Score\(hold\)\s+Time\s+Status\s*
(\s*\-+){8}\s*
\s*(?P<_lvl_cost>\S+)\s+(?P<_ncd>\S+)\s+(?P<_num_unrouted>\d+)\s+(?P<wns>\-?\d+\.\d+)\s+(?P<_setup_score>\d+)\s+(?P<whs>\-?\d+\.\d+)\s+(?P<_hold_score>\d+)\s+(?P<_runtime>\d+(?:\:\d+)*)\s+(?P<_status>\w+)\s*$'''
        self.parse_report(reports_dir / f'{design_name}_{impl_name}.par', slice_pat, time_pat)

        # NOTE there can be "page breaks" anywhere in the mrp file (others? TODO)
        # NOTE therefore only match lines
        #   1. Total number of LUT4s = (Number of logic LUT4s) + 2*(Number of distributed RAMs) + 2*(Number of ripple logic)
        #   2. Number of logic LUT4s does not include count of distributed RAM and ripple logic.
        slice_pattern = r'''\s*Number\s+of\s+registers:\s*(?P<ff>\d+)\s+out\s+of\s*(?P<_ff_avail>\d+).*
\s*Number\s+of\s+SLICEs:\s*(?P<_slice_map>\d+)\s*out\s+of\s*(?P<_slice_avail>\d+).*
\s+SLICEs\s+as\s+RAM:\s*(?P<_slice_ram>\d+)\s*out\s+of\s*(?P<_slice_ram_avail>\d+).*
\s+SLICEs\s+as\s+Carry:\s*(?P<_slice_carry>\d+)\s+out\s+of\s+(?P<_slice_carry_avail>\d+).*
\s*Number\s+of\s+LUT4s:\s*(?P<lut>\d+)\s+out of\s+(?P<_lut_avail>\d+).*
\s+Number\s+used\s+as\s+logic\s+LUTs:\s*(?P<_lut_logic>\d+)\s*
\s+Number\s+used\s+as\s+distributed\s+RAM:\s*(?P<_lut_dram>\d+)\s*
\s+Number\s+used\s+as\s+ripple\s+logic:\s*(?P<_lut_ripple>\d+)\s*
\s+Number\s+used\s+as\s+shift\s+registers:\s*(?P<_lut_shift>\d+)\s*.*
\s*Number\s+of\s+block\s+RAMs:\s*(?P<bram>\d+)\s+out\s+of\s+(?P<_bram_avail>\d+).*'''

        dsp_pattern = r'''\s+MULT18X18D\s+(?P<_dsp_MULT18X18D>\d+)\s*.*
\s+MULT9X9D\s+(?P<_dsp_MULT9X9D>\d+)\s*.*'''

        self.parse_report(reports_dir / f'{design_name}_{impl_name}.mrp', slice_pattern, dsp_pattern)

        # FIXME add other types of available ALUs and DSPs
        self.results['dsp'] = self.results['_dsp_MULT18X18D'] + self.results['_dsp_MULT9X9D']

        failed = False

        # TODO FIXME move to LwcSynth
        forbidden_resources = ['dsp', 'bram']
        for res in forbidden_resources:
            if (res in self.results and self.results[res] != 0):
                self.logger.critical(f'Map report shows {self.results[res]} use(s) of forbidden resource {res}.')
                failed = True

        failed = failed or (self.results['wns'] < 0) or (self.results['whs'] < 0) or (
            self.results['_num_unrouted'] != 0) or (self.results['_status'].lower() != 'completed') or (
                self.results['_timing_errors'] != 0)

        self.results['success'] = not failed
