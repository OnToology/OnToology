import os
from subprocess import call
from Integrator import dolog, get_file_from_path, build_path, delete_dir, verification_log_fname
from Integrator import get_parent_path, log_file_dir, config_folder_name

from . import call_and_get_log, timeout_comm

import sys


ar2dtool_config_types = ['ar2dtool-taxonomy.conf', 'ar2dtool-class.conf']

from OnToology.autoncore import get_target_home
import OnToology.settings as settings


ar2dtool_config_types = ['ar2dtool-taxonomy.conf', 'ar2dtool-class.conf']
ar2dtool_config = os.environ['tools_config_dir']


# e.g. ar2dtool_dir = 'blahblah/ar2dtool/bin/'
ar2dtool_dir = os.environ['ar2dtool_dir']


def draw_diagrams(rdf_files, base_dir):
    dolog(str(len(rdf_files)) + ' changed files')
    return_values = ""
    for r in rdf_files:
        for t in ar2dtool_config_types:
            rr = draw_file(r, t, base_dir)
            return_values += rr
    return return_values


def get_ar2dtool_config(config_type):
    f = open(ar2dtool_config + '/' + config_type, "r")
    return f.read()


def draw_file(rdf_file, config_type, base_dir):
    outtype = "png"
    rdf_file_abs = build_path(os.path.join(base_dir, config_folder_name, rdf_file, 'diagrams', config_type[:-5],
                                           get_file_from_path(rdf_file)))
    # now will delete the drawing type folder
    delete_dir(get_parent_path(rdf_file_abs))
    rdf_file_abs = build_path(os.path.join(base_dir, config_folder_name, rdf_file, 'diagrams', config_type[:-5],
                                           get_file_from_path(rdf_file)))
    config_file_abs = build_path(os.path.join(base_dir, config_folder_name, rdf_file, 'diagrams', 'config',
                                              config_type))
    try:
        open(config_file_abs, "r")
    except IOError:
        f = open(config_file_abs, "w")
        f.write(get_ar2dtool_config(config_type))
        f.close()
    except Exception as e:
        dolog('in draw_file: exception opening the file: ' + str(e))
        return 'in draw_file: exception opening the file: ' + str(e)
    comm = timeout_comm + 'java -jar '
    comm += ar2dtool_dir + 'ar2dtool.jar -i '
    comm += '"' + os.path.join(base_dir, rdf_file) + '"' + ' -o '
    comm += '"' + rdf_file_abs + '.' + outtype + '"' + ' -t ' + \
        outtype + ' -c ' + config_file_abs + ' -GV -gml '
    if not settings.TEST:
       comm += ' >> "' + log_file_dir + '"'
    # comm += " ; echo 'ar2dtool' >> " + os.path.join(get_parent_path(get_parent_path(
    #    get_parent_path(rdf_file_abs + '.' + outtype))), verification_log_fname)
    dolog("drawing is: "+comm)
    error_msg, msg = call_and_get_log(comm)
    dolog(msg+error_msg)
    return error_msg
