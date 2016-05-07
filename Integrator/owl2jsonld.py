import os
from ontoology.autoncore import dolog, valid_ont_file, build_file_structure, get_abs_path, tools_conf, get_target_home
from ontoology.autoncore import get_parent_path
from subprocess import call


# Must end with a '/':
owl2jsonld_dir = os.environ['owl2jsonld_dir']


def generate_owl2jsonld_file(changed_files):
    for r in changed_files:
        if valid_ont_file(r):
            dolog('will owl2jsonld: ' + r)
            build_owl2jsonld_file(r)


def build_owl2jsonld_file(ont_file):
    dolog('in owl2jsonld function')
    ont_file_abs = get_abs_path(ont_file)
    ctabs = build_file_structure('context.jsonld',
                                 [get_target_home(), ont_file,
                                  tools_conf['owl2jsonld']['folder_name']])
    dolog('ont_abs: %s and ctabs %s' % (ont_file_abs, ctabs))
    comm = "cd " + get_parent_path(ctabs) + "; "  # Not neccesary
    comm += "java -jar "
    comm += owl2jsonld_dir + "owl2jsonld-0.2.1-standalone.jar "  # ToolLocation
    comm += "-o " + ctabs  # Output File
    comm += "file://" + ont_file_abs  # Ontology Location
    dolog(comm)
    call(comm, shell=True)
