
# trick to manage package versions in one place only
# http://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
import re
VERSIONFILE="ontospy/VERSION.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    VERSIONSTRING = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))




# setup.py proper begins here
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path
import os

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()



def get_package_folders(top_folder, root_path):
    """
    Utility to generate dynamically the list of folders needed by the package_data setting
    ..
        package_data={
             'ontospy': ['viz/static/*.*', 'viz/templates/*.*', 'viz/templates/shared/*.*', 'viz/templates/splitter/*.*', 'viz/templates/markdown/*.*'],
        },
    ...
    """
    _dirs = []
    out = []
    for root, dirs, files in os.walk(top_folder):
        for dir in dirs:
            _dirs.append(os.path.join(root, dir))
    for d in _dirs:
        _d = os.path.join(d, "*.*")
        out.append(_d.replace(root_path+"/", ""))
    return out


# if False:
#     project_root = os.path.join(here, "ontospy")
#     static_root = os.path.join(project_root, "viz", "static")
#     templates_root = os.path.join(project_root, "viz", "templates")
#     # dynamically generate list of data folders
#     package_data_folders = get_package_folders(static_root, project_root) + get_package_folders(templates_root, project_root)
package_data_folders = []

# //// for testing
if False:
    for el in package_data_folders:
        print el, os.path.isdir(el)
# /////



setup(
    name='ontospy',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/distributing.html#version
    version=VERSIONSTRING,

    description='Query, inspect and visualize knowledge models encoded as RDF/OWL ontologies.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/lambdamusic/ontospy',

    # Author details
    author='Michele Pasin',
    author_email='michele.pasin@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='ontology semantic web linked data rdf owl',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # http://python-packaging-user-guide.readthedocs.org/en/latest/requirements/
    # NOTE: packages are installed in reverse order
    install_requires=[
        'rdflib',
        'rdflib-jsonld',
        'SPARQLWrapper',
        'requests',
        'pyfiglet',
        # note: on windows click requires colorama too
        # http://click.pocoo.org/5/utils/#ansi-colors
        'click',
        'colorama',
		'pyparsing',
	],

    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require = {
	'shell-autocomplete': ['readline']
        # 'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #      'ontospy': ['viz/static/*.*', 'viz/templates/*.*', 'viz/templates/shared/*.*', 'viz/templates/splitter/*.*', 'viz/templates/markdown/*.*'],
    # },

    package_data={
        'ontospy': package_data_folders
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            # 'ontospy-sketch=ontospy.extras.sketch:main',
            'ontospy-shell=ontospy.extras.shell:cli_run_shell',
            'ontospy=ontospy.main:main_cli'
        ],
    },
)
