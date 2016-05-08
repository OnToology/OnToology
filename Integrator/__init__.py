import ConfigParser

import os

ontology_formats = ['.rdf', '.owl', '.ttl']

config_folder_name = 'OnToology'
config_file_name = 'OnToology.cfg'
repo_abs_dir = ''


def dolog(msg):
    pass


def get_file_from_path(f):
    return f.split('/')[-1]


def get_target_home():
    return 'OnToology'


def config_for_file(file):
    """
    :param f: relative directory of the file e.g. dir1/dir2/my.owl
    :return:
    """
    # return the file configuration from
    pass


def handle_single_ofile(changed_file):
    """
    :param changed_file: relative directory of the file e.g. dir1/dir2/my.owl
    :return:
    """
    if changed_file[:-4] in ontology_formats:
        pass
    # check configuration
    # if ar2dtool then perform
    # if widoco then perform
    # if oops then perform
    pass


def create_of_get_conf(ofile):
    """
    :param ofile: relative directory of the file e.g. dir1/dir2/my.owl
    :return:
    """
    ofile_config_file = os.path.join(config_folder_name, ofile, config_file_name)
    build_path(ofile_config_file)
    f_abs = os.path.join(repo_abs_dir, ofile_config_file)
    dolog('config is called: ')
    ar2dtool_sec_name = 'ar2dtool'
    widoco_sec_name = 'widoco'
    oops_sec_name = 'oops'
    owl2jsonld_sec_name = 'owl2jsonld'
    ar2dtool_enable = True
    widoco_enable = True
    oops_enable = True
    owl2jsonld_enable = True
    config = ConfigParser.RawConfigParser()
    conf_file = config.read(f_abs)
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
        dolog(ofile+' configuration file does not exists')
        config.add_section(ar2dtool_sec_name)
        config.set(ar2dtool_sec_name, 'enable', ar2dtool_enable)
        config.add_section(widoco_sec_name)
        config.set(widoco_sec_name, 'enable', widoco_enable)
        config.add_section(oops_sec_name)
        config.set(oops_sec_name, 'enable', oops_enable)
        config.add_section(owl2jsonld_sec_name)
        config.set(owl2jsonld_sec_name, 'enable', owl2jsonld_enable)
        dolog('will create conf file: ' + f_abs)
        try:
            with open(f_abs, 'wb') as configfile:
                config.write(configfile)
        except Exception as e:
            dolog('exception: ')
            dolog(e)
    return {'ar2dtool_enable': ar2dtool_enable,
            'widoco_enable': widoco_enable,
            'oops_enable': oops_enable,
            'owl2jsonld_enable': owl2jsonld_enable}


def build_path(file_with_rel_dir):
    """
    :param file_with_rel_dir:
    :return: abs_dir as string
    """
    abs_dir = os.path.join(repo_abs_dir, file_with_rel_dir)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    return abs_dir




