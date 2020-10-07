import os

import requests


from . import dolog, get_file_from_path, tools_conf, build_path_all, get_target_home, get_parent_path, log_file_dir, g
from . import call_and_get_log, timeout_comm

from subprocess import call
import shutil


oops_dir = os.environ['oops_dir']


def oops_ont_files(target_repo, changed_files, base_dir):
    results = ""
    for r in changed_files:
        # if valid_ont_file(r): # this is moved to the caller function, we assume here the changed_files are all ont
        dolog('will oops: ' + r)
        try:
            results += generate_oops_report(target_repo, r, base_dir)
        except Exception as e:
            dolog("for file: "+r+" cannot evaluate it using oops error: "+str(e))
    return results


def generate_oops_report(target_repo, ontology_rel_dir, base_dir):
    python_venv = os.path.join(oops_dir, '.venv/bin/python')
    dolog("python_venv: %s"%python_venv)
    ontology_dir = os.path.join(base_dir, ontology_rel_dir)
    dolog("ontology dir: %s"%ontology_dir)
    report_output_dir = os.path.join(base_dir, get_target_home(), ontology_rel_dir, tools_conf['oops']['folder_name'])
    dolog("report output dir: %s"%report_output_dir)
    build_path_all(report_output_dir)
    dolog("path is built")
    dolog("report output dir: %s"%report_output_dir)
    # report_output_abs_file = os.path.join(report_output_dir, 'oops.html')
    # dolog("report output file: %s"%report_output_abs_file)
    comm = "%s %s --ontologydir '%s' --outputdir '%s'" % (python_venv, os.path.join(oops_dir, 'main.py'), ontology_dir, report_output_dir)
    dolog("comm: %s" % comm)
    error_msg, msg = call_and_get_log(comm)
    dolog("msg: %s"%msg)
    dolog("error_msg: %s"%error_msg)
    if "exception in generating oops error" in msg:
        return "Error in generating OOPS! evaluation report"
    return ""
