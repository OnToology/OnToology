

from . import get_file_from_path, get_target_home

import os
from subprocess import call

from . import dolog, build_path
from . import ontology_formats, get_parent_path, log_file_dir
from . import call_and_get_log, timeout_comm
#  import ontoology.settings as settings


tools_config_dir = os.environ['tools_config_dir']

# e.g. widoco_dir = 'blahblah/Widoco/JAR/'
widoco_dir = os.environ['widoco_dir']
widoco_config = os.path.join(tools_config_dir, 'widoco.conf')


def get_widoco_config():
    f = open(widoco_config, "r")
    return f.read()


def generate_widoco_docs(changed_files, base_dir, languages, webVowl):
    results = ""
    for r in changed_files:
        if r[-4:] in ontology_formats:
            dolog('will widoco '+r)
            results += create_widoco_doc(r, base_dir, languages, webVowl)
        else:
            pass
    return results


def create_widoco_doc(rdf_file, base_dir, languages, webVowl):
    dolog('in Widoco function')
    rdf_file_abs = os.path.join(base_dir, rdf_file)
    # rdf_file_abs = get_abs_path(rdf_file)
    # config_file_abs = build_file_structure(os.path.join(base_dir, get_file_from_path(rdf_file) + '.widoco.conf'),
    #                                       [get_target_home(), rdf_file, 'documentation'])
    config_file_abs = build_path(os.path.join(base_dir, get_target_home(), rdf_file, 'documentation',
                                                        get_file_from_path(rdf_file) + '.widoco.conf'))
    dolog('rdf_abs: %s and config_file_abs %s' % (rdf_file_abs, config_file_abs))
    use_conf_file = True
    try:
        open(config_file_abs, "r")
    except IOError:
        use_conf_file = False
    except Exception as e:
        dolog('in create_widoco_doc: exception opening the file: ' + str(e))
    out_abs_dir = get_parent_path(config_file_abs)
    comm = "cd " + base_dir + "; "
    comm += timeout_comm + "java -jar "
    comm += ' -Dfile.encoding=utf-8 '
    comm += widoco_dir + "widoco.jar  -rewriteAll "
    #comm += widoco_dir + "widoco-0.0.1-jar-with-dependencies.jar  "
    comm += " -ontFile '" + rdf_file_abs
    comm += "' -outFolder '" + out_abs_dir + "'"
    if use_conf_file:
        comm += " -confFile " + config_file_abs
        comm += " -crossRef"
    else:
        comm += " -getOntologyMetadata "
        comm += " -licensius "  # Only works if the -getOntologyMetadata flag is enabled.
        comm += " -saveConfig " + config_file_abs
    comm += " -htaccess "
    if webVowl:
        comm += " -webVowl "
    comm += '-lang %s' % ('-'.join(languages))
    # if not settings.TEST:
    dolog("languages: ")
    dolog(languages)
    dolog("merged: ")
    dolog('-'.join(languages))
    if True:
        comm += ' >> "' + log_file_dir + '" '
    #comm += " ; echo 'widoco' >> " + os.path.join(get_parent_path(out_abs_dir), verification_log_fname)
    dolog(comm)
    #return_code = call(comm, shell=True)
    error_msg, msg = call_and_get_log(comm)
    dolog(msg+error_msg)
    if error_msg != "":
        return "Error while generating the documentation"
    return ""
