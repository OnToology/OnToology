import os
from subprocess import call
from Integrator import dolog, ontology_formats

ar2dtool_config_types = ['ar2dtool-taxonomy.conf',  'ar2dtool-class.conf']



from OnToology.autoncore import build_file_structure
from OnToology.autoncore import get_file_from_path, get_target_home, delete_dir, get_parent_path
from OnToology.autoncore import get_abs_path, log_file_dir, verification_log_fname
import OnToology.settings as settings


ar2dtool_config_types = ['ar2dtool-taxonomy.conf',  'ar2dtool-class.conf']
ar2dtool_config = os.environ['tools_config_dir']

# e.g. ar2dtool_dir = 'blahblah/ar2dtool/bin/'
ar2dtool_dir = os.environ['ar2dtool_dir']


def draw_diagrams(rdf_files):
    dolog(str(len(rdf_files)) + ' changed files')
    for r in rdf_files:
        if r[-4:] in ontology_formats:
            for t in ar2dtool_config_types:
                draw_file(r, t)


def get_ar2dtool_config(config_type):
    f = open(ar2dtool_config + '/' + config_type, "r")
    return f.read()


def draw_file(rdf_file, config_type):
    outtype = "png"
    rdf_file_abs = build_file_structure(get_file_from_path(
        rdf_file), [get_target_home(), rdf_file, 'diagrams', config_type[:-5]])
    # now will delete the drawing type folder
    delete_dir(get_parent_path(rdf_file_abs))
    rdf_file_abs = build_file_structure(get_file_from_path(
        rdf_file), [get_target_home(), rdf_file, 'diagrams', config_type[:-5]])
    config_file_abs = build_file_structure(
        config_type, [get_target_home(), rdf_file, 'diagrams', 'config'])
    try:
        open(config_file_abs, "r")
    except IOError:
        f = open(config_file_abs, "w")
        f.write(get_ar2dtool_config(config_type))
        f.close()
    except Exception as e:
        dolog('in draw_file: exception opening the file: ' + str(e))
    comm = 'java -jar '
    comm += ar2dtool_dir + 'ar2dtool.jar -i '
    comm += get_abs_path(rdf_file) + ' -o '
    comm += rdf_file_abs + '.' + outtype + ' -t ' + \
        outtype + ' -c ' + config_file_abs + ' -GV -gml '
    if not settings.TEST:
        comm += ' >> "' + log_file_dir + '"'
    comm += " ; echo 'ar2dtool' >> " + os.path.join(get_parent_path(get_parent_path(
        get_parent_path(rdf_file_abs + '.' + outtype))), verification_log_fname)
    dolog(comm)
    call(comm, shell=True)
