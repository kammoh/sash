from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import sys
import versioneer
import atexit
from pathlib import Path
from distutils.cmd import Command


setup(
    name='xeda',

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description='Cross EDA Abstraction and Automation',
    long_description='''Xeda `/ˈziːdə/` is a cross-platform, cross-EDA, cross-target abstraction and automation platform for digital hardware simulation and synthesis flows.
Xeda can assists hardware developers during verification, evaluation, and deployment of RTL designs. Xeda supports tools and flows from multiple commercial and open-source electronic design automation suites.''',

    # The project's main homepage.
    url='https://github.com/XedaHQ/xeda',


    # Author details
    author='Kamyar Mohajerani',
    author_email='kamyar@ieee.org',

    license='Apache-2.0',
    # https://www.apache.org/licenses/LICENSE-2.0.txt
    # https://opensource.org/licenses/Apache-2.0

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers

    keywords='EDA Electronic Design Automation Tool Synthesis Simulation Hardware Verilog VHDL FPGA ASIC',


    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    # py_modules=['xeda'],


    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html



    # packages=find_packages(),
    # package_dir={'xeda': 'src/xeda'},
    # package_data={"":
    #               [
    #                   '*.xdc', '*.sdf', '*.sdc', '*.dse', '*.fdc', '*.ldc', '*.tcl', '*.json', '*.ys'
    #               ]
    #               },
    # include_package_data=True,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'xeda=xeda:cli.run_xeda',
        ],
    },
)
