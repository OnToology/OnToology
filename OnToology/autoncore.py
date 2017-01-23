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
#


import sys
import os
from github import Github
from datetime import datetime
from subprocess import call
import string
import random
import time
import StringIO
import settings

from __init__ import *

import Integrator


import shutil
import logging

from mongoengine import *


from urllib import quote

use_database = True

ToolUser = 'OnToologyUser'


parent_folder = None


# e.g. home = 'blahblah/temp/'
home = os.environ['github_repos_dir']
verification_log_fname = 'verification.log'
sleeping_time = 7
ontology_formats = ['.rdf', '.owl', '.ttl']
g = None
log_file_dir = None  # '&1'#which is stdout #sys.stdout#by default
tools_conf = {
    'ar2dtool': {'folder_name': 'diagrams', 'type': 'png'},
    'widoco': {'folder_name': 'documentation'},
    'oops': {'folder_name': 'evaluation'},
    'owl2jsonld': {'folder_name': 'context'}
}


def prepare_logger(user):
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
    l = os.path.join(home, 'log', user + sec + '.log_new')
    f = open(l, 'w')
    f.close()
    logging.basicConfig(filename=l, format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)
    return l


def dolog(msg):
    logging.critical(msg)


def init_g():
    global g
    username = os.environ['github_username']
    password = os.environ['github_password']
    g = Github(username, password)


def git_magic(target_repo, user, cloning_repo, changed_filesss):
    logger_fname = prepare_logger(user)
    global g
    global parent_folder
    global log_file_dir
    parent_folder = user
    if not settings.TEST:
        prepare_log(user)
    dolog('############################### magic #############################')
    dolog('target_repo: ' + target_repo)
    change_status(target_repo, 'Preparing')
    # so the tool user can takeover and do stuff
    username = os.environ['github_username']
    password = os.environ['github_password']
    g = Github(username, password)
    local_repo = target_repo.replace(target_repo.split('/')[-2], ToolUser)
    if not settings.TEST or not settings.test_conf['local']:
        delete_repo(local_repo)
    dolog('repo deleted')
    if not settings.TEST or not settings.test_conf['local']:
        dolog('will fork the repo')
        change_status(target_repo, 'forking repo')
        fork_repo(target_repo, username, password)
        dolog('repo forked')
    if not settings.TEST or not settings.test_conf['local']:
        change_status(target_repo, 'cloning repo')
        clone_repo(cloning_repo, user)
        dolog('repo cloned')
    files_to_verify = []
    # print "will loop through changed files"
    from models import Repo
    drepo = Repo.objects.get(url=target_repo)
    Integrator.tools_execution(changed_files=changed_filesss, base_dir=os.path.join(home, user), logfile=log_file_dir,
                               target_repo=target_repo, g_local=g, dolog_fname=logger_fname,
                               change_status=change_status, repo=drepo)

    exception_if_exists = ""
    files_to_verify = [c for c in changed_filesss if c[-4:] in ontology_formats]
    for c in changed_filesss:
        if c[:-4] in ontology_formats:
            print "file to verify: "+c
        else:
            print "c: %s c-4: %s"%(c, c[-4:])

    # After the loop
    dolog("number of files to verify %d" % (len(files_to_verify)))
    if len(files_to_verify) == 0:
        print "files: "+str(files_to_verify)
        change_status(target_repo, 'Ready')
        return
    # if not settings.TEST or not settings.test_conf['local']:
    commit_changes()
    dolog('changes committed')
    remove_old_pull_requests(target_repo)
    if exception_if_exists == "":  # no errors
        change_status(target_repo, 'validating')
    else:
        change_status(target_repo, exception_if_exists)
        # in case there is an error, create the pull request as well
    # Now to enabled
    # This kind of verification is too naive and need to be eliminated
    # for f in files_to_verify:
    #     repo = None
    #     if use_database:
    #         from models import Repo
    #         repo = Repo.objects.get(url=target_repo)
    #     try:
    #         verify_tools_generation_when_ready(f, repo)
    #         dolog('verification is done successfully')
    #     except Exception as e:
    #         dolog('verification have an exception: ' + str(e))

    if use_database:
        if Repo.objects.get(url=target_repo).state != 'validating':
            r = Repo.objects.get(url=target_repo)
            s = r.state
            s = s.replace('validating', '')
            r.state = s
            r.save()
            # The below "return" is commented so pull request are created even if there are files that are not generated
    # if not settings.TEST or not settings.test_conf['local']:
    if True:
        change_status(target_repo, 'creating a pull request')
        try:
            r = send_pull_request(target_repo, ToolUser)
            dolog('pull request is sent')
            change_status(target_repo, 'pull request is sent')
            change_status(target_repo, 'Ready')
        except Exception as e:
            exception_if_exists += str(e)
            dolog('failed to create pull request: '+exception_if_exists)
            change_status(target_repo, 'failed to create a pull request')
    # change_status(target_repo, 'Ready')


def git_magic1(target_repo, user, cloning_repo, changed_filesss):
    prepare_logger(user)
    global g
    global parent_folder
    parent_folder = user
    if not settings.TEST:
        prepare_log(user)
    dolog('############################### magic #############################')
    dolog('target_repo: ' + target_repo)
    change_status(target_repo, 'Preparing')
    # so the tool user can takeover and do stuff
    username = os.environ['github_username']
    password = os.environ['github_password']
    g = Github(username, password)
    local_repo = target_repo.replace(target_repo.split('/')[-2], ToolUser)
    if not settings.TEST or not settings.test_conf['local']:
        delete_repo(local_repo)
    dolog('repo deleted')
    if not settings.TEST or not settings.test_conf['local']:
        dolog('will fork the repo')
        change_status(target_repo, 'forking repo')
        fork_repo(target_repo, username, password)
        dolog('repo forked')
    if not settings.TEST or not settings.test_conf['local']:
        change_status(target_repo, 'cloning repo')
        clone_repo(cloning_repo, user)
        dolog('repo cloned')
    files_to_verify = []
    for chf in changed_filesss:
        auton_conf = {'ar2dtool_enable': False, 'widoco_enable': False,
                      'oops_enable': False, 'owl2jsonld_enable': False}
        if chf[-4:] not in ontology_formats:  # validate ontology formats
            # for now, do not detect the configuration
            continue
            # print 'check conf file changed is: %s'%(chf)
            dolog('check conf file changed is: %s' % (chf))
            if get_file_from_path(chf) == 'OnToology.cfg':
                dolog('OnToology.cfg is changed')
                fi = get_level_up(chf)
                fi = fi[6:]
                dolog('ont file is: ' + fi)
                changed_files = [fi]
                auton_conf = get_auton_configuration(fi)
            elif get_file_from_path(chf) in ar2dtool.ar2dtool_config_types:
                auton_conf['ar2dtool_enable'] = True
                fi = get_level_up(chf)
                fi = get_level_up(fi)
                fi = get_level_up(fi)
                fi = fi[6:]
                changed_files = [fi]
                dolog('change in AR2DTool file %s' % (fi))
            elif 'widoco.conf' in get_file_from_path(chf):
                fi = get_level_up(chf)
                fi = get_level_up(fi)
                fi = fi[6:]
                changed_files = [fi]
                dolog('change in Widoco file %s' % (fi))
        else:
            dolog('working with: ' + chf)
            changed_files = [chf]
            auton_conf = get_auton_configuration(chf)
            # The below three lines is to add files to verify their output
            # later on
            ftvcomp = auton_conf
            ftvcomp['file'] = chf
            files_to_verify.append(ftvcomp)
        dolog(str(auton_conf))
        exception_if_exists = ""
        if auton_conf['ar2dtool_enable']:
            dolog('ar2dtool_enable is true')
            change_status(
                target_repo, 'drawing diagrams for ' + changed_files[0])
            try:
                ar2dtool.draw_diagrams(changed_files)
                dolog('diagrams drawn successfully')
            except Exception as e:
                exception_if_exists += chf + ": " + str(e) + "\n"
                dolog('diagrams not drawn: ' + str(e))
        else:
            dolog('ar2dtool_enable is false')
        if auton_conf['widoco_enable']:
            dolog('ar2dtool_enable is false')
            change_status(
                target_repo, 'generating documents for ' + changed_files[0])
            try:
                generate_widoco_docs(changed_files)
                dolog('generated docs')
            except Exception as e:
                exception_if_exists += str(e)
                dolog('exception in generating documentation: ' + str(e))
        else:
            dolog('widoco_enable is false')
        if auton_conf['oops_enable']:
            dolog('oops_enable is true')
            change_status(
                target_repo, 'OOPS is checking for errors for ' + changed_files[0])
            try:
                oops_ont_files(target_repo, changed_files)
                dolog('oops checked ontology for pitfalls')
            except Exception as e:
                exception_if_exists += str(e)
                dolog('exception in generating oops validation document: ' + str(e))
        else:
            dolog('oops_enable is false')
        if auton_conf['owl2jsonld_enable']:
            dolog('owl2jsonld_enable is true')
            change_status(target_repo,
                          'generating context document for ' +
                          changed_files[0])
            try:
                generate_owl2jsonld_file(changed_files)
                dolog('generated context')
            except Exception as e:
                exception_if_exists += str(e)
                dolog('exception in generating context documentation: ' + str(e))
        else:
            dolog('owl2jsonld_enable is false')

    # After the loop
    dolog("number of files to verify %d" % (len(files_to_verify)))
    if len(files_to_verify) == 0:
        change_status(target_repo, 'Ready')
        return
    if not settings.TEST or not settings.test_conf['local']:
        commit_changes()
        dolog('changes committed')
        remove_old_pull_requests(target_repo)
    if exception_if_exists == "":  # no errors
        change_status(target_repo, 'validating')
    else:
        change_status(target_repo, exception_if_exists)
        # in case there is an error, create the pull request as well
    # Now to enabled
    for f in files_to_verify:
        repo = None
        if use_database:
            from models import Repo
            repo = Repo.objects.get(url=target_repo)
        try:
            verify_tools_generation_when_ready(f, repo)
            dolog('verification is done successfully')
        except Exception as e:
            dolog('verification have an exception: ' + str(e))

    if use_database:
        if Repo.objects.get(url=target_repo).state != 'validating':
            r = Repo.objects.get(url=target_repo)
            s = r.state
            s = s.replace('validating', '')
            r.state = s
            r.save()
            # The below "return" is commented so pull request are created even if there are files that are not generated
    if not settings.TEST or not settings.test_conf['local']:
        change_status(target_repo, 'creating a pull request')
        try:
            r = send_pull_request(target_repo, ToolUser)
        except Exception as e:
            exception_if_exists += str(e)
        dolog('pull request is sent')
    change_status(target_repo, 'Ready')


def verify_tools_generation_when_ready(ver_file_comp, repo=None):
    ver_file = os.path.join(get_target_home(), ver_file_comp['file'], verification_log_fname)
    ver_file = get_abs_path(ver_file)
    dolog('ver file: ' + ver_file)
    if ver_file_comp['ar2dtool_enable'] == ver_file_comp['widoco_enable'] == ver_file_comp['oops_enable'] == ver_file_comp['owl2jsonld_enable'] == False:
        return
    for i in range(20):
        time.sleep(15)
        f = open(ver_file, "r")
        s = f.read()
        f.close()
        if ver_file_comp['ar2dtool_enable'] and 'ar2dtool' not in s:
            continue
        if ver_file_comp['widoco_enable'] and 'widoco' not in s:
            continue
        if ver_file_comp['oops_enable'] and 'oops' not in s:
            continue
        if ver_file_comp['owl2jsonld_enable'] and 'owl2jsonld' not in s:
            continue
        os.remove(ver_file)  # the verification file is no longer needed
        dolog('The removed file is: ' + ver_file)
        return verify_tools_generation(ver_file_comp, repo)
    repo.state = ver_file_comp['file'] + \
        ' is talking too much time to generate output'
    if settings.TEST:
        assert False, 'Taking too much time for verification'
    else:  # I want to see the file in case of testing
        os.remove(ver_file)  # the verification file is no longer needed


# copied from new-look and fixed
def update_file(target_repo, path, message, content):
    global g
    username = os.environ['github_username']
    password = os.environ['github_password']
    g = Github(username, password)
    repo = g.get_repo(target_repo)
    sha = repo.get_file_contents(path).sha
    apath = path
    if apath[0] != "/":
        apath = "/" + apath.strip()
    print "username: " + username
    dolog('will update the file <%s> on repo<%s> with the content <%s>,  sha <%s> and message <%s>' %
          (apath, target_repo, content, sha, message))
    print "repo.update_file('%s', '%s', \"\"\"%s\"\"\" , '%s' )" % (apath, message, content, sha)
    for i in range(3):
        try:
            repo.update_file(apath, message, content, sha)
            dolog('file updated')
            return
        except:
            dolog('chance #%d file update' % i)
            time.sleep(1)
    dolog('after 10 changes, still could not update ')
    # so if there is a problem it will raise an exception which will be captured by the calling function
    repo.update_file(apath, message, content, sha)


def verify_tools_generation(ver_file_comp, repo=None):
    # AR2DTool
    if ver_file_comp['ar2dtool_enable']:
        target_file = os.path.join(get_abs_path(get_target_home()),
                                   ver_file_comp['file'],
                                   tools_conf['ar2dtool']['folder_name'],
                                   ar2dtool.ar2dtool_config_types[0][:-5],
                                   get_file_from_path(ver_file_comp['file']) +
                                   "." + tools_conf['ar2dtool']['type'] +
                                   '.graphml')
        file_exists = os.path.isfile(target_file)
        if repo is not None and not file_exists:
            repo.state += ' The Diagram of the file %s is not generated ' % \
                (ver_file_comp['file'])
            repo.save()
        if settings.TEST:
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
        if settings.TEST:
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
        if settings.TEST:
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
        if settings.TEST:
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


def get_ontologies_in_online_repo(target_repo):
    global g
    if type(g) == type(None):
        init_g()
    repo = g.get_repo(target_repo)
    sha = repo.get_commits()[0].sha
    files = repo.get_git_tree(sha=sha, recursive=True).tree
    ontologies = []
    ontoology_home_name = 'OnToology'
    for f in files:
        if f.path[:len(ontoology_home_name)] != ontoology_home_name:
            for ontfot in ontology_formats:
                if f.path[-len(ontfot):] == ontfot:
                    ontologies.append(f.path)
                    break
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
    id = g.get_user().id
    if is_organization(target_repo):
        try:
            collaborators = g.get_repo(target_repo).get_collaborators()
            for coll in collaborators:
                if id == coll.id:
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


def fork_repo(target_repo, username, password):
    # the wait time to give github sometime so the repo can be forked
    # successfully
    time.sleep(sleeping_time)
    # this is a workaround and not a proper way to do a fork
    comm = "curl --user \"%s:%s\" --request POST --data \'{}\' https://api.github.com/repos/%s/forks" % (
        username, password, target_repo)
    if not settings.TEST:
        comm += ' >> "' + log_file_dir + '"'
    dolog(comm)
    call(comm, shell=True)
    dolog('fork')


def clone_repo(cloning_repo, parent_folder, dosleep=True):
    global g
    if g is None:
        init_g()
    dolog('home: %s' % (home))
    dolog('parent_folder: %s' % (parent_folder))
    dolog('logfile: %s' % (log_file_dir))
    if dosleep:
        # the wait time to give github sometime so the repo can be cloned
        time.sleep(sleeping_time)
    try:
        comm = "rm" + " -Rf " + home + parent_folder
        if not settings.TEST:
            comm += ' >> "' + log_file_dir + '"'
        dolog(comm)
        call(comm, shell=True)
    except Exception as e:
        dolog('rm failed: ' + str(e))
    comm = "git" + " clone" + " " + cloning_repo + " " + home + parent_folder
    if not settings.TEST:
        comm += ' >> "' + log_file_dir + '"'
    dolog(comm)
    call(comm, shell=True)
    # comm = "chmod -R 777 " + home + parent_folder
    # if not settings.TEST:
    #     comm += ' >> "' + log_file_dir + '"'
    # dolog(comm)
    # call(comm, shell=True)
    return home + parent_folder


def commit_changes():
    global g
    if g is None:
        init_g()
    gu = "git config  user.email \"ahmad88csc@gmail.com\";"
    gu += 'git config  user.name "%s" ;' % (ToolUser)
    comm = "cd " + home + parent_folder + ";" + gu + " git add . "
    if not settings.TEST:
        comm += ' >> "' + log_file_dir + '"'
    dolog(comm)
    call(comm, shell=True)
    comm = "cd " + home + parent_folder + ";" + \
        gu + " git commit -m 'automated change' "
    if not settings.TEST:
        comm += ' >> "' + log_file_dir + '"'
    dolog(comm)
    call(comm, shell=True)
    gup = "git config push.default matching;"
    comm = "cd " + home + parent_folder + ";" + gu + gup + " git push "
    if not settings.TEST:
        comm += ' >> "' + log_file_dir + '"'
    dolog(comm)
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
            print "Exception removing an old pull request: "+str(e)
            dolog("Exception removing an old pull request: "+str(e))


def send_pull_request(target_repo, username):
    title = 'OnToology update'
    body = title
    err = ""
    time.sleep(sleeping_time)
    try:
        g.get_repo(target_repo).create_pull(head=username +
                                            ':master', base='master', title=title, body=body)
        return {'status': True, 'msg': 'pull request created successfully'}
    except Exception as e:
        err = str(e)
        dolog('pull request error: ' + err)
    return {'status': False, 'error': err}


def webhook_access(client_id, redirect_url, isprivate):
    if isprivate:
        scope = 'repo'
    else:
        scope = 'public_repo'
    # scope = 'admin:org_hook'
    # scope+=',admin:org,admin:public_key,admin:repo_hook,gist,notifications,delete_repo,repo_deployment,
    # repo,public_repo,user,admin:public_key'
    sec = ''.join([random.choice(string.ascii_letters + string.digits)
                   for _ in range(9)])
    return "https://github.com/login/oauth/authorize?client_id=" + client_id + "&redirect_uri=" +\
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
    print "target_repo: "+str(target_repo)
    print "notification url: "+str(notification_url)
    for hook in g.get_repo(target_repo).get_hooks():
        try:
            if hook.config["url"] == notification_url:
                hook.delete()
                break
        except Exception as e:
            print "error removing the webhook: %s" %(str(e))
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
        return {'status': False, 'error': str(e)}  # e.data}


def add_collaborator(target_repo, user, newg=None):
    global g
    if newg is None:
        if g is None:
            init_g()
        newg = g
    try:
        print "adding collaborator from user: %s " % str(newg.get_user().name)
        if newg.get_user().name is None or newg.get_user().email is None:
            return {'status': False, 'error': 'Make sure you have your name and email public and not empty on GitHub'}
        if newg.get_repo(target_repo).has_in_collaborators(user):
            return {'status': True, 'msg': 'this user is already a collaborator'}
        else:
            msg = newg.get_repo(target_repo).add_to_collaborators(user)
            #return {'status': True, 'msg': str(msg)}
            return {'status': True, 'msg': 'added as a new collaborator'}
    except Exception as e:
        return {'status': False, 'error': str(e)}  # e.data}


def update_g(token):
    global g
    g = Github(token)


def generate_bundle(base_dir, target_repo, ontology_bundle):
    """
    :param base_dir: e.g. /home/user/temp/random-folder-xyz
    :param target_repo:  user/reponame
    :param ontology_bundle: OnToology/abc/alo.owl
    :return: the bundle zip file dir if successful, or None otherwise
    """
    global g
    if g is None:
        init_g()
    try:
        print 'ontology bundle: '+ontology_bundle
        repo = g.get_repo(target_repo)
        sha = repo.get_commits()[0].sha
        files = repo.get_git_tree(sha=sha, recursive=True).tree
        print 'num of files: '+str(len(files))
        for f in files:
            try:
                for i in range(3):
                    try:
                        print 'f: '+str(f)
                        print 'next: '+str(f.path)
                        p = f.path
                        break
                    except:
                        time.sleep(2)
                p = f.path
                if p[0] == '/':
                    p = p[1:]
                abs_path = os.path.join(base_dir, p)
                if p[:len(ontology_bundle)] == ontology_bundle:
                    print 'true: '+str(p)
                    if f.type == 'tree':
                        os.makedirs(abs_path)
                    elif f.type == 'blob':
                        parent_folder = os.path.join(*abs_path.split('/')[:-1])
                        if parent_folder != base_dir: # not in the top level of the repo
                            try:
                                os.makedirs(parent_folder)
                            except:
                                pass
                        with open(abs_path, 'w') as fii:
                            file_content = repo.get_file_contents(f.path).decoded_content
                            fii.write(file_content)
                            print 'file %s content: %s' % (f.path, file_content[:10])
                    else:
                        print 'unknown type in generate bundle'
                else:
                    print 'not: '+p
            except Exception as e:
                print 'exception: '+str(e)
        zip_file = os.path.join(base_dir, '%s.zip' % ontology_bundle.split('/')[-1])
        comm = "cd %s; zip -r '%s' OnToology" % (base_dir, zip_file)
        print 'comm: %s' % comm
        call(comm, shell=True)
        return os.path.join(base_dir, zip_file)
        #return None
    except Exception as e:
        print 'error in generate_bundle: '+str(e)
        return None


########################################################################
########################################################################
# #####################  Auton configuration file  #####################
########################################################################
########################################################################


import ConfigParser


def get_confs_from_repo(target_repo):
    global g
    repo = g.get_repo(target_repo)
    sha = repo.get_commits()[0].sha
    files = repo.get_git_tree(sha=sha, recursive=True).tree
    conf_files = []
    for f in files:
        if 'OnToology.cfg' in f.path:
            conf_files.append(f)
    return repo, conf_files


def parse_online_repo_for_ontologies(target_repo):
    """ This is parse repositories for ontologies configuration files OnToology.cfg
    """
    global g
    if g is None:
        init_g()
    print "in parse online repo for ontologies"
    repo, conf_paths = get_confs_from_repo(target_repo)
    print "repo: %s, conf_paths: %s" % (str(repo), str(conf_paths))
    ontologies = []

    for cpath in conf_paths:
        p = quote(cpath.path)
        print "get file content: %s" % (str(cpath.path))
        print "after quote: %s" % p
        print "now get the decoded content"
        # file_content = repo.get_file_contents(cpath.path).decoded_content
        file_content = repo.get_file_contents(p).decoded_content
        print "file_content: "+str(file_content)
        buffile = StringIO.StringIO(file_content)
        print "will get the config"
        confs = get_auton_config(buffile)
        print "gotten confs: "+str(confs)
        o = {}
        # o['ontology'] = get_parent_path(cpath.path)[len(get_target_home()):]
        o['ontology'] = get_parent_path(p)[len(get_target_home()):]
        for c in confs:
            tool = c.replace('_enable', '')
            o[tool] = confs[c]
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
    dolog('auton config is called: ')
    ar2dtool_sec_name = 'ar2dtool'
    widoco_sec_name = 'widoco'
    oops_sec_name = 'oops'
    owl2jsonld_sec_name = 'owl2jsonld'
    ar2dtool_enable = True
    widoco_enable = True
    oops_enable = True
    owl2jsonld_enable = True
    config = ConfigParser.RawConfigParser()
    if from_string:
        opened_conf_files = config.readfp(conf_file_abs)
    else:
        opened_conf_files = config.read(conf_file_abs)
    if from_string or len(opened_conf_files) == 1:
        dolog('auton configuration file exists')
        try:
            ar2dtool_enable = config.getboolean(ar2dtool_sec_name, 'enable')
            dolog('got ar2dtool enable value: ' + str(ar2dtool_enable))
        except:
            dolog('ar2dtool enable value doesnot exist')
            pass
        try:
            widoco_enable = config.getboolean(widoco_sec_name, 'enable')
            dolog('got widoco enable value: ' + str(widoco_enable))
        except:
            dolog('widoco enable value doesnot exist')
            pass
        try:
            oops_enable = config.getboolean(oops_sec_name, 'enable')
            dolog('got oops enable value: ' + str(oops_enable))
        except:
            dolog('oops enable value doesnot exist')
        try:
            owl2jsonld_enable = config.getboolean(
                owl2jsonld_sec_name, 'enable')
            dolog('got owl2jsonld enable value: ' + str(owl2jsonld_enable))
        except:
            dolog('owl2jsonld enable value doesnot exist')
    else:
        dolog('auton configuration file does not exists')
        config.add_section(ar2dtool_sec_name)
        config.set(ar2dtool_sec_name, 'enable', ar2dtool_enable)
        config.add_section(widoco_sec_name)
        config.set(widoco_sec_name, 'enable', widoco_enable)
        config.add_section(oops_sec_name)
        config.set(oops_sec_name, 'enable', oops_enable)
        config.add_section(owl2jsonld_sec_name)
        config.set(owl2jsonld_sec_name, 'enable', owl2jsonld_enable)
        conff = conf_file_abs
        dolog('will create conf file: ' + conff)
        try:
            with open(conff, 'wb') as configfile:
                config.write(configfile)
        except Exception as e:
            dolog('expection: ')
            dolog(e)
    return {'ar2dtool_enable': ar2dtool_enable,
            'widoco_enable': widoco_enable,
            'oops_enable': oops_enable,
            'owl2jsonld_enable': owl2jsonld_enable}


##########################################################################
################################# generic helper functions ###############
##########################################################################


def delete_dir(target_directory):
    comm = "rm -Rf " + target_directory
    if not settings.TEST:
        comm += '  >> "' + log_file_dir + '" '
    print comm
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
    if type(category_folder) == type(""):  # if string
        if category_folder != '':
            abs_dir += category_folder + '/'
    elif type(category_folder) == type([]):  # if list
        for catfol in category_folder:
            abs_dir += catfol + '/'
    abs_dir_with_file = abs_dir + file_with_rel_dir
    abs_dir = get_parent_path(abs_dir_with_file)
    if not os.path.exists(abs_dir):
        os.makedirs(abs_dir)
    return abs_dir_with_file


##########################################################################
################################ Database functions ######################
##########################################################################

# if use_database:
#    from Auton.models import Repo
# import it for now
def change_status(target_repo, state):
    from models import Repo
    if not use_database:
        return ''
    try:
        repo = Repo.objects.get(url=target_repo)
        repo.last_used = datetime.today()
        repo.state = state
        repo.owner = parent_folder
        repo.save()
    except DoesNotExist:
        repo = Repo()
        repo.url = target_repo
        repo.state = state
        repo.owner = parent_folder
        repo.save()
    except Exception as e:
        print 'database_exception: ' + str(e)


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


##########################################################################
#####################   Generate user log file  ##########################
##########################################################################

# just for the development phase


def generate_user_log(log_file_name):
    comm = 'cp ' + home + 'log/' + log_file_name + '  ' + \
        os.path.join(settings.MEDIA_ROOT,
                     'logs')  # ' /home/ubuntu/auton/media/logs/'
    print comm
    sys.stdout.flush()
    if sys.stdout == default_stdout:
        print 'Warning: trying to close sys.stdout in generate_user_log function, I am disabling the closing for now'
    call(comm, shell=True)


# #########################################################################
# ###################################   main  #############################
# #########################################################################


if __name__ == "__main__":
    print "autoncore command: " + str(sys.argv)
    if use_database:
        connect('OnToology')
    git_magic(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
