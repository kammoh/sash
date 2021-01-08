from setuptools import setup, find_packages

setup(
    name='xeda',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    # version='0.0.3',

    version_config={
        "version_style": {
            "style": "semver",
            "dirty": True,
        },
    },

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
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='EDA Electronic Design Automation Tool Synthesis Simulation Hardware Verilog VHDL FPGA ASIC',
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    # py_modules=['xeda'],

    python_requires='>=3.6, <4',

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "jinja2>=2.11.2", "colored", "progress>=1.5", "coloredlogs>=14", "pebble>=4", "numpy>=1", 'psutil',
        "tomlkit>=0.7"
    ],

    setup_requires=['setuptools-vcs-version'],


    package_data={"":
                  [
                      '*.xdc', '*.sdf', '*.sdc', '*.dse', '*.fdc', '*.ldc', '*.tcl', '*.json', '*.ys'
                  ]
                  },
    include_package_data=True,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'xeda=xeda:cli.run_xeda',
        ],
    }
)
