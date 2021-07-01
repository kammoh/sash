from .flow import Flow, Design, registered_flows
from ..utils import dict_merge, snakecase_to_camelcase, dump_json, try_convert
from pathvalidate import sanitize_filename
import logging
import time
from datetime import datetime
from typing import Mapping, Type, Dict, List, Any
import importlib
import hashlib
from pathlib import Path
import re

from .._version import get_versions
__version__ = get_versions()['version']
del get_versions


logger = logging.getLogger()


class FlowGen:
    @staticmethod
    def merge_overrides(overrides, settings):
        if overrides:
            if isinstance(overrides, str):
                overrides = re.split(r'\s*,\s*', overrides)
            for override in overrides:
                key, val = override.split('=')
                hier = key.split('.')
                patch_dict = dict()
                tmp = patch_dict
                for field in hier[:-1]:
                    tmp[field] = dict()
                    tmp = tmp[field]
                tmp[hier[-1]] = try_convert(val, convert_lists=True)
                settings = dict_merge(settings, patch_dict, True)
        return settings

    # TODO more specific than Any?
    def __init__(self, all_flows_settings: Dict[str, Dict]):
        self.all_flows_settings: Dict[str, Dict] = all_flows_settings

    @staticmethod
    def semantic_hash(data: Any) -> str:
        def get_digest(b: bytes):
            return hashlib.sha1(b).hexdigest()[:16]

        # data: JsonType, not adding type as Pylance does not seem to like recursive types :/
        def sorted_dict_str(data):
            if isinstance(data, Mapping):
                return {k: sorted_dict_str(data[k]) for k in sorted(data.keys())}
            elif isinstance(data, list):
                return [sorted_dict_str(val) for val in data]
            elif hasattr(data, '__dict__'):
                return sorted_dict_str(data.__dict__)
            else:
                return str(data)

        return get_digest(bytes(repr(sorted_dict_str(data)), 'UTF-8'))

    @staticmethod
    def get_flow_class(flow_name: str, module_name: str, package: str) -> Type[Flow]:
        (mod, flow_class) = registered_flows.get(flow_name, (None, None))
        if flow_class is None:
            logger.warn(
                f"Flow {flow_name} was not found in registered flows. Trying to load using importlib.import_module")
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError as e:
                logger.critical(
                    f"Unable to import {module_name} from {package}")
                raise e from None
            assert module is not None, f"importlib.import_module returned None. module_name: {module_name}, package: {package}"
            flow_class_name = snakecase_to_camelcase(flow_name)
            try:
                flow_class = getattr(module, flow_class_name)
            except AttributeError as e:
                logger.critical(
                    f"Unable to find class {flow_class_name} in {module}")
                raise e from None
        assert flow_class is not None and issubclass(flow_class, Flow)
        return flow_class

    def get_settings_schema(self, flow_name: str, module_name: str, package: str = __package__):
        flow_class = self.get_flow_class(flow_name, module_name, package)
        return flow_class.Settings.schema(by_alias=False)

    def generate(self, flow_name: str, module_name: str, design: Design, xeda_run_dir: Path, completed_dependencies: List[Flow], override_settings: Mapping[str, Any], verbose: bool = False, package: str = __package__) -> Flow:
        flow_class = self.get_flow_class(flow_name, module_name, package)

        flow_settings_dict = self.all_flows_settings.get(flow_name, {})
        if override_settings:
            flow_settings_dict = self.merge_overrides(
                override_settings, flow_settings_dict)
        flow_settings = flow_class.Settings(**flow_settings_dict)
        if verbose:
            flow_settings.verbose = True  # force verbose
        all_settings = dict(
            flow_name=flow_name, flow_settings=flow_settings,
            design=design, xeda_version=__version__
        )
        xeda_hash = self.semantic_hash(all_settings)

        results_dir = xeda_run_dir / 'Results' / flow_name
        results_dir.mkdir(exist_ok=True, parents=True)
        run_path = xeda_run_dir / \
            sanitize_filename(f"{design.name}_{flow_name}_{xeda_hash}")
        run_path.mkdir(exist_ok=True)

        settings_json_path = run_path / f'settings.json'
        logger.info(f'dumping effective settings to {settings_json_path}')
        dump_json(all_settings, settings_json_path)

        reports_dir = run_path / flow_settings.reports_subdir_name
        reports_dir.mkdir(exist_ok=True)

        flow = flow_class(flow_settings, design, run_path,
                          completed_dependencies)

        flow.timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        flow.init_time = time.monotonic()

        return flow
