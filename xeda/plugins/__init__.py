from typing import Set
#from ..flows.settings import Settings
from typing import List

from pathlib import Path
from importlib import util
import os
import traceback
from inspect import isabstract
from abc import ABC, abstractmethod
class PluginBase(ABC):
    """Base class for creating Plugins.
    """
    registry = []
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not isabstract(cls): #Exclude interfaces from registry
            cls.registry.append(cls())
    @staticmethod
    def init():
        """Load all plugins in the {xeda_base}/plugins dir
        """
        PluginBase.loadPlugins(os.path.dirname(os.path.abspath(__file__)))
    @staticmethod
    def loadPlugins(plugindir):
        """Load plugins from a given directory

        Args:
            plugindir (Path): Directory to load plugins from
        """
        def load_module(path):
            print(path)
            name = os.path.split(path)[-1]
            print(name)
            spec = util.spec_from_file_location(name, path)
            print()
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        for fname in os.listdir(plugindir):
            #print(fname)
            if not fname.startswith('.') and \
                not fname.startswith('__') and fname.endswith('.py'):
                print(fname)
                try:
                    load_module(os.path.join(plugindir, fname))
                except Exception:
                    traceback.print_exc()

class IPostRun(PluginBase):
    """PostRun interface
    """
    @abstractmethod
    def post_run(self):
        """This method is called after a flow run
        """
        raise NotImplementedError


class IRunner(PluginBase):
    @property
    def command(self):
        raise NotImplementedError


    @abstractmethod
    def register_subparser(self, subparsers):
        raise NotImplementedError
    @abstractmethod
    def launch(self):
        raise NotImplementedError