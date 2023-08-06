from setuptools import setup, find_packages

setup(
    name='masonite-qiniu',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.1',
    package_dir={'': 'src'},

    description='Qiniu For Masonite',
    long_description='Qiniu For Masonite',

    # The project's main homepage.
    url='https://github.com/puzzle9/masonite-qiniu',

    # Author details
    author='puzzle9',
    author_email='happypuzzle@126.com',

    # Choose your license
    license='MIT',

    # If your package should include things you specify in your MANIFEST.in file
    # Use this option if your package needs to include files that are not python files
    # like html templates or css files
    include_package_data=True,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],

    # What does your project relate to?
    keywords='qiniu masonite',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=[
        'masonite.qiniu',
        'masonite.qiniu.configs',
        'masonite.qiniu.providers',
    ],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "masonite>=2.2.24",
        "qiniu >= 7.x, <8.x"
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # $ pip install your-package[dev,test]
    extras_require={
        'test': ['coverage', 'pytest'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    ## package_data={
    ##     'sample': [],
    ## },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    ## data_files=[('my_data', ['data/data_file.txt'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    ## entry_points={
    ##     'console_scripts': [
    ##         'sample=sample:main',
    ##     ],
    ## },
)
