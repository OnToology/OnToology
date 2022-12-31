import os
from Integrator import dolog, get_file_from_path, build_path, delete_dir
from Integrator import get_parent_path, log_file_dir, config_folder_name
from . import call_and_get_log, timeout_comm
import OnToology.settings as settings


ar2dtool_config_types = ['ar2dtool-taxonomy.conf', 'ar2dtool-class.conf']
ar2dtool_config = os.environ['tools_config_dir']


# e.g. ar2dtool_dir = 'blahblah/ar2dtool/bin/'
ar2dtool_dir = os.environ['ar2dtool_dir']


def draw_diagrams(rdf_files, base_dir):
    dolog("In draw_diagrams")
    dolog(str(len(rdf_files)) + ' changed files')
    return_values = ""
    for r in rdf_files:
        for t in ar2dtool_config_types:
            dolog("r: "+r)
            dolog("t: "+t)
            rr = draw_file(r, t, base_dir)
            dolog("rr: "+rr)
            return_values += rr
    return return_values


def get_ar2dtool_config(config_type):
    f = open(os.path.join(ar2dtool_config, config_type), "r")
    return f.read()


def draw_file(rdf_file, config_type, base_dir):
    outtype = "png"
    dolog("rdf_file_abs")
    rdf_file_abs = build_path(os.path.join(base_dir, config_folder_name, rdf_file, 'diagrams', config_type[:-5],
                                           get_file_from_path(rdf_file)))
    # now will delete the drawing type folder
    dolog("get parent path")
    parent_path = get_parent_path(rdf_file_abs)
    dolog("delete dir from parent path")
    delete_dir(parent_path)
    dolog("rdf_file_abs")
    rdf_file_abs = build_path(os.path.join(base_dir, config_folder_name, rdf_file, 'diagrams', config_type[:-5],
                                           get_file_from_path(rdf_file)))
    dolog("config_file_abs")
    config_file_abs = build_path(os.path.join(base_dir, config_folder_name, rdf_file, 'diagrams', 'config',
                                              config_type))
    dolog("pre write")
    try:
        open(config_file_abs, "r")
    except IOError:
        f = open(config_file_abs, "w")
        f.write(get_ar2dtool_config(config_type))
        f.close()
    except Exception as e:
        dolog('in draw_file: exception opening the file: ' + str(e))
        return 'in draw_file: exception opening the file: ' + str(e)
    dolog("timeout_comm: ")
    dolog(timeout_comm)
    dolog("outtype: ")
    dolog(outtype)
    dolog("config_file_abs: ")
    dolog(config_file_abs)
    comm = timeout_comm + 'java -jar '
    comm += os.path.join(ar2dtool_dir, 'ar2dtool.jar')
    comm += ' -i '
    comm += '"' + os.path.join(base_dir, rdf_file) + '"' + ' -o '
    comm += '"' + rdf_file_abs + '.' + outtype + '"' + ' -t ' + \
        outtype + ' -c ' + config_file_abs + ' -GV -gml '
    if not settings.test_conf['local']:
        comm += ' >> "' + log_file_dir + '"'
    dolog("drawing is: "+comm)
    error_msg, msg = call_and_get_log(comm)
    dolog(str(msg)+str(error_msg))
    return error_msg
