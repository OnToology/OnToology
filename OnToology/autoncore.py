#!/usr/bin/python
#
# Copyright 2012-2013 Ontology Engineering Group, Universidad Politecnica de Madrid, Spain
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @author Ahmad Alobaid

try:
    print("importing OnToology...")
    import OnToology
    print("Success")
except:
    print("Importing djangoperpmode")
    import djangoperpmod
    print("Imported it")

from OnToology import settings
from OnToology import models
from OnToology.models import OUser, Repo, OTask, ORun
from OnToology.models import *
from OnToology import *
from ConfigParserList import ConfigParser
from github import Github
from subprocess import call
import string
import random
import time
import sys
import traceback
import os
import Integrator
import logging
from django.utils import timezone
import urllib.parse

use_database = True

ToolUser = os.environ['github_username']
ToolEmail = os.environ['github_email']

parent_folder = None

publish_dir = os.environ['publish_dir']
home = os.environ['github_repos_dir']  # e.g. home = 'blahblah/temp/'
verification_log_fname = 'verification.log'
sleeping_time = 7
refresh_sleeping_secs = 10  # because github takes time to refresh
ontology_formats = ['.rdf', '.owl', '.ttl']
g = None
log_file_dir = None  # '&1'#which is stdout #sys.stdout#by default
tools_conf = {
    'ar2dtool': {'folder_name': 'diagrams', 'type': 'png'},
    'widoco': {'folder_name': 'documentation'},
    'oops': {'folder_name': 'evaluation'},
    'owl2jsonld': {'folder_name': 'context'}
}

logger = logging.getLogger(__name__)


def set_config(logger, logdir=""):
    """
    :param logger: logger
    :param logdir: the directory log
    :return:
    """
    if logdir != "":
        handler = logging.FileHandler(logdir)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def prepare_logger(user, ext='.log_new'):
    global logger
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
    home_path = os.path.join(home, 'log', user + sec + ext)
    logger = set_config(logger, home_path)
    return home_path


def dolog(msg):
    print("dolog> " + msg)
    logger.critical(msg)


def init_g():
    global g
    username = os.environ['github_username']
    password = os.environ['github_password']
    if settings.DEBUG:
        print("init_g> debug")
        from OnToology.mock import mock_dict
        if 'mock_id' in os.environ and os.environ['mock_id'].strip() != "":
            print("init_g> mock_id in environ: <%s>" % os.environ['mock_id'])
            mock_id = os.environ['mock_id']
            m = mock_dict[mock_id]
            print("init_g>  mock: ")
            print(m.keys())
            g = Github(username, password, mock=m)
        else:
            print("init_g> mock_id is not in environ")
            g = Github(username, password)
    else:
        g = Github(username, password)
        print("init_g> No mock id")
    return g


def magic_prep(target_repo, user, branch):
    """
    To prepare the git magic

    :param target_repo: user/reponame
    :param user: user email
    :param branch: the branch of the changed
    :return: ouser, orun, drepo, otask
    """
    prepare_logger(user)
    if not settings.test_conf['local']:
        prepare_log(user)
    dolog('############################### magic #############################')
    dolog("1> number of users: %d" % len(OUser.objects.all()))
    dolog('target_repo: <%s>' % target_repo)
    dolog("branch: %s" % branch)
    drepo = Repo.objects.get(url=target_repo)
    drepo.state = 'Preparing'
    drepo.save()
    dolog("have the repo now")
    drepo.clear_ontology_status_pairs()
    dolog("cleared")
    dolog("2> number of users: %d" % len(OUser.objects.all()))
    dolog("looking for user: <%s> " % (str(user)))
    ouser = OUser.objects.get(email=user)
    dolog("got the ouser")
    orun = ORun(user=ouser, repo=drepo, branch=branch)
    orun.save()
    dolog("created the orun")
    otask = OTask(name='Preparation', finished=False, success=False, description="", orun=orun)
    dolog("otask is init")
    otask.save()
    dolog("otask is saved")
    otask.description = 'Getting changed files'
    dolog("created the otask")
    dolog("added the task to run")
    return orun, drepo, otask


def fork_and_clone_block(drepo, user, branch, otask, target_repo):
    """
    This is the preparation block before the execution of the tools
    :param drepo: Repo object
    :param user: User object
    :param branch: str. The branch of the repo
    :param otask: OTask obj.

    return g
    """
    # so the tool user can takeover and do stuff
    dolog("pre block")
    g = init_g()
    cloning_url = None
    # in case it is not test or test with fork option
    if not settings.test_conf['local'] or settings.test_conf['fork'] or settings.test_conf['clone']:
        dolog('will fork the repo')
        drepo.state = 'forking repo'
        otask.description += 'fork the repo'
        otask.save()
        forked_repo = fork_repo(target_repo)
        cloning_url = forked_repo.ssh_url
        time.sleep(refresh_sleeping_secs)
        dolog('repo forked: ' + str(cloning_url))
        drepo.progress = 10.0
        drepo.save()
    else:
        print("no fork")
    if not settings.test_conf['local'] or settings.test_conf['clone']:
        drepo.state = 'cloning repo'
        drepo.save()
        otask.description = 'Clone the repo'
        otask.save()
        clone_repo(cloning_url, user, branch=branch)
        dolog('repo cloned')
        drepo.progress = 20.0
    if log_file_dir is None:
        dolog("Prepare the log for the user: %s" % user)
        prepare_log(user)
        dolog("prepared the log")
    dolog("set success")
    otask.success = True
    dolog("save otask")
    otask.save()
    drepo.save()
    return g


def post_block(drepo, orun, changed_filesss, target_repo, branch, raise_exp=False):
    """
    After the execution of the tools
    """
    otask = OTask(name="Postprocessing", description="trying", success=False, finished=False, orun=orun)
    otask.save()
    try:
        otask.description = "verifying changed files"
        otask.save()
        files_to_verify = [c for c in changed_filesss if c[-4:] in ontology_formats]
        for c in changed_filesss:
            if c[:-4] in ontology_formats:
                print("file to verify: " + c)
            else:
                print("c: %s c-4: %s" % (c, c[-4:]))
        otask.description = "preparing the repo after the processing"
        otask.save()
        # After the loop
        dolog("number of files to verify %d" % (len(files_to_verify)))
        if len(files_to_verify) == 0:
            print("files: " + str(files_to_verify))
            drepo.state = 'Ready'
            drepo.notes = ''
            drepo.progress = 100
            drepo.save()
            return
        # if not test or test with push
        if not settings.test_conf['local'] or settings.test_conf['push']:
            dolog("will commit the changed")
            commit_changes()
            dolog('changes committed')
        else:
            dolog('No push for testing')
        otask.description = "Removing old pull requests"
        otask.save()

        otask.description = "Generating pull request"
        otask.save()
        if settings.test_conf['pull']:
            print("pull is true")
        else:
            print("pull is false")
        if not settings.test_conf['local'] or settings.test_conf['pull']:
            drepo.state = 'creating a pull request'
            drepo.save()
            try:
                remove_old_pull_requests(target_repo)
                time.sleep(5)
                r = send_pull_request(target_repo, ToolUser, branch)
                if r['status']:
                    dolog('pull request is sent')
                    drepo.notes = ''
                    drepo.state = 'Ready'
                    drepo.save()
                else:
                    dolog('Error generating the pull request')
                    dolog("Response: %s" % str(r))
                    err_msg = ""
                    if 'error' in r:
                        err_msg = r['error']
                    elif 'errors' in r:
                        err_msgs = [er['message'] for er in r['errors'] if 'message' in er]
                        err_msg = " + ".join(err_msgs)
                    drepo.notes = err_msg
                    drepo.state = 'Ready'
                    drepo.save()
                    raise Exception(err_msg)
            except Exception as e:
                print("3) Exception: " + str(e))
                traceback.print_exc()
                exception_if_exists = str(e)
                err_msg = 'We have not been able to create the pull request. Please contact us to analyze the issue.'
                dolog(err_msg+ exception_if_exists)
                drepo.notes = err_msg
                drepo.progress = 100
                drepo.state = 'Ready'
                drepo.save()
                otask.success = False
                otask.finished = True
                otask.save()
                if raise_exp:
                    raise Exception(str(e))
                return
        else:
            dolog("No pull for testing 11")
            print('No pull for testing 11')
            drepo.state = 'Ready'
            drepo.save()
        drepo.progress = 100
        drepo.save()

        otask.success = True
        otask.save()

    except Exception as e:
        print("4) Exception - generic: " + str(e))
        traceback.print_exc()
        otask.success = False
        otask.description = str(e)
        otask.save()
        otask.finished = True
        otask.save()
        if raise_exp:
            raise Exception(str(e))
    otask.finished = True
    otask.save()
    orun.save()


def git_magic(target_repo, user, changed_filesss, branch, raise_exp=False):
    """
    :param target_repo: user/reponame
    :param user: user email
    :param changed_filesss: list of changed files
    :param branch: the branch of the changed
    :param raise_exp: Whether to raise exception or not in the case of an error
    :return:
    """
    global g
    global parent_folder
    global log_file_dir
    global logger

    print("\n\n\n In gitmagic print")
    print("printing test_conf from magic")
    print(settings.test_conf)
    parent_folder = user

    orun, drepo, otask = magic_prep(target_repo, user, branch)

    try:
        for ftov in changed_filesss:
            if ftov[-4:] in ontology_formats:
                if ftov[:len('OnToology/')] != 'OnToology/':  # This is to solve bug #265
                    dolog("update ontology status")
                    dolog("ontology: " + ftov)
                    drepo.update_ontology_status(ontology=ftov, status='pending')
                    dolog("ontology status is updated")

        g = fork_and_clone_block(drepo, user, branch, otask, target_repo)
    except Exception as e:
        dolog("1) Exception: " + str(e))
        traceback.print_exc()
        otask.success = False
        otask.finished = True
        otask.description = str(e)
        otask.save()
        drepo.state = 'Ready'
        drepo.notes += str(e)
        drepo.progress = 100
        drepo.save()
        if raise_exp:
            raise Exception(str(e))
        return

    otask.finished = True
    otask.save()
    drepo.state = 'Tools'
    drepo.save()

    try:
        Integrator.tools_execution(changed_files=changed_filesss, base_dir=os.path.join(home, user), branch=branch,
                                   target_repo=target_repo, g_local=g, change_status=change_status, repo=drepo,
                                   orun=orun, m_logger=logger, logfile=log_file_dir)
    except Exception as e:
        dolog("2) Exception - tools: " + str(e))
        traceback.print_exc()
        drepo.state = 'Ready'
        drepo.notes += str(e)
        drepo.progress = 100
        drepo.save()
        if raise_exp:
            raise Exception(str(e))
        return

    post_block(drepo, orun, changed_filesss, target_repo, branch, raise_exp)


def update_file(target_repo, path, message, content, branch=None, g_local=None):
    """
    Update the file on GitHub
    :param target_repo:
    :param path:
    :param message:
    :param content:
    :param branch:
    :param g_local:
    :return:
    """
    global g
    if g_local is None:
        gg = init_g()
        print("update_file> get g from init_g")
    else:
        gg = g_local
        print("update_file> g local")
    print("*****\n\n\n\n\n\n\nupdate_file> gg: " + str(gg))
    print("vget user: " + str(gg.get_user()))
    print("\n\n\nupdate_file> *** branch: " + str(branch))
    print("path: " + path)
    clean_path = path
    if path[0] == '/':
        clean_path = clean_path[1:]
    repo = gg.get_repo(target_repo)
    if branch is None:
        sha = repo.get_contents(path).sha
        dolog('update_file> default branch with file sha: %s' % str(sha))
    else:
        print("update_file> get_contents: ")
        cont = repo.get_contents(path, branch)
        print(cont)
        sha = cont.sha
        dolog('branch %s with file %s sha: %s' % (branch, clean_path, str(sha)))

    apath = clean_path.strip()
    # dolog("username: " + username)
    dolog('will update the file <%s> on repo <%s> with the content <%s>,  sha <%s> and message <%s>' %
          (apath, target_repo, content, sha, message))
    dolog("repo.update_file('%s', '%s', \"\"\"%s\"\"\" , '%s' )" % (apath, message, content, sha))
    for i in range(3):
        try:
            if branch is None:
                repo.update_file(apath, message, content, sha)
            else:
                repo.update_file(apath, message, content, sha, branch=branch)
            dolog('file updated')
            return
        except:
            dolog('chance #%d file update' % i)
            time.sleep(3)
    dolog('after x chances, still could not update ')
    # so if there is a problem it will raise an exception which will be captured by the calling function
    repo.update_file(apath, message, content, sha)


def verify_tools_generation(ver_file_comp, repo=None):
    # AR2DTool
    if ver_file_comp['ar2dtool_enable']:
        target_file = os.path.join(get_abs_path(get_target_home()),
                                   ver_file_comp['file'],
                                   tools_conf['ar2dtool']['folder_name'],
                                   Integrator.ar2dtool.ar2dtool_config_types[0][:-5],
                                   get_file_from_path(ver_file_comp['file']) +
                                   "." + tools_conf['ar2dtool']['type'] +
                                   '.graphml')
        file_exists = os.path.isfile(target_file)
        if repo is not None and not file_exists:
            repo.state += ' The Diagram of the file %s is not generated ' % \
                          (ver_file_comp['file'])
            repo.save()
        if settings.test_conf['local']:
            assert file_exists, 'the file %s is not generated' % (target_file)
        elif not file_exists:
            dolog('The Diagram of the file %s is not generated ' %
                  (ver_file_comp['file']))
    # Widoco
    if ver_file_comp['widoco_enable']:
        target_file = os.path.join(get_abs_path(get_target_home()), ver_file_comp['file'],
                                   tools_conf['widoco']['folder_name'],
                                   'index.html')
        file_exists = os.path.isfile(target_file)
        if repo is not None and not file_exists:
            repo.state += ' The Documentation of the file %s if not generated ' % (
                ver_file_comp['file'])
            repo.save()
        if settings.test_conf['local']:
            assert file_exists, 'the file %s is not generated' % (target_file)
        elif not file_exists:
            dolog('The Documentation of the file %s if not generated ' %
                  (ver_file_comp['file']))
    # OOPS
    if ver_file_comp['oops_enable']:
        target_file = os.path.join(get_abs_path(get_target_home()), ver_file_comp['file'],
                                   tools_conf['oops']['folder_name'],
                                   'oopsEval.html')
        file_exists = os.path.isfile(target_file)
        if repo is not None and not file_exists:
            repo.state += ' The Evaluation report of the file %s if not generated ' % (
                ver_file_comp['file'])
            repo.save()
        if settings.test_conf['local']:
            assert file_exists, 'the file %s is not generated' % (target_file)
        elif not file_exists:
            dolog('The Evaluation report of the file %s if not generated ' %
                  (ver_file_comp['file']))
    # owl2jsonld
    if ver_file_comp['owl2jsonld_enable']:
        target_file = os.path.join(get_abs_path(get_target_home()),
                                   ver_file_comp['file'],
                                   tools_conf['owl2jsonld']['folder_name'],
                                   'context.jsonld')
        file_exists = os.path.isfile(target_file)
        if repo is not None and not file_exists:
            repo.state += ' The Context documentation of the file %s if not generated ' % (
                ver_file_comp['file'])
            repo.save()
        if settings.test_conf['local']:
            assert file_exists, 'the file %s is not generated' % (target_file)
        elif not file_exists:
            dolog('The Context documentation of the file %s if not generated ' %
                  (ver_file_comp['file']))

    if 'not generated' in repo.state:
        repo = g.get_repo(repo.url)
        for iss in repo.get_issues():
            if 'OnToology error notification' in iss.title:
                iss.edit(state='closed')
        repo.create_issue('OnToology error notification', repo.state)


def get_ontologies_from_a_submodule(path, url):
    """
    :param path: local path within the repository
    :param url: url of the repository
    :return: list of detected ontologies
    """
    global g
    ontologies = []
    print("get_ontologies_from_a_submodule: path=%s and url=%s" % (path, url))
    try:
        target_repo = ("/".join(url.split('/')[-2:])).strip()[:-4]
        repo = g.get_repo(target_repo)
        sha = repo.get_commits()[0].sha
        files = repo.get_git_tree(sha=sha, recursive=True).tree
        ontoology_home_name = 'OnToology'
        for f in files:
            if f.path[:len(ontoology_home_name)] != ontoology_home_name:
                if f.type == 'blob':
                    for ontfot in ontology_formats:
                        if f.path[-len(ontfot):] == ontfot:
                            print("get_ontologies_from_a_submodule f.path: %s" % f.path)
                            ontologies.append(os.path.join(path, f.path))
                            break
    except Exception as e:
        print("get_ontologies_from_a_submodule exception: " + str(e))
    return ontologies


def get_ontologies_from_submodules_tree(tree, repo):
    """
    :param tree: a github tree
    :param repo: a repo object from GitHub
    :return: a list of detected ontologies
    """
    ontologies = []
    submodule_tree_elements = [f for f in tree if f.path == '.gitmodules']
    if len(submodule_tree_elements) == 1:
        config_parser = ConfigParser()
        subm_tree_ele = submodule_tree_elements[0]
        print("tree ele: ")
        print(subm_tree_ele)
        print("path: ")
        print(subm_tree_ele.path)
        file_content = repo.get_contents(subm_tree_ele.path).decoded_content
        print("file_content")
        file_content = file_content.decode('utf-8')
        print(file_content)

        file_content = file_content.replace('\t', '')  # because it was containing \t
        config_parser.read_string(file_content)
        sections = config_parser.sections()
        for sec in sections:
            p = config_parser.get(sec, "path")
            u = config_parser.get(sec, "url")
            ontologies += get_ontologies_from_a_submodule(path=p, url=u)
    return ontologies


def get_ontologies_in_online_repo(target_repo):
    global g
    ontologies = []
    try:
        g = init_g()
        print("asking for repo: <%s>" % target_repo)
        repo = g.get_repo(target_repo)
        print("asking for commits")
        sha = repo.get_commits()[0].sha
        print("asking for files")
        files = repo.get_git_tree(sha=sha, recursive=True).tree
        ontoology_home_name = 'OnToology'

        for f in files:
            if f.path[:len(ontoology_home_name)] != ontoology_home_name:
                if f.type == 'blob':
                    for ontfot in ontology_formats:
                        if f.path[-len(ontfot):] == ontfot:
                            ontologies.append(f.path)
                            break
        ontologies += get_ontologies_from_submodules_tree(files, repo)
    except Exception as e:
        print("get_ontologies_in_online_repo exception: " + str(e))
        traceback.print_exc()
    return ontologies


def prepare_log(user):
    global log_file_dir
    global default_stderr
    global default_stdout
    file_dir = build_file_structure(user + '.log', 'log', home)
    f = open(file_dir, 'w')
    log_file_dir = file_dir
    return f


def is_organization(target_repo):
    return g.get_repo(target_repo).organization is not None


def has_access_to_repo(target_repo):
    global g
    user_id = g.get_user().id
    if is_organization(target_repo):
        try:
            collaborators = g.get_repo(target_repo).get_collaborators()
            for coll in collaborators:
                if user_id == coll.id:
                    return True
            return False
        except:
            return False
    return True


def delete_repo(local_repo):
    global g
    if g is None:
        init_g()
    try:
        g.get_repo(local_repo).delete()
        dolog('repo deleted ')
    except:
        dolog('the repo doesn\'t exists [not an error]')


def fork_repo(target_repo):
    """
    :param target_repo: username/reponame
    :return: forked repo (e.g. OnToologyUser/reponame)
    """
    # the wait time to give github sometime so the repo can be forked successfully
    # time.sleep(sleeping_time)
    gg = init_g()
    repo = gg.get_repo(target_repo)
    user = gg.get_user()
    dolog("To fork repo: " + target_repo)
    try:
        gg.get_repo("%s/%s" % (user.name, repo.name)).delete()
        dolog("deleted %s/%s" % (user.name, repo.name))
    except:
        dolog("did not delete %s/%s" % (user.name, repo.name))
    for i in range(1, 3):
        try:
            gg.get_repo("%s/%s-%d" % (user.name, repo.name, i)).delete()
            dolog("deleted %s/%s-%d" % (user.name, repo.name, i))
        except:
            dolog("did not delete %s/%s-%d" % (user.name, repo.name, i))
    time.sleep(sleeping_time)
    forked_repo = user.create_fork(repo)
    dolog("forked repo")
    dolog('forked to: ' + forked_repo.name)
    return forked_repo


def clone_repo(cloning_url, parent_folder, dosleep=True, branch=None):
    """
    :param cloning_url:
    :param parent_folder: just the name of the new direct folder name to be created if it does not exists
    :param dosleep:
    :param branch:
    :return: the abs path
    """
    if branch is None:
        raise Exception("clone_repo> branch is not passed")
    global g
    if g is None:
        init_g()
    dolog('home: %s' % (home))
    dolog('parent_folder: %s' % (parent_folder))
    if dosleep:
        # the wait time to give github sometime so the repo can be cloned
        time.sleep(sleeping_time)
    try:
        comm = "rm" + " -Rf " + os.path.join(home, parent_folder)
        dolog(comm)
        call(comm, shell=True)
    except Exception as e:
        dolog('rm failed: ' + str(e))
    comm = "git clone " + "--single-branch --branch " + branch + " --recurse-submodules  " + cloning_url + " " + os.path.join(
        home, parent_folder)
    dolog(comm)
    call(comm, shell=True)
    return os.path.join(home, parent_folder)


def commit_changes():
    global g
    if g is None:
        init_g()
    gu = 'git config  user.email "%s" ; ' % ToolEmail
    gu += 'git config  user.name "%s" ;' % (ToolUser)
    comm = "cd " + os.path.join(home, parent_folder) + ";" + gu + " git add . "
    if not settings.test_conf['local']:
        comm += ' >> "' + log_file_dir + '"'
    dolog(comm)
    if settings.test_conf['push'] or not settings.test_conf['local']:
        call(comm, shell=True)

    comm = "cd " + os.path.join(home, parent_folder) + ";" + \
           gu + " git commit -m 'automated change' "
    if not settings.test_conf['local']:
        comm += ' >> "' + log_file_dir + '"'
    dolog(comm)
    if settings.test_conf['push'] or not settings.test_conf['local']:
        call(comm, shell=True)
    gup = "git config push.default matching;"
    # comm = "cd " + home + parent_folder + ";" + gu + gup + " git push "
    comm = "cd " + os.path.join(home, parent_folder) + ";" + gu + gup + " git push "
    if not settings.test_conf['local']:
        comm += ' >> "' + log_file_dir + '"'
    dolog(comm)
    if settings.test_conf['push'] or not settings.test_conf['local']:
        call(comm, shell=True)


def refresh_repo(target_repo):
    global g
    if g is None:
        init_g()
    local_repo = target_repo.split('/')[-1]
    g.get_user().get_repo(local_repo).delete()
    g.get_user().create_fork(target_repo)


def remove_old_pull_requests(target_repo):
    global g
    if g is None:
        init_g()
    title = 'OnToology update'
    for p in g.get_repo(target_repo).get_pulls():
        try:
            if p.title == title:
                p.edit(state="closed")
        except Exception as e:
            print("Exception removing an old pull request: " + str(e))
            dolog("Exception removing an old pull request: " + str(e))


def send_pull_request(target_repo, username, branch):
    title = 'OnToology update'
    body = title
    err = ""
    time.sleep(sleeping_time)
    repo = g.get_repo(target_repo)
    try:
        repo.create_pull(head=username + ':%s' % branch, base='%s' % branch, title=title, body=body)
        return {'status': True, 'msg': 'pull request created successfully'}
    except Exception as e:
        err = str(e)
        dolog('pull request error: ' + err)
        if 'No commits between' in err:
            dolog('pull request detecting no commits')
            r = Repo.objects.get(url=target_repo)
            r.notes = 'No difference to generate the pull request, make a change in the repo so the pull request can be generated.'
            r.save()
    return {'status': False, 'error': err}


def webhook_access(client_id, redirect_url, isprivate):
    if isprivate:
        scope = 'repo'
    else:
        scope = 'public_repo'
    sec = ''.join([random.choice(string.ascii_letters + string.digits)
                   for _ in range(9)])
    return "https://github.com/login/oauth/authorize?client_id=" + client_id + "&redirect_uri=" + \
           redirect_url + "&scope=" + scope + "&state=" + sec, sec


def get_user_github_email(username):
    try:
        return g.get_user(username).email
    except:
        return None


def remove_webhook(target_repo, notification_url):
    global g
    if g is None:
        init_g()
    # for some reason adding the below two prints solves the problem for removing the webhook, strange but true
    print("target_repo: " + str(target_repo))
    print("notification url: " + str(notification_url))
    for hook in g.get_repo(target_repo).get_hooks():
        try:
            if hook.config["url"] == notification_url:
                hook.delete()
                break
        except Exception as e:
            print("error removing the webhook: %s" % (str(e)))
            time.sleep(2)
    sys.stdout.flush()
    sys.stderr.flush()


def add_webhook(target_repo, notification_url, newg=None):
    global g
    if newg is None:
        if g is None:
            init_g()
        newg = g
    name = "web"
    active = True
    events = ["push"]
    config = {
        "url": notification_url,
        "content_type": "form"
    }
    try:
        newg.get_repo(target_repo).create_hook(name, config, events, active)
        return {'status': True}
    except Exception as e:
        return {'status': False, 'error': str(e)}


def add_collaborator(target_repo, user, newg=None):
    global g
    if newg is None:
        if g is None:
            g = init_g()
        newg = g
    try:
        print("in try")
        u = newg.get_user()
        print(u)
        print("user name: " + str(u.name))
        print("email: " + str(u.email))
        print("adding collaborator from user: %s " % str(newg.get_user().name))
        print("goring for the first")
        if u.name is None or u.email is None:
            print("no email or name")
            return {'status': False, 'error': 'Make sure you have your name and email public and not empty on GitHub'}
        if newg.get_repo(target_repo).has_in_collaborators(user):
            print("collaborator already there")
            return {'status': True, 'msg': 'this user is already a collaborator'}
        else:
            print("going to collaborator\n\n")
            invitation = newg.get_repo(target_repo).add_to_collaborators(user)
            print("got a reply")
            print(invitation)
            if invitation is None:
                print("no invitation is created")
                return {'status': False, 'error': 'Invitation is not generated'}
            else:
                print("invitation exists")
                try:
                    g = init_g()
                    print("try to accept invitation (new g)")
                    print("accepting user: %s" % str(g.get_user().name))
                    g.get_user().accept_invitation(invitation)
                    print("invitation accepted: " + str(invitation))
                    return {'status': True, 'msg': 'added as a new collaborator'}
                except Exception as e:
                    print("exception: " + str(e))
                    print("invitation not accepted or invalid: " + str(invitation))
                    traceback.print_exc()
                    return {'status': False, 'error': 'Could not accept the invitation for becoming a collaborator'}
    except Exception as e:
        print("add_collaborator> Exception: " + str(e))
        traceback.print_exc()
        return {'status': False, 'error': str(e)}  # e.data}


def previsual(useremail, target_repo, branch):
    """
    :param useremail: email of the repo owner
    :param target_repo: owner/reponame
    :param branch: e.g., master
    :return: error, orun
    """
    from Integrator.previsual import start_previsual
    prepare_logger(useremail + "-prev-")
    dolog("starting previsual function with ontology: %s" % target_repo)
    orun = None
    otask = None
    try:
        dolog("previsual> trying the previsual")
        users = OUser.objects.filter(email=useremail)
        if len(users) != 1:
            error_msg = "%s is invalid email" % useremail
            dolog("previsual> " + error_msg)
            return error_msg, None
        user = users[0]
        repos = Repo.objects.filter(ousers=user, url=target_repo)

        if len(repos) > 0:
            repo = repos[0]
            orun = ORun(user=user, repo=repo, branch=branch)
            orun.save()
            dolog("previsual> created the orun")
            otask = OTask(name='Cloning the repo', finished=False, success=False,
                          description="prepaaring the previsualization", orun=orun)
            dolog("previsual> otask is init")
            otask.save()

            dolog("previsual> repo is found and now generating previsualization")
            repo.state = 'Generating Previsualization'
            repo.notes = ''
            # repo.previsual_page_available = True
            repo.save()
            # prepare_log(user.email)
            # cloning_repo should look like 'git@github.com:AutonUser/target.git'
            cloning_repo = 'git@github.com:%s.git' % target_repo
            sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
            folder_name = 'prevclone-' + sec

            if not settings.test_conf['local'] or settings.test_conf['clone']:
                otask.description = "Cloning the repo"
                otask.save()
                clone_repo(cloning_repo, folder_name, dosleep=True, branch=branch)
                otask.description = "Cloning is complete"
                otask.save()

            else:
                otask.description = "Skip cloning"
                otask.save()
            otask.success = True
            otask.finished = True
            otask.save()
            otask = OTask(name='Previsualization', finished=False, success=False,
                          description="preparing the previsualization", orun=orun)
            otask.save()
            repo_dir = os.path.join(home, folder_name)
            dolog("previsual> will call start previsual")
            otask.description = "Generating the previsualization"
            otask.save()
            msg = start_previsual(repo_dir, target_repo)
            if msg == "":  # no errors
                dolog("previsual> completed successfully")
                otask.description = "The previsualization is generated without errors"
                otask.success = True
                otask.finished = True
                otask.save()
                repo.state = 'Ready'
                repo.save()
                dolog("previsual> test state: %s" % repo.state)
                return "", orun
            else:
                repo.notes = msg
                repo.state = 'Ready'
                repo.save()
                otask.description = "Error generating the previsualization: " + msg
                otask.success = False
                otask.finished = True
                otask.save()
                return msg, orun
        else:  # not found
            error_msg = 'You should add the repo while you are logged in before the revisual renewal'
            dolog("previsual> " + error_msg)
            return error_msg, None
    except Exception as e:
        dolog("autoncore.previsual exception: <%s>" % str(e))
        dolog(traceback.format_exc())
        if otask is not None:
            otask.description = "Exception generating the previsualization: " + str(e)
            otask.success = False
            otask.finished = True
        return str(e), orun


def update_g(token):
    global g
    g = Github(token)


def get_file_content(target_repo, path, branch=None):
    username = os.environ['github_username']
    password = os.environ['github_password']
    g = Github(username, password)
    repo = g.get_repo(target_repo)
    if branch is None:
        return repo.get_contents(path).decoded_content
    else:
        return repo.get_contents(path, branch).decoded_content


def bundle_file_handler(repo, f, ontology_bundle, base_dir):
    """
    Generate Bundle
    :param repo: repo object
    :param f: file github
    :param ontology_bundle:
    :param base_dir:
    """
    fpath = None
    try:
        for _ in range(3):
            try:
                fpath = f.path
                print("generate_bundle> %s" % fpath)
                break
            except Exception as e:
                time.sleep(2)
                print("generate_bundle> Exception " + str(e))
                traceback.print_exc()
        if not fpath:
            fpath = f.path
        p = fpath
        if fpath[0] == '/':
            p = fpath[1:]
        abs_path = os.path.join(base_dir, p)
        if p[:len(ontology_bundle)] == ontology_bundle:
            print('true: ' + str(p))
            if f.type == 'tree':
                os.makedirs(abs_path)
            elif f.type == 'blob':
                parent_folder = os.path.join(*abs_path.split('/')[:-1])
                if parent_folder != base_dir:  # not in the top level of the repo
                    if not os.path.exists(parent_folder):
                        os.makedirs(parent_folder)
                with open(abs_path, 'wb') as fii:
                    file_content = repo.get_contents(fpath).decoded_content
                    fii.write(file_content)
                    print("file %s" % str(f.path))
            else:
                print('unknown type in generate bundle')
        else:
            pass
    except Exception as e:
        print('generate_bundle> Exception3: ' + str(e))
        traceback.print_exc()


def generate_bundle(base_dir, target_repo, ontology_bundle, branch):
    """
    :param base_dir: e.g. /home/user/temp/random-folder-xyz
    :param target_repo:  user/reponame
    :param ontology_bundle: OnToology/abc/alo.owl
    :param branch: e.g., master
    :return: the bundle zip file dir if successful, or None otherwise
    """
    global g
    if g is None:
        init_g()
    try:
        print('ontology bundle: ' + ontology_bundle)
        repo = g.get_repo(target_repo)
        branch = repo.get_branch(branch)
        sha = branch.commit.sha
        files = repo.get_git_tree(sha=sha, recursive=True).tree
        print('num of files: ' + str(len(files)))
        for f in files:
            bundle_file_handler(repo, f, ontology_bundle, base_dir)

        zip_file = os.path.join(base_dir, '%s.zip' % ontology_bundle.split('/')[-1])
        comm = "cd %s; zip -r '%s' OnToology" % (base_dir, zip_file)
        print('comm: %s' % comm)
        call(comm, shell=True)
        return os.path.join(base_dir, zip_file)
    except Exception as e:
        print('generate_bundle> Exception3: ' + str(e))
        traceback.print_exc()
        return None


def filter_pub_name(name):
    name = ''.join(ch for ch in name if ch.isalnum() or ch in ['_', '-'])
    return name


def publish(name, target_repo, ontology_rel_path, useremail, branch, orun, g_local=None):
    """
    To publish the ontology via github.
    :param name:
    :param target_repo:
    :param ontology_rel_path:
    :param useremail:
    :param branch:
    :param orun:
    :param g_local:
    :return: error message, it will return an empty string if everything went ok
    """
    global g
    if g_local is None:
        if g is None:
            g = init_g()
        gg = g
    else:
        gg = g_local
    try:
        OUser.objects.all()
    except:
        django_setup_script()
    from OnToology.models import OUser, PublishName, Repo

    try:
        user = OUser.objects.get(email=useremail)
        dolog("publish> user is found")
    except Exception as e:
        error_msg = "user is not found"
        dolog("publish> error: %s" % str(e))
        return error_msg
    prepare_logger(useremail + "-publish-")

    repos = Repo.objects.filter(url=target_repo)
    if len(repos) == 0:
        error_msg = "The repository: <" + target_repo + "> is not found"
        dolog("publish>" + error_msg)
        return error_msg

    repo = repos[0]
    otask = OTask(name='Name Reservation', finished=False, success=False, description="Look for published names",
                  orun=orun)
    dolog("publish> otask is init")
    otask.save()

    ontology = ontology_rel_path
    if ontology[0] == '/':
        ontology = ontology[1:]
    if ontology[-1] == '/':
        ontology = ontology[:-1]
    ontology = "/" + ontology
    name = name.strip()
    name = filter_pub_name(name)
    pns_name = PublishName.objects.filter(name=name)
    if len(pns_name) > 1:
        error_msg = 'a duplicate published names, please contact us ASAP to fix it'
        dolog("publish> " + error_msg)
        otask.success = False
        otask.finished = True
        otask.description = error_msg
        otask.save()
        return error_msg

    print("ontology: " + ontology)
    print("repo: " + repo.url)
    print("user: " + user.email)
    pns_ontology = PublishName.objects.filter(user=user, ontology=ontology, repo=repo)

    otask.description = "Verify ontology publication"
    otask.save()

    if len(pns_ontology) == 0 and name.strip() == '':
        error_msg = 'can not reserve an empty name'
        dolog('publish> ' + error_msg)
        otask.success = False
        otask.finished = True
        otask.description = error_msg
        otask.save()
        return error_msg
    elif len(pns_ontology) > 0 and name.strip() != '':  # If the ontology is published with another name
        error_msg = 'can not reserve multiple names for the same ontology'
        dolog("publish> " + error_msg)
        otask.success = False
        otask.finished = True
        otask.description = error_msg
        otask.save()
        return error_msg

    # If the publication name is taken
    if len(pns_name) == 1 and len(pns_ontology) == 0:
        error_msg = "This name is already taken, please choose a different one"
        dolog("publish> " + error_msg)
        otask.success = False
        otask.finished = True
        otask.description = error_msg
        otask.save()
        return error_msg

    otask.success = True
    otask.finished = True
    otask.description = "Name reservation has been validated"
    otask.save()
    otask = OTask(name='.htaccess Preparation', finished=False, success=False, description="Get .htaccess",
                  orun=orun)
    dolog("publish> otask is init .htaccess Preparation")
    otask.save()

    # new name and ontology is not published or republish
    if (len(pns_name) == 0 and len(pns_ontology) == 0) or (name == ''):
        rel_htaccess_path = os.path.join('OnToology', ontology[1:], 'documentation/.htaccess')
        try:
            htaccess = get_file_content(target_repo=target_repo, path=rel_htaccess_path, branch=branch)
            otask.description = ".htaccess content is fetched successfully"
            otask.save()
            dolog("publish> gotten the htaccess successfully")
        except Exception as e:
            if '404' in str(e):
                error_msg = """documentation of the ontology has to be generated first (%s)""" % rel_htaccess_path
                dolog("publish> " + error_msg)
                otask.success = False
                otask.finished = True
                otask.description = error_msg
                otask.save()
                return error_msg
            else:
                error_msg = "github error: %s" % str(e)
                dolog("publish> " + error_msg)
                otask.success = False
                otask.finished = True
                otask.description = error_msg
                otask.save()
                return error_msg
        dolog("publish> htaccess content: ")
        if isinstance(htaccess, bytes):
            htaccess = htaccess.decode('utf-8')
        #dolog(str(type(htaccess)))
        otask.description = "rewriting .htaccess with redirects to GitHub"
        otask.save()
        new_htaccess = htaccess_github_rewrite(target_repo=target_repo, htaccess_content=htaccess,
                                               ontology_rel_path=ontology[1:])
        dolog("new htaccess is generated")
        otask.description = "updating the .htaccess on GitHub"
        otask.save()
        update_file(target_repo=target_repo,
                    path=rel_htaccess_path,
                    content=new_htaccess, branch='gh-pages', message='OnToology Publish', g_local=gg)

        otask.success = True
        otask.finished = True
        otask.description = "The .htaccess is updated successfully"
        otask.save()
        otask = OTask(name='Redirection', finished=False, success=False,
                      description="setup the .htaccess file on OnToogy server", orun=orun)
        dolog("publish> otask is init. Redirection")
        otask.save()

        dolog(f"publish> name: <{name}>")

        if name != "": # new reserved name
            comm = 'mkdir -p "%s"' % os.path.join(publish_dir, name)
            dolog("publish> " + comm)
            call(comm, shell=True)
        else:
            dolog("publish> republish")

        otask.description = "writing the new .htaccess on OnToology server"
        otask.save()

        if name == "": # republish case
            publication_folder_name = pns_ontology[0].name
        else: # new name
            publication_folder_name = name

        f = open(os.path.join(publish_dir, publication_folder_name, '.htaccess'), 'w')
        f.write(new_htaccess)
        f.close()
        if name != '':
            otask.description = "Reserving the new w3id name"
            otask.save()
            p = PublishName(name=name, user=user, repo=repo, ontology=ontology)
            p.save()

        dolog("publish> published correctly")
        otask.success = True
        otask.finished = True
        otask.description = "The ontology is published correctly"
        otask.save()

        return ""  # means it is published correctly


def change_configuration(user_email, target_repo, data, ontologies):
    """
    :param user_email:
    :param target_repo:
    :param data:
    :param ontologies:
    :return:
    """
    otask = True  # This is assigned true here in case the exception code is reached
    try:
        users = OUser.objects.filter(email=user_email)
        repos = Repo.objects.filter(url=target_repo)
        if len(repos) == 1:
            repo = repos[0]
        else:
            dolog("change_configuration> Invalid repo: " + target_repo)
            raise Exception("Invalid repo: " + target_repo)
        if len(users) == 1:
            user = users[0]
        else:
            dolog("change_configuration> Invalid email: " + user_email)
            raise Exception("Invalid email: " + user_email)

        orun = ORun(user=user, repo=repo)
        orun.save()
        otask = OTask(name="Change Configuration", description="changing the configuration", orun=orun)
        otask.save()
        for onto in ontologies:
            dolog('inside the loop')
            ar2dtool = onto + '-ar2dtool' in data
            widoco = onto + '-widoco' in data
            oops = onto + '-oops' in data
            dolog('will call get_conf')
            otask.description = 'Get new configuration for the ontology: ' + onto
            otask.save()
            new_conf = get_conf(ar2dtool, widoco, oops)
            dolog('will call update_file')
            o = 'OnToology' + onto + '/OnToology.cfg'
            try:
                dolog("target_repo <%s> ,  path <%s> ,  message <%s> ,   content <%s>" % (
                    target_repo, o, 'OnToology Configuration', new_conf))
                otask.description = 'Update the configuration for the ontology: ' + onto
                otask.save()
                update_file(target_repo, o, 'OnToology Configuration', new_conf)
                dolog('configuration is changed for file for ontology: ' + onto)
                otask.description = 'The task is completed successfully'
                otask.success = True
                otask.save()
            except Exception as e:
                dolog('Error in updating the configuration: ' + str(e))
                otask.description = 'Error in updating the configuration: ' + str(e)
                otask.success = False
                otask.save()
                break
        otask.finished = True
        otask.save()
    except Exception as e:
        err = "Error in change_configuration"
        print(err)
        dolog(err)
        err = str(e)
        print(err)
        dolog(err)
        if otask:
            otask.finished = True
            otask.success = False
            otask.description = str(e)
            otask.save()


#############################
# Auton configuration file  #
#############################


def get_conf(ar2dtool, widoco, oops):
    conf = """
[ar2dtool]
enable = %s

[widoco]
enable = %s

[oops]
enable = %s
    """ % (str(ar2dtool), str(widoco), str(oops))
    return conf


def get_confs_from_repo(target_repo, branch):
    global g
    repo = g.get_repo(target_repo)
    branch = repo.get_branch(branch)
    sha = branch.commit.sha
    files = repo.get_git_tree(sha=sha, recursive=True).tree
    conf_files = []
    for f in files:
        if 'OnToology.cfg' in f.path:
            conf_files.append(f)
    return repo, conf_files


def add_themis_results(target_repo, branch, ontologies):
    """
      get all themis results from a given repo,
      then, cross-reference them with the ontologies list,
      finally, add the themis results to the ontologies list
    :param target_repo:
    :param branch:
    :param ontologies: a list of dicts of ontologies and tools
    :return: list of pairs of the form (ontology path in the repo, themis results path in the repo)
    """
    global g
    repo = g.get_repo(target_repo)
    branch = repo.get_branch(branch)
    sha = branch.commit.sha
    files = repo.get_git_tree(sha=sha, recursive=True).tree
    ontology_results_d = dict()
    themis_results_dir = "/" + Integrator.tools_conf['themis']['folder_name']
    themis_results_dir += "/" + Integrator.tools_conf['themis']['results_file_name']

    start_subs = get_target_home() + "/"
    end_subs = themis_results_dir
    for f in files:
        if f.path.startswith(start_subs) and f.path.endswith(end_subs):
            ontology_results_d["/" + f.path[len(start_subs):-len(end_subs)]] = f.path

    for o in ontologies:
        if o['ontology'] in ontology_results_d:
            o['themis_results'] = compute_themis_results(repo, branch.name, ontology_results_d[o['ontology']])
    return ontologies


def compute_themis_results(repo, branch, path):
    """
    :param repo:
    :param branch:
    :param path:
    :return: score (0-100)
    """
    p = path
    print("get file content: %s" % (str(path)))
    print("after quote: %s" % p)
    print("now get the decoded content")
    file_content = repo.get_contents(p, ref=branch).decoded_content
    file_content = file_content.decode('utf-8')

    passed = 0
    failed = 0
    for line in file_content.split('\n'):
        line = line.strip()
        if line == "":
            continue
        else:
            print("line: <%s> " % line)
            comp = line.split('\t')
            print(comp)
            if comp[1].strip().lower() == "passed":
                passed += 1
            else:
                failed += 1
    if passed + failed == 0:
        return 0
    return round(passed * 100 / (passed + failed))


# This seems correct but no longer needed at the moment
# def get_themis_results(target_repo):
#     """
#       get all themis results from a given repo
#     :param target_repo:
#     :return: list of pairs of the form (ontology path in the repo, themis results path in the repo)
#     """
#     global g
#     repo = g.get_repo(target_repo)
#     sha = repo.get_commits()[0].sha
#     files = repo.get_git_tree(sha=sha, recursive=True).tree
#     pairs = []  # of ontology_rel_dir, results_path
#     themis_results_dir = "/"+Integrator.tools_conf['themis']['folder_name'] + "/" + \
#                          Integrator.tools_conf['themis']['results_file_name']
#     for f in files:
#         if f.path[:10] == get_target_home()+"/" and f.path[-23:] == themis_results_dir:
#             p = (f.path[10:-23], f.path)
#             pairs.append(p)
#     return pairs


def parse_online_repo_for_ontologies(target_repo, branch='master'):
    """
        This is parse repositories for ontologies configuration files OnToology.cfg
    """
    global g
    if g is None:
        init_g()
    print("in parse online repo for ontologies")
    repo, conf_paths = get_confs_from_repo(target_repo, branch)
    print("repo: %s, conf_paths: %s" % (str(repo), str(conf_paths)))
    ontologies = []

    for cpath in conf_paths:
        p = cpath.path
        print("get file content: %s" % (str(cpath.path)))
        print("after quote: %s" % p)
        print("now get the decoded content")
        file_content = repo.get_contents(p).decoded_content
        print("type: " + str(type(file_content)))
        file_content = file_content.decode('utf-8')
        print("file_content: " + file_content)
        print("will get the config")
        conf = get_auton_config(file_content, from_string=True)
        conf_str = Integrator.get_conf_as_str(conf)
        print("gotten confs: " + conf_str)
        o = dict()
        o['ontology'] = get_parent_path(p)[len(get_target_home()):]
        for tool in conf.sections():
            o[tool] = Integrator.get_conf_tool_json(conf, tool)
            print("parse_online_repo_for_ontologies> ")
            print("Themis debug: ")
            print("tool: %s" % tool)
            print(type(o[tool]))
            print(o[tool])
        ontologies.append(o)

    return ontologies


def get_auton_configuration(f=None, abs_folder=None):
    if abs_folder is not None:
        conf_file_abs = os.path.join(abs_folder, 'OnToology.cfg')
    elif f is not None:
        conf_file_abs = build_file_structure(
            'OnToology.cfg', [get_target_home(), f])
    else:
        conf_file_abs = build_file_structure(
            'OnToology.cfg', [get_target_home()])
    return get_auton_config(conf_file_abs, from_string=False)


def get_auton_config(conf_file_abs, from_string=True):
    """
    :param conf_file_abs:
    :param from_string:
    :return: config obj
    """

    if from_string:
        config = Integrator.get_default_conf_obj()
        config.read_string(conf_file_abs)
        print("obj from string")
    else:
        config = Integrator.create_of_get_conf(config_abs=conf_file_abs)
        config.read(conf_file_abs)
        print("obj from file")
        try:
            with open(conf_file_abs, 'wb') as configfile:
                config.write(configfile)
        except Exception as e:
            dolog('expection: ' + str(e))
            traceback.print_exc()

    dolog("\n\n***get_auton_config***")
    conf_str = Integrator.get_conf_as_str(config)
    print("Type")
    print(type(conf_str))
    print(conf_str)
    dolog(conf_str)
    return config


def htaccess_github_rewrite(htaccess_content, target_repo, ontology_rel_path):
    """
    :param htaccess_content:
    :param target_repo: username/reponame
    :param ontology_rel_path: without leading or trailing /
    :return: htaccess with github rewrite as the domain
    """
    rewrites = [
        "RewriteRule ^$ index-de.html [R=303, L]",
        "RewriteRule ^$ index-pt.html [R=303, L]",
        "RewriteRule ^$ index-it.html [R=303, L]",
        "RewriteRule ^$ index-es.html [R=303, L]",
        "RewriteRule ^$ index-en.html [R=303, L]",
        "RewriteRule ^$ ontology.n3 [R=303, L]",
        "RewriteRule ^$ ontology.xml [R=303, L]",
        "RewriteRule ^$ ontology.ttl [R=303, L]",
        "RewriteRule ^$ 406.html [R=406, L]",
        "RewriteRule ^$ ontology.json [R=303, L]",
        "RewriteRule ^$ ontology.nt [R=303, L]",

        "RewriteRule ^$ index-de.html [R=303,L]",
        "RewriteRule ^$ index-pt.html [R=303,L]",
        "RewriteRule ^$ index-it.html [R=303,L]",
        "RewriteRule ^$ index-es.html [R=303,L]",
        "RewriteRule ^$ index-en.html [R=303,L]",
        "RewriteRule ^$ ontology.n3 [R=303,L]",
        "RewriteRule ^$ ontology.xml [R=303,L]",
        "RewriteRule ^$ ontology.ttl [R=303,L]",
        "RewriteRule ^$ 406.html [R=406,L]",
        "RewriteRule ^$ ontology.json [R=303,L]",
        "RewriteRule ^$ ontology.nt [R=303,L]"

    ]
    user_username = target_repo.split('/')[0]
    repo_name = target_repo.split('/')[1]
    base_url = "https://%s.github.io/%s/OnToology/%s/documentation/" % (user_username, repo_name, ontology_rel_path)
    base_url = urllib.parse.quote(base_url)
    new_htaccess = ""

    for line in htaccess_content.split('\n'):
        # for slash-based ontologies
        if line.strip() in rewrites:
            rewr_rule = line.split(' ')
            rewr_rule[2] = base_url + rewr_rule[2]
            new_htaccess += " ".join(rewr_rule) + "\n"
        # for hash-based ontologies
        elif "RewriteRule" in line and "^def" in line:
            rewr_rule = line.split(' ')
            rewr_rule[2] = base_url + rewr_rule[2]
            new_htaccess += "RewriteRule ^$ "
            new_htaccess += " ".join(rewr_rule[2:]) + "\n"
        else:
            if "RewriteRule" in line:
                print("NOTIN: " + line)
            new_htaccess += line + "\n"
    return new_htaccess


############################
# generic helper functions #
############################


def delete_dir(target_directory):
    comm = "rm -Rf " + target_directory
    if not settings.test_conf['local']:
        comm += '  >> "' + log_file_dir + '" '
    print(comm)
    call(comm, shell=True)


def valid_ont_file(r):
    if r[-4:] in ontology_formats:
        return True
    return False


def get_target_home():
    return 'OnToology'


def get_abs_path(relative_path):
    return os.path.join(home, parent_folder, relative_path)


def get_level_up(relative_path):
    fi = get_file_from_path(relative_path)
    return relative_path[:-len(fi) - 1]


def get_parent_path(f):
    return '/'.join(f.split('/')[0:-1])


def get_file_from_path(f):
    return f.split('/')[-1]


# e.g. category_folder = docs, file_with_rel_dir = ahmad88me/org/ont.txt
def build_file_structure(file_with_rel_dir, category_folder='', abs_home=''):
    if abs_home == '':
        abs_dir = get_abs_path('')
    else:
        abs_dir = abs_home
    if isinstance(category_folder, str):  # if string
        if category_folder != '':
            abs_dir += category_folder + '/'
    elif isinstance(category_folder, list):  # if list
        for catfol in category_folder:
            abs_dir += catfol + '/'
    abs_dir_with_file = abs_dir + file_with_rel_dir
    abs_dir = get_parent_path(abs_dir_with_file)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    return abs_dir_with_file


######################
# Database functions #
######################


def change_status(target_repo, state):
    try:
        repo = Repo.objects.get(url=target_repo)
        repo.last_used = timezone.now()
        repo.state = state
        repo.save()
        print("change_status> " + repo.state)
        return repo
    except models.DoesNotExist:
        print("change_status> New repo")
        repo = Repo()
        repo.url = target_repo
        repo.state = state
        repo.save()
        return repo
    except Exception as e:
        print('database_exception: ' + str(e))
    return None


# Before calling this function, the g must belong to the user not OnToologyUser
def get_proper_loggedin_scope(ouser, target_repo):
    if ouser.private:
        return True
    try:
        repo = g.get_repo(target_repo)
        if repo.private:
            ouser.private = True
            ouser.save()
            return True
        return False
    except:  # Since we do not have access, it should be private or invalid
        ouser.private = True
        ouser.save()
        return True


def get_repo_branches(repo):
    global g
    if g is None:
        g = init_g()
    repo = g.get_repo(repo)
    branches = repo.get_branches()
    return [b.name for b in branches]


#############################
#   Generate user log file  #
#############################


def generate_user_log(log_file_name):
    # comm = 'cp ' + home + 'log/' + log_file_name + '  ' + \
    comm = 'cp ' + os.path.join(home, 'log', log_file_name) + '  ' + \
           os.path.join(settings.MEDIA_ROOT,
                        'logs')  # ' /home/ubuntu/auton/media/logs/'
    print(comm)
    sys.stdout.flush()
    if sys.stdout == default_stdout:
        print('Warning: trying to close sys.stdout in generate_user_log function, I am disabling the closing for now')
    call(comm, shell=True)


#################################################################
#           TO make this app compatible with Django             #
#################################################################


def django_setup_script():
    """
    To load django
    """
    proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    # This is so Django knows where to find stuff.
    sys.path.append(os.path.join(proj_path, '..'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnToology.settings")
    sys.path.append(proj_path)

    # This is so my local_settings.py gets loaded.
    os.chdir(proj_path)

    # This is so models get loaded.
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
    return application
