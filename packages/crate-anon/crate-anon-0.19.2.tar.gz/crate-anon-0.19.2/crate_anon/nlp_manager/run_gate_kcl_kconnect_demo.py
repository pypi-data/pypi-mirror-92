#!/usr/bin/env python

"""
crate_anon/nlp_manager/run_gate_kcl_kconnect_demo.py

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

**Run the GATE ANNIE (people and places) demo via CRATE.**

"""

import logging
import os

from cardinal_pythonlib.logs import main_only_quicksetup_rootlogger

from crate_anon.common.constants import (
    CrateDir,
    DEMO_NLP_INPUT_TERMINATOR,
    DEMO_NLP_OUTPUT_TERMINATOR,
    EnvVar,
)
from cardinal_pythonlib.subproc import check_call_verbose
from cardinal_pythonlib.sysops import get_envvar_or_die


def main() -> None:
    """
    Command-line entry point.
    """
    main_only_quicksetup_rootlogger(level=logging.DEBUG)
    gate_home = get_envvar_or_die(EnvVar.GATE_HOME)
    plugin_file = get_envvar_or_die(EnvVar.CRATE_GATE_PLUGIN_FILE)
    kconnect_dir = get_envvar_or_die(EnvVar.KCL_KCONNECT_DIR)
    check_call_verbose([
        "java",
        "-classpath", f"{CrateDir.JAVA_CLASSES}:{gate_home}/lib/*",
        f"-Dgate.home={gate_home}",
        "CrateGatePipeline",
        "--pluginfile", plugin_file,
        "--gate_app", os.path.join(kconnect_dir, "main-bio", "main-bio.xgapp"),
        "--annotation", "Disease_or_Syndrome",
        "--input_terminator", DEMO_NLP_INPUT_TERMINATOR,
        "--output_terminator", DEMO_NLP_OUTPUT_TERMINATOR,
        "--suppress_gate_stdout",
        "--show_contents_on_crash",
        "-v", "-v",
    ])


if __name__ == "__main__":
    main()
