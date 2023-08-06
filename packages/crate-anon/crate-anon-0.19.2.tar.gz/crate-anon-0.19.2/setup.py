#!/usr/bin/env python

"""
setup.py

===============================================================================

    Copyright (C) 2015-2021 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.

===============================================================================

CRATE setup file

To use:

    python setup.py sdist --extras

    twine upload dist/*

To install in development mode:

    pip install -e .

More reasoning is in the setup.py file for CamCOPS.
"""
# https://packaging.python.org/en/latest/distributing/#working-in-development-mode  # noqa
# http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
# http://jtushman.github.io/blog/2013/06/17/sharing-code-across-applications-with-python/  # noqa

import argparse
from setuptools import find_packages, setup
from codecs import open
import fnmatch
import os
import platform
from pprint import pformat
import shutil
import sys
from typing import List

from crate_anon.version import CRATE_VERSION

assert sys.version_info >= (3, 6), "Need Python 3.6+"


# =============================================================================
# Helper functions
# =============================================================================

def deltree(path: str, verbose: bool = False) -> None:
    if verbose:
        print(f"Deleting directory: {path}")
    shutil.rmtree(path, ignore_errors=True)


# Files not to bundle
SKIP_PATTERNS = [
    "*.gitignore",  # .gitignore files
    "*.class",  # compiled Java
    "*.pyc",  # "compiled" Python
    "~*",  # temporary files
    "*~",  # autosave files
]


def add_all_files(root_dir: str,
                  filelist: List[str],
                  absolute: bool = False,
                  relative_to: str = "",
                  include_n_parents: int = 0,
                  verbose: bool = False,
                  skip_patterns: List[str] = None) -> None:
    skip_patterns = skip_patterns or SKIP_PATTERNS
    if absolute or relative_to:
        base_dir = root_dir
    else:
        base_dir = os.path.abspath(
            os.path.join(root_dir, *(['..'] * include_n_parents)))
    for dir_, subdirs, files in os.walk(root_dir, topdown=True):
        if absolute or relative_to:
            final_dir = dir_
        else:
            final_dir = os.path.relpath(dir_, base_dir)
        for filename in files:
            _, ext = os.path.splitext(filename)
            final_filename = os.path.join(final_dir, filename)
            if relative_to:
                final_filename = os.path.relpath(final_filename, relative_to)
            if any(fnmatch.fnmatch(final_filename, pattern)
                   for pattern in skip_patterns):
                if verbose:
                    print(f"Skipping: {final_filename}")
                continue
            if verbose:
                print(f"Adding: {final_filename}")
            filelist.append(final_filename)


# =============================================================================
# Constants
# =============================================================================

# Arguments
EXTRAS_ARG = "extras"

# Directories
THIS_DIR = os.path.abspath(os.path.dirname(__file__))  # .../crate
CRATE_ROOT_DIR = os.path.join(THIS_DIR, "crate_anon")  # .../crate/crate_anon/
DOC_ROOT_DIR = os.path.join(THIS_DIR, "docs")
DOC_HTML_DIR = os.path.join(DOC_ROOT_DIR, "build", "html")
EGG_DIR = os.path.join(THIS_DIR, "crate_anon.egg-info")

# Files
DOCMAKER = os.path.join(DOC_ROOT_DIR, "rebuild_docs.py")
MANIFEST_FILE = os.path.join(THIS_DIR, "MANIFEST.in")  # we will write this
PIP_REQ_FILE = os.path.join(THIS_DIR, "requirements.txt")

# OS; setup.py is executed on the destination system at install time, so:
RUNNING_WINDOWS = platform.system() == "Windows"

# Get the long description from the README file
with open(os.path.join(THIS_DIR, "README.rst"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

# Package dependencies
INSTALL_REQUIRES = [
    "amqp==2.6.0",  # amqp is used by Celery
    "appdirs==1.4.4",  # where to store some temporary data
    "arrow==0.15.7",  # [pin exact version from cardinal_pythonlib]
    "beautifulsoup4==4.9.1",  # [pin exact version from cardinal_pythonlib]
    "cardinal_pythonlib==1.0.95",  # RNC libraries
    "cairosvg==2.5.1",  # work with SVG files
    "celery==4.4.6",  # back-end scheduling
    "chardet==3.0.4",  # character encoding detection for cardinal_pythonlib  # noqa
    "cherrypy==18.6.0",  # Cross-platform web server
    "colorlog==4.1.0",  # colour in logs
    "distro==1.5.0",  # replaces platform.linux_distribution
    "django==3.0.8",  # for main CRATE research database web server
    "django-debug-toolbar==3.0a2",  # Django debug toolbar
    # "django-debug-toolbar-template-profiler==2.0.1",  # v1.0.1 removed 2017-01-30: division by zero when rendering time is zero  # noqa
    "django-extensions==3.0.3",  # for graph_models, show_urls etc.
    "django-picklefield==3.0.1",  # NO LONGER USED - dangerous to use pickle - but kept for migrations  # noqa
    # "django-silk==4.0.1",  # Django profiler
    "django-sslserver==0.22",  # SSL development server for Django
    "flake8==3.8.4",  # code checks
    "flashtext==2.7",  # fast word replacement with the FlashText algorithm
    "flower==0.9.5",  # debug Celery; web server; only runs explicitly
    "fuzzy==1.2.2",  # phonetic matching
    "gunicorn==20.0.4",  # UNIX only, though will install under Windows
    "kombu==4.6.11",  # AMQP library for Celery; requires VC++ under Windows
    "mako==1.1.3",  # templates with Python in
    "MarkupSafe==1.1.1",  # for HTML escaping
    # mmh3 requires VC++
    "mmh3==2.5.1",  # MurmurHash, for fast non-cryptographic hashing; optionally used by cardinal_pythonlib; requires VC++ under Windows?  # noqa
    "openpyxl==3.0.4",  # read Excel
    "pendulum==2.1.1",  # dates/times
    "pillow==7.2.0",  # image processing; import as PIL (Python Imaging Library)  # noqa
    "pdfkit==0.6.1",  # interface to wkhtmltopdf
    "prettytable==0.7.2",  # pretty formating of text-based tables
    "psutil==5.7.2",  # process management
    "pygments==2.6.1",  # syntax highlighting
    "pyparsing==2.4.7",  # generic grammar parser
    "PyPDF2==1.26.0",  # [pin exact version from cardinal_pythonlib]
    "pytest==6.0.2",  # automatic testing
    "pytz==2020.1",  # timezones
    "python-dateutil==2.8.1",  # [pin exact version from cardinal_pythonlib]
    # "python-docx==0.8.10",  # needs lxml, which has Visual C++ dependencies under Windows  # noqa
    # ... https://python-docx.readthedocs.org/en/latest/user/install.html
    "regex==2020.7.14",  # better regexes (cf. re)
    "semantic_version==2.8.5",  # semantic versioning; better than semver
    "sortedcontainers==2.2.2",  # for SortedSet
    "SQLAlchemy==1.3.18",  # database access
    "sqlparse==0.3.1",  # [pin exact version from cardinal_pythonlib]
    "unidecode==1.1.1",  # for removing accents
    "xlrd==1.2.0",  # for ONS postcode database handling; read Excel files

    # Packages for cloud NLP:
    "bcrypt==3.1.7",  # bcrypt encryption
    "cryptography==3.3.1",  # cryptography library
    # "mysqlclient",  # database access
    "paste==3.4.2",  # middleware; https://github.com/cdent/paste/
    "pyramid==1.10.4",  # Pyramid web framework
    "pyramid_tm==2.4",  # Pyramid transaction management
    "redis==3.5.3",  # interface to Redis in-memory key-value database
    "requests==2.24.0",  # HTTP requests
    "tornado==6.0.4",  # web framework
    "transaction==3.0.0",  # generic transaction management
    "urllib3==1.25.9",  # used by requests
    "waitress==1.4.4",  # pure-Python WSGI server
    "zope.sqlalchemy==1.3",  # Zope/SQLAlchemy transaction integration

    # For development only:
    "sphinx==3.1.2",  # documentation
    "sphinx_rtd_theme==0.5.0",  # documentation

    # ---------------------------------------------------------------------
    # For database connections (see manual): install manually
    # ---------------------------------------------------------------------
    # MySQL: one of:
    #   "PyMySQL",
    #   "mysqlclient",
    # SQL Server / ODBC route:
    #   "django-pyodbc-azure",
    #   "pyodbc",  # has C prerequisites
    #   "pypyodbc==1.3.3",
    # SQL Server / Embedded FreeTDS route:
    #   "django-pymssql",
    #   "django-mssql",
    #   "pymssql",
    # PostgreSQL:
    #   "psycopg2",  # has prerequisites (e.g. pg_config executable)

]

if RUNNING_WINDOWS:
    INSTALL_REQUIRES += [
        # Windows-specific stuff
        "pypiwin32==223",
    ]


# =============================================================================
# There's a nasty caching effect. So remove the old ".egg_info" directory
# =============================================================================
# http://blog.codekills.net/2011/07/15/lies,-more-lies-and-python-packaging-documentation-on--package_data-/  # noqa

deltree(EGG_DIR, verbose=True)


# =============================================================================
# If we run this with "python setup.py sdist --extras", we *BUILD* the package
# and do all the extras. (When the end user installs it, that argument will be
# absent.)
# =============================================================================

parser = argparse.ArgumentParser()
parser.add_argument(
    '--' + EXTRAS_ARG, action='store_true',
    help=(
        f"USE THIS TO CREATE PACKAGES (e.g. "
        f"'python setup.py sdist --{EXTRAS_ARG}. Copies extra info in."
    )
)
our_args, leftover_args = parser.parse_known_args()
sys.argv[1:] = leftover_args

extra_files = []  # type: List[str]

if getattr(our_args, EXTRAS_ARG):
    # Here's where we do the extra stuff.

    # -------------------------------------------------------------------------
    # Add extra files
    # -------------------------------------------------------------------------

    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/consent/templates'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/research/templates'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/static'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/specimen_archives'),  # noqa
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/templates'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'crateweb/userprofile/templates'),  # noqa
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'nlp_manager'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)
    # ... for the Java and .ini files
    add_all_files(os.path.join(CRATE_ROOT_DIR, 'testdocs_for_text_extraction'),
                  extra_files, relative_to=THIS_DIR,
                  skip_patterns=SKIP_PATTERNS)

    extra_files.sort()
    print(f"EXTRA_FILES: \n{pformat(extra_files)}")

    # -------------------------------------------------------------------------
    # Write the manifest (ensures files get into the source distribution).
    # -------------------------------------------------------------------------
    manifest_lines = ['include ' + x for x in extra_files]
    with open(MANIFEST_FILE, 'wt') as manifest:
        manifest.writelines([
            "# This is an AUTOCREATED file, MANIFEST.in; see setup.py and DO "
            "NOT EDIT BY HAND"])
        manifest.write("\n\n" + "\n".join(manifest_lines) + "\n")

    # -------------------------------------------------------------------------
    # Write requirements.txt (helps PyCharm)
    # -------------------------------------------------------------------------
    with open(PIP_REQ_FILE, "w") as req_file:
        for line in INSTALL_REQUIRES:
            req_file.write(line + "\n")


# =============================================================================
# setup args
# =============================================================================

setup(
    name="crate-anon",  # "crate" is taken

    version=CRATE_VERSION,

    description="CRATE: clinical records anonymisation and text extraction",
    long_description=LONG_DESCRIPTION,

    # The project"s main homepage.
    url="https://crateanon.readthedocs.io",

    # Author details
    author="Rudolf Cardinal",
    author_email="rudolf@pobox.com",

    # Choose your license
    license="GNU General Public License v3 or later (GPLv3+)",

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",

        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",

        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa

        "Natural Language :: English",

        "Operating System :: OS Independent",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",

        "Topic :: System :: Hardware",
        "Topic :: System :: Networking",
    ],

    keywords="anonymisation",

    packages=find_packages(),
    # finds all the .py files in subdirectories, as long as there are
    # __init__.py files

    package_data={
        "crate_anon": extra_files,
    },

    include_package_data=True,  # use MANIFEST.in during install?
    # https://stackoverflow.com/questions/7522250/how-to-include-package-data-with-setuptools-distribute  # noqa

    install_requires=INSTALL_REQUIRES,

    entry_points={
        "console_scripts": [
            # Format is "script=module:function".

            # Documentation

            "crate_help=crate_anon.tools.launch_docs:main",

            # Preprocessing

            "crate_fetch_wordlists=crate_anon.anonymise.fetch_wordlists:main",
            "crate_postcodes=crate_anon.preprocess.postcodes:main",
            "crate_preprocess_pcmis=crate_anon.preprocess.preprocess_pcmis:main",  # noqa
            "crate_preprocess_rio=crate_anon.preprocess.preprocess_rio:main",

            # Linkage

            "crate_bulk_hash=crate_anon.linkage.bulk_hash:main",
            "crate_fuzzy_id_match=crate_anon.linkage.fuzzy_id_match:main",

            # Anonymisation

            "crate_anonymise=crate_anon.anonymise.anonymise_cli:main",
            "crate_anonymise_multiprocess=crate_anon.anonymise.launch_multiprocess_anonymiser:main",  # noqa
            "crate_make_demo_database=crate_anon.anonymise.make_demo_database:main",  # noqa
            "crate_test_anonymisation=crate_anon.anonymise.test_anonymisation:main",  # noqa
            "crate_test_extract_text=crate_anon.anonymise.test_extract_text:main",  # noqa

            # NLP

            "crate_nlp=crate_anon.nlp_manager.nlp_manager:main",
            "crate_nlp_build_gate_java_interface=crate_anon.nlp_manager.build_gate_java_interface:main",  # noqa
            "crate_nlp_build_medex_itself=crate_anon.nlp_manager.build_medex_itself:main",  # noqa
            "crate_nlp_build_medex_java_interface=crate_anon.nlp_manager.build_medex_java_interface:main",  # noqa
            "crate_nlp_multiprocess=crate_anon.nlp_manager.launch_multiprocess_nlp:main",  # noqa
            "crate_nlp_prepare_ymls_for_bioyodie=crate_anon.nlp_manager.prepare_umls_for_bioyodie:main",  # noqa
            "crate_run_crate_nlp_demo=crate_anon.nlp_manager.run_crate_nlp_demo:main",  # noqa
            "crate_run_gate_annie_demo=crate_anon.nlp_manager.run_gate_annie_demo:main",  # noqa
            "crate_run_gate_kcl_kconnect_demo=crate_anon.nlp_manager.run_gate_kcl_kconnect_demo:main",  # noqa
            "crate_run_gate_kcl_lewy_demo=crate_anon.nlp_manager.run_gate_kcl_lewy_demo:main",  # noqa
            "crate_run_gate_kcl_pharmacotherapy_demo=crate_anon.nlp_manager.run_gate_kcl_pharmacotherapy_demo:main",  # noqa
            "crate_show_crate_gate_pipeline_options=crate_anon.nlp_manager.show_crate_gate_pipeline_options:main",  # noqa
            "crate_show_crate_medex_pipeline_options=crate_anon.nlp_manager.show_crate_medex_pipeline_options:main",  # noqa

            # Web site

            "crate_celery_status=crate_anon.tools.celery_status:main",
            "crate_django_manage=crate_anon.crateweb.manage:main",  # will cope with argv  # noqa
            "crate_email_rdbm=crate_anon.tools.email_rdbm:main",
            "crate_generate_new_django_secret_key=cardinal_pythonlib.django.tools.generate_new_django_secret_key:main",  # noqa
            "crate_launch_celery=crate_anon.tools.launch_celery:main",
            "crate_launch_flower=crate_anon.tools.launch_flower:main",
            "crate_print_demo_crateweb_config=crate_anon.tools.print_crateweb_demo_config:main",  # noqa
            "crate_windows_service=crate_anon.tools.winservice:main",

            # Indirect shortcuts to "crate_django_manage" commands:
            "crate_launch_cherrypy_server=crate_anon.tools.launch_cherrypy_server:main",  # noqa
            # ... a separate script with ":main" rather than
            # "crate_anon.crateweb.manage:runcpserver" so that we can launch
            # the "runcpserver" function from our Windows service, and have it
            # deal with the CherryPy special environment variable
            "crate_launch_django_server=crate_anon.crateweb.manage:runserver",

            # NLP web server

            "crate_nlp_webserver_generate_encryption_key=crate_anon.nlp_webserver.security:generate_encryption_key",  # noqa
            "crate_nlp_webserver_initialize_db=crate_anon.nlp_webserver.initialize_db:main",  # noqa
            "crate_nlp_webserver_launch_celery=crate_anon.tools.launch_nlp_webserver_celery:main",  # noqa
            "crate_nlp_webserver_launch_flower=crate_anon.tools.launch_nlp_webserver_flower:main",  # noqa
            "crate_nlp_webserver_launch_gunicorn=crate_anon.tools.launch_nlp_webserver_gunicorn:main",  # noqa
            "crate_nlp_webserver_manage_users=crate_anon.nlp_webserver.manage_users:main",  # noqa
            "crate_nlp_webserver_print_demo=crate_anon.nlp_webserver.print_demos:main",  # noqa
            "crate_nlp_webserver_pserve=pyramid.scripts.pserve:main",  # noqa

        ],
        # Entry point for nlp webserver
        "paste.app_factory": [
            "main = crate_anon.nlp_webserver.wsgi_app:make_wsgi_app",
            # ... means we can launch with "pserve <config_file>"; see
            # https://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/pylons/launch.html  # noqa
        ],
        "paste.server_runner": [
            "cherrypy = crate_anon.nlp_webserver.wsgi_launchers:cherrypy",
            "waitress = crate_anon.nlp_webserver.wsgi_launchers:waitress",
        ],
    },
)
