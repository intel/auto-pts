"""PTS automation IronPython script

Since PTS requires admin rights, you have to run this script as admin. You need
to use 32 bit IronPython to run this script because PTS is a 32 bit
application.

Run this is script in admin terminal as follows:

ipy.exe autopts.py

"""

import os
import sys
import logging
import argparse

import winutils
from ptsprojects.utils import exec_adb_root
from ptsprojects.testcase import get_max_test_case_desc
import ptscontrol
import ptsprojects.aospbluez as autoprojects

# instance of ptscontrol.PyPTS
PTS = None

log = logging.debug

def parse_args():
    """Parses command line arguments and options"""

    arg_parser = argparse.ArgumentParser(
        description = "PTS automation IronPython script")

    arg_parser.add_argument(
        "workspace",
        help = "Path to PTS workspace to use for testing. It should have pqw6 "
        "extension")

    args = arg_parser.parse_args()

    return args

def init_pts(workspace):
    """Initializes PTS COM objects
    
    workspace -- Path to PTS workspace to use for testing.

    """
    global PTS

    PTS = ptscontrol.PyPTS()
    PTS.open_workspace(workspace)

def init():
    "Initialization procedure"
    winutils.exit_if_not_admin()

    args = parse_args()

    script_name = os.path.basename(sys.argv[0]) # in case it is full path
    script_name_no_ext = os.path.splitext(script_name)[0]

    log_filename = "%s.log" % (script_name_no_ext,)
    logging.basicConfig(format = '%(name)s [%(asctime)s] %(message)s',
                        filename = log_filename,
                        filemode = 'w',
                        level = logging.DEBUG)

    init_pts(args.workspace)
    exec_adb_root()

def main():
    """Main."""
    init()

    test_cases = autoprojects.rfcomm.test_cases(PTS)
    # test_cases = autoprojects.l2cap.test_cases(PTS)
    # test_cases = autoprojects.gap.test_cases(PTS)

    log("Running test cases...")

    num_test_cases = len(test_cases)
    num_test_cases_width = len(str(num_test_cases))
    max_project_name, max_test_case_name = get_max_test_case_desc(test_cases)
    margin = 3

    PTS.set_call_timeout(120000) # milliseconds

    for index, test_case in enumerate(test_cases):
        print (str(index + 1).rjust(num_test_cases_width) +
               "/" +
               str(num_test_cases).ljust(num_test_cases_width + margin) +
               test_case.project_name.ljust(max_project_name + margin) +
               test_case.name.ljust(max_test_case_name + margin - 1)),
        PTS.run_test_case_object(test_case)
        print test_case.status

    print "\nBye!"

if __name__ == "__main__":
    main()
