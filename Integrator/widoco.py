

from . import get_file_from_path, get_target_home

import os
from subprocess import call

from ontoology.autoncore import dolog, get_abs_path, build_file_structure
from ontoology.autoncore import ontology_formats, get_parent_path, log_file_dir
from ontoology.autoncore import verification_log_fname
import ontoology.settings as settings


tools_config_dir = os.environ['tools_config_dir']

# e.g. widoco_dir = 'blahblah/Widoco/JAR/'
widoco_dir = os.environ['widoco_dir']
widoco_config = os.path.join(tools_config_dir, 'widoco.conf')


def get_widoco_config():
    f = open(widoco_config, "r")
    return f.read()


def generate_widoco_docs(changed_files):
    for r in changed_files:
        if r[-4:] in ontology_formats:
            print 'will widoco ' + r
            create_widoco_doc(r)
        else:
            pass


def create_widoco_doc(rdf_file):
    dolog('in Widoco function')
    rdf_file_abs = get_abs_path(rdf_file)
    config_file_abs = build_file_structure(get_file_from_path(rdf_file) + '.widoco.conf',
                                           [get_target_home(), rdf_file, 'documentation'])
    dolog('rdf_abs: %s and config_file_abs %s' % (rdf_file_abs, config_file_abs))
    use_conf_file = True
    try:
        open(config_file_abs, "r")
    except IOError:
        use_conf_file = False
    except Exception as e:
        dolog('in create_widoco_doc: exception opening the file: ' + str(e))
    out_abs_dir = get_parent_path(config_file_abs)
    comm = "cd " + get_abs_path('') + "; "
    comm += "java -jar "
    comm += ' -Dfile.encoding=utf-8 '
    comm += widoco_dir + "widoco-0.0.1-jar-with-dependencies.jar  -rewriteAll "
    comm += " -ontFile " + rdf_file_abs
    comm += " -outFolder " + out_abs_dir
    if use_conf_file:
        comm += " -confFile " + config_file_abs
    else:
        comm += " -getOntologyMetadata "
        comm += " -saveConfig " + config_file_abs
    if not settings.TEST:
        comm += ' >> "' + log_file_dir + '" '
    comm += " ; echo 'widoco' >> " + os.path.join(get_parent_path(out_abs_dir), verification_log_fname)
    dolog(comm)
    call(comm, shell=True)
