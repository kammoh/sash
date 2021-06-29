
# Xeda ISE Synthtesis flow
# ©2021 Kamyar Mohajerani and contributors

from collections import abc
import logging
from typing import Any, Dict, Optional, List, Sequence

from pydantic.main import BaseModel
from pydantic.types import NoneStr
from ..flow import FPGA, SynthFlow

logger = logging.getLogger()


class IseSynth(SynthFlow):

    class Settings(SynthFlow.Settings):
        clock_period: NoneStr = None
        
    def run(self):
        script_path = self.copy_from_template(f'ise_synth.tcl')

        self.run_process('xtclsh', [script_path], initial_step='Starting vivado',
                         stdout_logfile='xeda_ise_stdout.log')
