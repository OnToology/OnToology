import ConfigParser
import os
import random
import string
import io
from subprocess import call

import logging


ontology_formats = ['.rdf', '.owl', '.ttl']
config_folder_name = 'OnToology'
config_file_name = 'OnToology.cfg'
log_file_dir = ''  # need to be set some how

g = None


tools_conf = {
    'ar2dtool': {'folder_name': 'diagrams', 'type': 'png'},
    'widoco': {'folder_name': 'documentation'},
    'oops': {'folder_name': 'evaluation'},
    'owl2jsonld': {'folder_name': 'context'}
}

#
# # currently only user for the previsualization
# def prepare_logger(file_name):
#     home = os.environ['github_repos_dir']
#     sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
#     l = os.path.join(home, 'log', file_name)
#     f = open(l, 'w')
#     f.close()
#     logging.basicConfig(filename=l, format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
#     return l


def dolog_logg(msg):
    logging.critical(msg)


def p(msg):
    print(msg)

dolog = p


def prepare_logger(log_fname):
    logging.basicConfig(filename=log_fname, format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)

# for the outline
# def tools_execution(changed_files, base_dir, logfile, dolog_fname=None, target_repo=None, g_local=None,
#                     change_status=None, repo=None):
#     """
#     :param changed_files:  changed files include relative path
#             base_dir: abs dir to the repo file name, e.g. /home/user/myrepo/
#     :return:
#     """
#     global g
#     global dolog
#     global log_file_dir
#
#     # clean up status pairs for that repo
#     for sp in repo.ontology_status_pairs:
#         sp.delete()
#     repo.ontology_status_pairs = []
#     repo.save()
#     g = g_local
#     log_file_dir = logfile
#     if dolog_fname is not None:
#         prepare_logger(dolog_fname)
#         dolog = dolog_logg
#     repo.notes = ''
#     repo.save()
#     progress_out_of = 70.0
#     if len(changed_files) == 0:
#         repo.progress = progress_out_of
#         repo.save()
#         return
#
#     single_piece = progress_out_of/len(changed_files)
#     progress_inc = single_piece/4.0
#     for f in changed_files:
#         if f[-4:] in ontology_formats:
#             if f[:len('OnToology/')] == 'OnToology/':  # This is to solve bug #265
#                 dolog("nested prevented bug: "+f)
#                 continue
#             dolog("tools_execution: "+f)
#             handle_single_ofile(f, base_dir, target_repo=target_repo, change_status=change_status, repo=repo,
#                                 progress_inc=progress_inc)


def tools_execution(changed_files, base_dir, logfile, dolog_fname=None, target_repo=None, g_local=None,
                    change_status=None, repo=None):
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
    repo.notes = ''
    repo.save()
    progress_out_of = 70.0
    if len(changed_files) == 0:
        repo.progress = progress_out_of
        repo.save()
        return
    single_piece = progress_out_of/len(changed_files)
    progress_inc = single_piece/4.0
    for f in changed_files:
        if f[-4:] in ontology_formats:
            if f[:len('OnToology/')] == 'OnToology/':  # This is to solve bug #265
                dolog("nested prevented bug: "+f)
                continue
            dolog("tools_execution: "+f)
            handle_single_ofile(f, base_dir, target_repo=target_repo, change_status=change_status, repo=repo,
                                progress_inc=progress_inc)


def handle_single_ofile(changed_file, base_dir, target_repo, change_status, repo=None, progress_inc=0.0):
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
    import ar2dtool
    import widoco
    import oops
    import owl2jsonld
    import syntaxchecker
    dolog("will call create or get conf")
    conf = create_of_get_conf(changed_file, base_dir)
    dolog("conf: "+str(conf))
    if not syntaxchecker.valid_syntax(os.path.join(base_dir, changed_file)):
        repo.notes += "syntax error in %s\n" % changed_file
        repo.save()
        return
    if conf['ar2dtool']['enable']:
        dolog("will call draw diagrams")
        change_status(target_repo, 'drawing diagrams for: '+changed_file)
        repo.update_ontology_status(ontology=changed_file, status='diagram')
        repo.save()
        try:
            r = ar2dtool.draw_diagrams([changed_file], base_dir)
            # if r != "":
            #     print 'in init draw detected an error'
            #     # repo.notes += 'Error generating diagrams for %s. ' % changed_file
            #     repo.save()
        except Exception as e:
            dolog("Exception in running ar2dtool.draw_diagrams: "+str(e))
    repo.progress += progress_inc
    repo.save()
    if conf['widoco']['enable']:
        dolog('will call widoco')
        change_status(target_repo, 'generating docs for: '+changed_file)
        repo.update_ontology_status(ontology=changed_file, status='documentation')
        repo.save()
        try:
            r = widoco.generate_widoco_docs([changed_file], base_dir, languages=conf['widoco']['languages'])
            # if r != "":
            #     print 'in init documentation detected an error for ontology file: %s' % changed_file
            #     # repo.notes += 'Error generating documentation for %s. ' % changed_file
            #     repo.save()
        except Exception as e:
            dolog("Exception in running widoco.generate_widoco_docs: "+str(e))
    repo.progress += progress_inc
    repo.save()
    if conf['oops']['enable']:
        dolog('will call oops')
        change_status(target_repo, 'evaluating: '+changed_file)
        repo.update_ontology_status(ontology=changed_file, status='evaluation')
        repo.save()
        try:
            r = oops.oops_ont_files(target_repo=target_repo, changed_files=[changed_file], base_dir=base_dir)
            # if r != "":
            #     print 'in init evaluation detected an error'
            #     # repo.notes += 'Error generating evaluation for %s. ' % changed_file
            #     repo.save()
            if r != "":
                dolog("Error in producing OOPS! report: "+str(r))
                repo.notes += "Error in producing the evaluation report for: %s" % str(changed_file)
                repo.save()
        except Exception as e:
            dolog("Exception in running oops.oops.oops_ont_files: "+str(e))
    repo.progress += progress_inc
    repo.save()
    if conf['owl2jsonld']['enable']:
        dolog('will call owl2jsonld')
        change_status(target_repo, 'generating context for: '+changed_file)
        repo.update_ontology_status(ontology=changed_file, status='jsonld')
        repo.save()
        try:
            owl2jsonld.generate_owl2jsonld_file([changed_file], base_dir=base_dir)
        except Exception as e:
            dolog("Exception in running owl2jsonld.generate_owl2jsonld_file: "+str(e))
    repo.progress += progress_inc
    repo.update_ontology_status(ontology=changed_file, status='finished')
    repo.save()


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
    config = ConfigParser.RawConfigParser()
    # import subprocess
    # subprocess.call('echo "terminal output: "', shell=True)
    # comm = 'cat %s'%ofile_config_file_abs
    # print "comm: "+comm
    # subprocess.call(comm, shell=True)
    # par_file = "/".join(ofile_config_file_abs.split('/')[:-1])
    # comm = "ls %s" % par_file
    # print "comm: "+comm
    # subprocess.call(comm, shell=True)
    conf_file = config.read(ofile_config_file_abs)
    config_result = {
        'widoco': {
            'enable': True,
            'languages': ['en'],
        },
        'ar2dtool': {
            'enable': True
        },
        'oops': {
            'enable': True
        },
        'owl2jsonld': {
            'enable': True
        }
    }
    if len(conf_file) == 1:
        dolog(ofile+' configuration file exists')
        try:
            config_result['ar2dtool']['enable'] = config.getboolean(ar2dtool_sec_name, 'enable')
            dolog('got ar2dtool enable value: ' + str(config_result['ar2dtool']['enable']))
        except:
            dolog('ar2dtool enable value doesnot exist')

        try:
            config_result['widoco']['enable'] = config.getboolean(widoco_sec_name, 'enable')
            config_result['widoco']['languages'] = config.get(widoco_sec_name, 'languages').replace(' ','').replace('"','').replace("'", '').split(',')
            dolog('got widoco enable value: ' + str(config_result['widoco']['enable']))
            dolog('languages: ')
            dolog(config_result['widoco']['languages'])
        except:
            dolog('widoco enable value doesnot exist')

        try:
            config_result['oops']['enable'] = config.getboolean(oops_sec_name, 'enable')
            dolog('got oops enable value: ' + str(config_result['oops']['enable']))
        except:
            dolog('oops enable value doesnot exist')
        try:
            config_result['owl2jsonld']['enable'] = config.getboolean(owl2jsonld_sec_name, 'enable')
            dolog('got owl2jsonld enable value: ' + str(config_result['owl2jsonld']['enable']))
        except:
            dolog('owl2jsonld enable value doesnot exist')
    else:
        dolog(ofile+' configuration file does not exists (not an error)')
        dolog('full path is: '+ofile_config_file_abs)
        for sec in config_result.keys():
            config.add_section(sec)
            for k in config_result[sec].keys():
                if k != 'languages':
                    config.set(sec, k, config_result[sec][k])
        config.set(widoco_sec_name, 'languages', ",".join(config_result[widoco_sec_name]['languages']))
        dolog('will create conf file: ' + ofile_config_file_abs)
        try:
            with open(ofile_config_file_abs, 'wb') as configfile:
                config.write(configfile)
        except Exception as e:
            dolog('exception: ')
            dolog(e)
    return config_result


#######################
# helper functions  ###
#######################

def build_path(file_with_abs_dir):
    """
    :param file_with_abs_dir:
    :return: abs_dir as string
    """
    abs_dir = get_parent_path(file_with_abs_dir)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    dolog("build_path abs_dir: "+abs_dir)  # file_with_abs_dir
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
    dolog("build_path_all abs_dir: "+abs_dir)  # file_with_abs_dir


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


def call_and_get_log(comm):
    """
    :param comm: The command to be executed via call
    :return: error message, output of the call
    """
    temp_dir = os.environ['github_repos_dir']
    sec = ''.join([random.choice(string.ascii_letters + string.digits)
                   for _ in range(9)])
    fname_output = 'call-output-'+sec
    fname_output = os.path.join(temp_dir, fname_output)
    fname_err = 'call-error-'+sec
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

error_msg, output_msg = call_and_get_log(timeout_comm+" echo 'testing timeout command'")
if error_msg.strip() != "":
    timeout_comm = "gtimeout 300;" # for mac os
    error_msg, output_msg = call_and_get_log(timeout_comm+" echo 'testing gtimeout command'")
    if error_msg.strip() != "": # incase timeout and gtimeout are not installed
        timeout_comm = "echo "


