from . import cli

__all_ = [cli]
__project__ = 'xeda'
__author__ = 'Kamyar Mohajerani'
__package__ = 'xeda'

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
