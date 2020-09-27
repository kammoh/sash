import json
import logging
import argparse
from xeda.plugins import IRunner
class DummyPlugin(IRunner):
    """Example plugin which prints the settings.json for the run

    """
    command = "dumdum"
    def __init__(self):
        self.logger = logging.getLogger()
    
    def register_subparser(self, subparsers):
        """Register the dumdum command

        Args:
            subparsers (ArgumentParser): Add your command and related arguments to its operation
        """
        dummy_parser = subparsers.add_parser(self.command, help='Do something dumb')
        dummy_parser.add_argument(
            '--reverse',
            action='store_true',
            help='Print Dummy string in reverse'
        )
    def launch(self, args):
        if args.reverse:
            self.logger.info("Running Dummy Plugin"[::-1])
        else:
            self.logger.info("Running Dummy Plugin")
