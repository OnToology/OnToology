from ConfigParserList import ConfigParser
import os
import random
import string
from subprocess import call
from OnToology.models import OTask
from OnToology.models import *
import logging

ontology_formats = ['.rdf', '.owl', '.ttl']
config_folder_name = 'OnToology'
config_file_name = 'OnToology.cfg'

logger = logging.getLogger(__name__)
log_file_dir = None
g = None

tools_conf = {
    'ar2dtool': {'folder_name': 'diagrams', 'type': 'png'},
    'widoco': {'folder_name': 'documentation'},
    'oops': {'folder_name': 'evaluation'},
    'owl2jsonld': {'folder_name': 'context'},
    'themis': {'folder_name': 'validation', 'tests_file_name': 'tests.txt', 'results_file_name': 'results.tsv'}
}


def dolog(msg):
    logger.critical(msg)


def p(msg):
    print(msg)


def tools_execution(changed_files, base_dir, target_repo, branch, g_local=None, logfile=None,
                    change_status=None, repo=None, orun=None, m_logger=None):
    """
    :param changed_files:  changed files include relative path
    :param base_dir: abs dir to the repo file name, e.g. /home/user/myrepo/
    :param target_repo:
    :param g_local:
    :param logfile:
    :param change_status:
    :param repo:
    :param orun:
    :param branch:
    :param m_logger:
    :return:
    """
    global g
    global logger
    global log_file_dir

    if m_logger:
        logger = m_logger

    log_file_dir = logfile

    dolog("tools execution")
    g = g_local

    dolog("after the logger")
    repo.notes = ''
    repo.save()
    progress_out_of = 70.0
    if len(changed_files) == 0:
        repo.progress = progress_out_of
        repo.save()
        return
    single_piece = progress_out_of / len(changed_files)
    progress_inc = single_piece / 4.0
    for f in changed_files:
        if f[-4:] in ontology_formats:
            if f[:len('OnToology/')] == 'OnToology/':  # This is to solve bug #265
                dolog("nested prevented bug: " + f)
                continue
            dolog("tools_execution: " + f)
            handle_single_ofile(f, base_dir, target_repo=target_repo, change_status=change_status, repo=repo,
                                progress_inc=progress_inc, orun=orun, branch=branch)


def task_reporter(name=None, desc=None, success=None, finished=None, orun=None, otask=None):
    dolog("taskreporter")
    if orun is None:
        raise Exception("orun cannot be None")
    if otask is None:
        if name is None:
            raise Exception("Expected name if otask is not passed")
        t = OTask(name=name, description='', orun=orun)
        t.save()
    else:
        t = otask
    if desc is not None:
        dolog("desc: " + desc)
        t.description = desc
    else:
        dolog("desc None: " + str(desc))
    if success is not None:
        t.success = success
    if finished is not None:
        t.finished = finished
    t.save()
    return t


def get_conf_as_dict(conf):
    """
    Get dict from a conf object
    """
    d = {section: dict(conf[section]) for section in conf}
    return d


def get_conf_as_str(conf):
    """
    Get str from a conf object
    """
    conf_str = get_conf_as_dict(conf)
    conf_str = str(conf_str)
    return conf_str


def run_syntax(display_onto_name, orun, base_dir, changed_file, repo):
    """
    Syntax Check
    """
    from . import syntaxchecker
    otask = task_reporter("Syntax Check (%s)" % display_onto_name, desc="Check the syntax", orun=orun)
    if not syntaxchecker.valid_syntax(os.path.join(base_dir, changed_file)):
        repo.notes += "syntax error in %s\n" % changed_file
        repo.save()
        task_reporter(otask=otask, desc="Syntax error", finished=True, success=False, orun=orun)
        return False
    task_reporter(otask=otask, desc="Valid syntax", finished=True, success=True, orun=orun)
    return True


def run_ar2dtool(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo, change_status):
    """
    Run AR2DTool
    """
    from . import ar2dtool
    if conf.getboolean('ar2dtool', 'enable'):
        otask = task_reporter("Diagrams (%s)" % display_onto_name, desc="Drawing diagrams", orun=orun)
        dolog("will call draw diagrams")
        change_status(target_repo, 'drawing diagrams for: ' + changed_file)
        repo.update_ontology_status(ontology=changed_file, status='diagram')
        repo.save()
        try:
            ar2dtool.draw_diagrams([changed_file], base_dir)
            otask = task_reporter(otask=otask, desc="Diagrams are drawn", success=True, finished=True, orun=orun)
        except Exception as e:
            dolog("Exception in running ar2dtool.draw_diagrams: " + str(e))
            dolog("changed_file: <" + changed_file + ">")
            task_reporter(otask=otask, desc="Error generating the diagrams: <%s>" % str(e), success=True, finished=True,
                          orun=orun)
    repo.progress += progress_inc
    repo.save()


def run_widoco(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo, change_status):
    """
    Run Widoco
    """
    from . import widoco
    if conf.getboolean('widoco', 'enable'):
        otask = task_reporter("Documentation (%s)" % display_onto_name, desc="Generating HTML documentation", orun=orun)
        dolog('will call widoco')
        change_status(target_repo, 'generating docs for: ' + changed_file)
        repo.update_ontology_status(ontology=changed_file, status='documentation')
        repo.save()
        try:
            widoco.generate_widoco_docs([changed_file], base_dir, languages=conf.getlist('widoco', 'languages'),
                                        webVowl=conf.getboolean('widoco', 'webVowl'))
            otask = task_reporter(otask=otask, desc="HTML documentation is generated", success=True, finished=True,
                                  orun=orun)
        except Exception as e:
            dolog("Exception in running widoco.generate_widoco_docs: " + str(e))
            task_reporter(otask=otask, desc="Error while generating the documentation", success=False, finished=True,
                          orun=orun)
    repo.progress += progress_inc
    repo.save()


def run_oops(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo, change_status):
    """
    Run OOPS!
    """
    from . import oops
    if conf.getboolean('oops', 'enable'):
        otask = task_reporter("Evaluation (%s)" % display_onto_name, desc="Generating OOPS! Evaluation", orun=orun)
        dolog('will call oops')
        change_status(target_repo, 'evaluating: ' + changed_file)
        repo.update_ontology_status(ontology=changed_file, status='evaluation')
        repo.save()
        try:
            r = oops.oops_ont_files(target_repo=target_repo, changed_files=[changed_file], base_dir=base_dir)
            otask = task_reporter(otask=otask, desc="OOPS! reported is generated", orun=orun)
            if r != "":
                dolog("Error in producing OOPS! report: " + str(r))
                repo.notes += "Error in producing the evaluation report for: %s" % str(changed_file)
                repo.save()
                otask = task_reporter(otask=otask, desc="Error generating OOPS! report", finished=True, success=False,
                                      orun=orun)
            else:
                dolog("OOPS! report is generated successfully")
                repo.notes += "Evaluation report is produced for: %s " % str(changed_file)
                repo.save()
                otask = task_reporter(otask=otask, desc="OOPS! reported is generated", finished=True, success=True,
                                      orun=orun)

        except Exception as e:
            dolog("Exception in running oops.oops.oops_ont_files: " + str(e))
            task_reporter(otask=otask, desc="Error generating OOPS! report: " + str(e), finished=True,
                          success=False, orun=orun)
    repo.progress += progress_inc
    repo.save()


def run_owl2jsonld(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo,
                   change_status):
    """
    Run owl2jsonld
    """
    from . import owl2jsonld
    if conf.getboolean('owl2jsonld', 'enable'):
        otask = task_reporter("JSONLD (%s)" % display_onto_name, desc="Generating jsonld", orun=orun)
        dolog('will call owl2jsonld')
        change_status(target_repo, 'generating context for: ' + changed_file)
        repo.update_ontology_status(ontology=changed_file, status='jsonld')
        repo.save()
        try:
            owl2jsonld.generate_owl2jsonld_file([changed_file], base_dir=base_dir)
            otask = task_reporter(otask=otask, desc="jsonld is generated", finished=True, success=True, orun=orun)
        except Exception as e:
            dolog("Exception in running owl2jsonld.generate_owl2jsonld_file: " + str(e))
            task_reporter(otask=otask, desc="jsonld is generated", finished=True, success=False, orun=orun)
    repo.progress += progress_inc
    repo.save()


def run_themis(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo, branch, change_status):
    """
    Run themis
    """
    from . import themis
    if conf.getboolean('themis', 'enable'):
        otask = task_reporter("Validation (%s)" % display_onto_name, desc="Themis validation", orun=orun)
        dolog('will call themis')
        change_status(target_repo, 'generating validation for: ' + changed_file)
        repo.update_ontology_status(ontology=changed_file, status='validation')
        repo.save()
        try:
            themis.validate_ontologies(target_repo=target_repo, branch=branch, changed_files=[changed_file], base_dir=base_dir)
            otask = task_reporter(otask=otask, desc="Themis validation", success=True, finished=True, orun=orun)
        except Exception as e:
            dolog("Exception in running themis: " + str(e))
            task_reporter(otask=otask, desc="Themis validation", success=False, finished=True, orun=orun)
    repo.progress += progress_inc
    repo.save()
    repo.update_ontology_status(ontology=changed_file, status='finished')


def handle_single_ofile(changed_file, base_dir, target_repo, change_status, branch, repo=None, progress_inc=0.0, orun=None):
    """
    assuming the change_file is an ontology file
    :param changed_file: relative directory of the file e.g. dir1/dir2/my.owl
    :param base_dir:
    :param target_repo:
    :param change_status:
    :param repo: a Repo instance of the target repo
    :param progress_inc: how much to increment the progress after each
    :return:
    """

    display_onto_name = changed_file[-15:]
    dolog("changed_file <%s> = display <%s>" % (display_onto_name, changed_file))
    otask = task_reporter("Configuration (%s)" % display_onto_name, desc="Loading configuration", orun=orun)
    dolog("will call create or get conf")
    try:
        conf = create_of_get_conf(changed_file, base_dir)
        conf_str = get_conf_as_str(conf)
        dolog("conf: %s" % conf_str)
        otask = task_reporter(otask=otask, desc="Configuration loaded successfully", finished=True, success=True,
                              orun=orun)
    except Exception as e:
        task_reporter(otask=otask, desc="Configuration Error: " + str(e), finished=True, success=False, orun=orun)
        raise e

    if not run_syntax(display_onto_name, orun, base_dir, changed_file, repo):
        return

    run_ar2dtool(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo, change_status)
    run_widoco(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo, change_status)
    run_oops(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo, change_status)
    run_owl2jsonld(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo,
                   change_status)
    run_themis(conf, display_onto_name, orun, base_dir, changed_file, repo, progress_inc, target_repo, branch, change_status)


def get_default_conf():
    config_result = {
        'widoco': {
            'enable': True,
            'languages': ['en'],
            'webVowl': False,
        },
        'ar2dtool': {
            'enable': True
        },
        'oops': {
            'enable': True
        },
        'owl2jsonld': {
            'enable': True
        },
        'themis': {
            'enable': False
        }
    }
    return config_result


def get_conf_tool_json(conf, tool):
    """
    Get tool
    """
    if tool == "widoco":
        return {
            'enable': conf.getboolean(tool, "enable"),
            'languages': conf.getlist(tool, "languages"),
            'webVowl': conf.getboolean(tool, "webVowl"),
        }
    else:
        return {
            'enable': conf.getboolean(tool, "enable")
        }


def get_default_conf_obj():
    """
    Get default config object
    """
    dolog('config is called')
    config = ConfigParser()
    config.read_dict(get_default_conf())
    return config


def create_of_get_conf(ofile=None, base_dir=None, config_abs=None):
    """
    Returns the configuraation if not present. Otherwise, it will create a default one.
    :param ofile: relative directory of the file e.g. dir1/dir2/my.owl
    :param base_dir:
    :param config_abs:
    :return: dict of the configurations
    """
    global config_folder_name, config_file_name

    if config_abs:
        ofile_config_file_abs = config_abs
    else:
        ofile_config_file_rel = os.path.join(config_folder_name, ofile, config_file_name)
        ofile_config_file_abs = os.path.join(base_dir, ofile_config_file_rel)

    config = get_default_conf_obj()

    if os.path.exists(ofile_config_file_abs):
        dolog("create_of_get_conf> config file exists: %s" % ofile_config_file_abs)
        config.read(ofile_config_file_abs)
        dolog("prev content: ")
        with open(ofile_config_file_abs) as f:
            dolog(f.read())
    else:
        dolog("create_of_get_conf> config file does not exist (will be created): %s" % ofile_config_file_abs)
        build_path(ofile_config_file_abs)
    try:
        with open(ofile_config_file_abs, 'w') as configfile:
            config.write(configfile)
        dolog("post content: ")
        with open(ofile_config_file_abs) as f:
            dolog(f.read())
    except Exception as e:
        dolog('exception: ')
        dolog(e)
        raise e
    return config


######################
#  helper functions  #
######################

def build_path(file_with_abs_dir):
    """
    :param file_with_abs_dir:
    :return: abs_dir as string
    """
    abs_dir = get_parent_path(file_with_abs_dir)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    dolog("build_path abs_dir: " + abs_dir)
    return file_with_abs_dir


def build_path_all(abs_dir):
    """
    build each of the folders in the path. It differs from build_path as it creates all the folders, while build_path
    builds all the folders except for the last one (as it assume the last one is a file).
    :param abs_dir:
    :return:
    """
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    dolog("build_path_all abs_dir: " + abs_dir)


def delete_dir(target_directory):
    dolog("target_directory: ")
    dolog(target_directory)
    comm = "rm -Rf " + target_directory
    dolog(comm)
    call(comm, shell=True)


def get_parent_path(f):
    return '/'.join(f.split('/')[0:-1])


def get_file_from_path(f):
    return f.split('/')[-1]


def get_target_home():
    return 'OnToology'


def call_and_get_log(comm):
    """
    :param comm: The command to be executed via call
    :return: error message, output of the call
    """
    temp_dir = os.environ['github_repos_dir']
    sec = ''.join([random.choice(string.ascii_letters + string.digits)
                   for _ in range(9)])
    fname_output = 'call-output-' + sec
    fname_output = os.path.join(temp_dir, fname_output)
    fname_err = 'call-error-' + sec
    fname_err = os.path.join(temp_dir, fname_err)
    f = open(fname_output, 'w')
    ferr = open(fname_err, 'w')
    call(comm, stdout=f, stderr=ferr, shell=True)
    f.close()
    ferr.close()
    f = open(fname_output, 'r')
    ferr = open(fname_err, 'r')
    file_content = f.read()
    error_content = ferr.read()
    f.close()
    ferr.close()
    os.remove(fname_output)
    os.remove(fname_err)
    return error_content, file_content


# timeout_comm = "timeout 300;"
# disable the timeout for now
timeout_comm = ""
