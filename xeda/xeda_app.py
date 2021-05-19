# © 2020 [Kamyar Mohajerani](mailto:kamyar@ieee.org)

from pkg_resources import get_distribution, DistributionNotFound
from datetime import datetime
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Mapping
import coloredlogs
import logging

logger = logging.getLogger()


try:
    __version__ = get_distribution(__package__).version
except DistributionNotFound:
    __version__ = '(N/A - Local package)'


def run_xeda(xeda_project, args):
    if isinstance(args, Mapping):
        args = SimpleNamespace(**args)

    runner_cls = args.flow_runner

    if args.xeda_run_dir is None:
        rundir = None
        project = xeda_project.get('project')
        if isinstance(project, list):
            project = project[0]
        if project:
            rundir = project.get('xeda_run_dir')
        if not rundir:
            rundir = os.environ.get('xeda_run_dir')
        if not rundir:
            rundir = 'xeda_run'
        args.xeda_run_dir = rundir

    xeda_run_dir = Path(args.xeda_run_dir).resolve()
    xeda_run_dir.mkdir(exist_ok=True, parents=True)

    logdir = xeda_run_dir / 'Logs'
    logdir.mkdir(exist_ok=True, parents=True)

    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S%f")[:-3]

    logfile = logdir / f"xeda_{timestamp}.log"
    print(f"Logging to {logfile}")

    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    coloredlogs.install(
        'INFO', fmt='%(asctime)s %(levelname)s %(message)s', logger=logger)

    logger.info(f"Running using FlowRunner: {runner_cls.__name__}")

    runner = runner_cls(args, xeda_project, timestamp)

    runner.launch()
