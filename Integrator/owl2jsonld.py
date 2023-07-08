import os
from subprocess import call
from . import dolog, build_path, ontology_formats, get_target_home, tools_conf, get_parent_path, timeout_comm

owl2jsonld_dir = os.environ['owl2jsonld_dir']


def generate_owl2jsonld_file(changed_files, base_dir):
    dolog("in: generate_owl2jsonld_file")
    for r in changed_files:
        if r[-4:] in ontology_formats:
            dolog('will owl2jsonld: ' + r)
            build_owl2jsonld_file(r, base_dir=base_dir)
        else:
            dolog('not ontology: '+r)


def build_owl2jsonld_file(ont_file, base_dir):
    dolog('in owl2jsonld function')
    ctabs = build_path(os.path.join(base_dir, get_target_home(), ont_file, tools_conf['owl2jsonld']['folder_name'],
                                    'context.jsonld'))
    dolog('ctabs %s' % ctabs)
    comm = f" cd '{ get_parent_path(ctabs)}' ; {timeout_comm} java -jar "
    comm += f" '{os.path.join(owl2jsonld_dir, 'owl2jsonld-0.2.1-standalone.jar')}'"
    # comm += os.path.join(owl2jsonld_dir, 'owl2jsonld-0.2.1-standalone.jar')  # ToolLocation
    comm += f" -o '{ctabs}'"
    # comm += " -o " + ctabs  # Output File
    comm += f" 'file://{os.path.join(base_dir, ont_file)}' "
    # comm += ' file://' + os.path.join(base_dir, ont_file)  # Ontology Location
    dolog(comm)
    call(comm, shell=True)
