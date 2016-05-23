import ConfigParser
import os
from subprocess import call

import logging


ontology_formats = ['.rdf', '.owl', '.ttl']
config_folder_name = 'OnToology'
config_file_name = 'OnToology.cfg'
log_file_dir = ''  # need to be set some how
verification_log_fname = 'verification.log'

g = None

# def dolog(msg):
#     print(msg)
#     # dolog_function(msg)

tools_conf = {
    'ar2dtool': {'folder_name': 'diagrams', 'type': 'png'},
    'widoco': {'folder_name': 'documentation'},
    'oops': {'folder_name': 'evaluation'},
    'owl2jsonld': {'folder_name': 'context'}
}


def dolog_logg(msg):
    logging.critical(msg)


def p(msg):
    print(msg)

dolog = p


def prepare_logger(log_fname):
    logging.basicConfig(filename=log_fname, format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)


def tools_execution(changed_files, base_dir, logfile, dolog_fname=None, target_repo=None, g_local=None):
    """
    :param changed_files:  changed files include relative path
            base_dir: abs dir to the repo file name, e.g. /home/user/myrepo/
    :return:
    """
    global g
    global dolog
    global log_file_dir
    g = g_local
    log_file_dir = logfile
    if dolog_fname is not None:
        prepare_logger(dolog_fname)
        dolog = dolog_logg
    for f in changed_files:
        dolog("tools_execution: "+f)
        handle_single_ofile(f, base_dir, target_repo=target_repo)


def handle_single_ofile(changed_file, base_dir, target_repo):
    """
    assuming the change_file is an ontology file
    :param changed_file: relative directory of the file e.g. dir1/dir2/my.owl
    :return:
    """
    import ar2dtool
    import widoco
    import oops
    dolog("will call create or get conf")
    conf = create_of_get_conf(changed_file, base_dir)
    dolog("conf: "+str(conf))
    if conf['ar2dtool_enable']:
        dolog("will call draw diagrams")
        ar2dtool.draw_diagrams([changed_file], base_dir)
    if conf['widoco_enable']:
        dolog('will call widoco')
        widoco.generate_widoco_docs([changed_file], base_dir)
    if conf['oops_enable']:
        dolog('will call oops')
        oops.oops_ont_files(target_repo=target_repo, changed_files=[changed_file], base_dir=base_dir)


def create_of_get_conf(ofile, base_dir):
    """
    :param ofile: relative directory of the file e.g. dir1/dir2/my.owl
    :return:
    """
    ofile_config_file_rel = os.path.join(config_folder_name, ofile, config_file_name)
    ofile_config_file_abs = os.path.join(base_dir, ofile_config_file_rel)
    build_path(ofile_config_file_abs)
    dolog('config is called')
    ar2dtool_sec_name = 'ar2dtool'
    widoco_sec_name = 'widoco'
    oops_sec_name = 'oops'
    owl2jsonld_sec_name = 'owl2jsonld'
    ar2dtool_enable = True
    widoco_enable = True
    oops_enable = True
    owl2jsonld_enable = True
    config = ConfigParser.RawConfigParser()
    conf_file = config.read(ofile_config_file_abs)
    if len(conf_file) == 1:
        dolog(ofile+' configuration file exists')
        try:
            ar2dtool_enable = config.getboolean(ar2dtool_sec_name, 'enable')
            dolog('got ar2dtool enable value: ' + str(ar2dtool_enable))
        except:
            dolog('ar2dtool enable value doesnot exist')
            ar2dtool_enable = False
            pass
        try:
            widoco_enable = config.getboolean(widoco_sec_name, 'enable')
            dolog('got widoco enable value: ' + str(widoco_enable))
        except:
            dolog('widoco enable value doesnot exist')
            widoco_enable = False
            pass
        try:
            oops_enable = config.getboolean(oops_sec_name, 'enable')
            dolog('got oops enable value: ' + str(oops_enable))
        except:
            dolog('oops enable value doesnot exist')
            oops_enable = False
        try:
            owl2jsonld_enable = config.getboolean(owl2jsonld_sec_name, 'enable')
            dolog('got owl2jsonld enable value: ' + str(owl2jsonld_enable))
        except:
            dolog('owl2jsonld enable value doesnot exist')
            owl2jsonld_enable = False
    else:
        dolog(ofile+' configuration file does not exists (not an error)')
        config.add_section(ar2dtool_sec_name)
        config.set(ar2dtool_sec_name, 'enable', ar2dtool_enable)
        config.add_section(widoco_sec_name)
        config.set(widoco_sec_name, 'enable', widoco_enable)
        config.add_section(oops_sec_name)
        config.set(oops_sec_name, 'enable', oops_enable)
        config.add_section(owl2jsonld_sec_name)
        config.set(owl2jsonld_sec_name, 'enable', owl2jsonld_enable)
        dolog('will create conf file: ' + ofile_config_file_abs)
        try:
            with open(ofile_config_file_abs, 'wb') as configfile:
                config.write(configfile)
        except Exception as e:
            dolog('exception: ')
            dolog(e)
    return {'ar2dtool_enable': ar2dtool_enable,
            'widoco_enable': widoco_enable,
            'oops_enable': oops_enable,
            'owl2jsonld_enable': owl2jsonld_enable}


#######################
# helper functions  ###
#######################

def build_path(file_with_abs_dir):
    """
    :param file_with_abs_dir:
    :return: abs_dir as string
    """
    # file_with_abs_dir = os.path.join(repo_abs_dir, file_with_rel_dir)
    abs_dir = get_parent_path(file_with_abs_dir)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    dolog("build_path abs_dir: "+abs_dir)  # file_with_abs_dir
    return file_with_abs_dir


def delete_dir(target_directory):
    comm = "rm -Rf " + target_directory
    comm += '  >> "' + log_file_dir + '" '
    dolog(comm)
    call(comm, shell=True)


def get_parent_path(f):
    return '/'.join(f.split('/')[0:-1])


def get_file_from_path(f):
    return f.split('/')[-1]


def get_target_home():
    return 'OnToology'



