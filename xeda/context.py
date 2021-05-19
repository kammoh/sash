from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from collections import namedtuple
from typing import Dict, List, NamedTuple, Type
from .flows.flow import DesignSource, Flow


class RtlSettings(NamedTuple):
    sources: List[DesignSource]
    top: str
    generics: Dict[str, int]

class TbSettings(NamedTuple):
    sources: List[DesignSource]
    top: str
    generics: Dict[str, int]
    uut: str

class DesignSettings(NamedTuple):
    rtl: RtlSettings
    tb : TbSettings

class FlowDirs(NamedTuple):
    pass

class FlowContext:
    design_settings: DesignSettings
    flow_settings: SimpleNamespace
    
    def __init__(self, flow_class: Type[Flow], flow_run_dir: Path) -> None:
        assert flow_class.name

        self.dirs = SimpleNamespace()
        self.dirs.results = flow_run_dir / 'Results' / flow_class.name

    def init_dirs(self):
        for name, d in self.dirs.__dict__.items():
            if d:
                d.mkdir(exist_ok=True, parents=True)
        


class RunnerContext:
    run_dir: Path
    def __init__(self, run_dir, design_settings, flow_settings) -> None:
        self.timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S%f")[:-3]
        if design_settings and not isinstance(design_settings, list):
            design_settings = [design_settings]

        self.design_settings = design_settings
        self.flow_settings = flow_settings
        self.xeda_run_dir = Path(run_dir).resolve()
        self.xeda_run_dir.mkdir(exist_ok=True, parents=True)

    def newFlowView(self, flow_cls: Type[Flow]) -> FlowContext:
        pass
