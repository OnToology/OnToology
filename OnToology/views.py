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
import string
import random
import json
import os
import subprocess
import shutil
from subprocess import call

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mongoengine.queryset import DoesNotExist
import requests
from github import Github

import settings
from autoncore import git_magic, add_webhook, ToolUser, webhook_access, update_g, add_collaborator, \
    clone_repo
from autoncore import parse_online_repo_for_ontologies, update_file, remove_webhook, \
    init_g
from autoncore import get_proper_loggedin_scope, get_ontologies_in_online_repo, generate_bundle
from models import *
import autoncore
from settings import host
# from settings import client_id_login, client_id_public, client_id_private, client_secret_login, client_secret_public, client_secret_private
import Integrator.previsual as previsual

client_id_login = os.environ['client_id_login']  # 'e2ea731b481438fd1675'
client_id_public = os.environ['client_id_public']  # '878434ff1065b7fa5b92'
client_id_private = os.environ['client_id_private']  # 'dd002c8587d08edfaf5f'

client_secret_login = os.environ['client_secret_login']  # 'ba0f149934e3d78816cbd89d1f3c5109b82898ab'
client_secret_public = os.environ['client_secret_public']  # 'c76144cbbbf5df080df0232928af9811d78792dd'
client_secret_private = os.environ['client_secret_private']  # 'c5fbaa760362ba23f7c8d07c35021ac111ca5418'

settings.SECRET_KEY = os.environ['SECRET_KEY']
client_id = None
client_secret = None
is_private = None

publish_dir = os.environ['publish_dir']

import sys

reload(sys)
sys.setdefaultencoding("UTF-8")

# So the prints shows in apache error log
sys.stdout = sys.stderr


def home(request):
    global client_id, client_secret, is_private
    # sys.stdout = sys.stderr
    # print "******* output to stderror ********"
    sys.stdout.flush()
    sys.stderr.flush()
    if 'target_repo' in request.GET:
        print "we are inside"
        target_repo = request.GET['target_repo']
        if target_repo.strip() == "" or len(target_repo.split('/')) != 2:
            return render(request, 'msg.html', {'msg': 'please enter a valid repo'})
        init_g()
        # if not has_access_to_repo(target_repo):# this for the organization
        # return render(request,'msg.html',{'msg': 'repos under organizations are not supported at the moment'})
        wgets_dir = os.environ['wget_dir']
        if call('cd %s; wget %s;' % (wgets_dir, 'http://github.com/' + target_repo.strip()), shell=True) == 0:
            is_private = False
            client_id = client_id_public
            client_secret = client_secret_public
        else:
            is_private = True
            client_id = client_id_private
            client_secret = client_secret_private
        webhook_access_url, state = webhook_access(client_id, host + '/get_access_token', isprivate=is_private)
        request.session['target_repo'] = target_repo
        request.session['state'] = state
        request.session['access_token_time'] = '1'
        return HttpResponseRedirect(webhook_access_url)
    repos = Repo.objects.order_by('-last_used')[:10]
    num_of_users = len(User.objects.all())
    num_of_repos = len(Repo.objects.all())
    print "returning the request"
    return render(request, 'home.html', {'repos': repos, 'user': request.user, 'num_of_users': num_of_users,
                                         'num_of_repos': num_of_repos})


def grant_update(request):
    return render_to_response('msg.html', {'msg': 'Magic is done'}, context_instance=RequestContext(request))


def get_access_token(request):
    print "get_access_token"
    global is_private, client_id, client_secret
    if 'state' not in request.session or request.GET['state'] != request.session['state']:
        return HttpResponseRedirect('/')
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': request.GET['code'],
        'redirect_uri': host + '/add_hook'
    }
    res = requests.post('https://github.com/login/oauth/access_token', data=data)
    try:
        atts = res.text.split('&')
        d = {}
        for att in atts:
            keyv = att.split('=')
            d[keyv[0]] = keyv[1]
    except Exception as e:
        print "Exception: %s" % str(e)
        print "response: %s" % str(res.text)
        return render(request, 'msg.html', {'Error getting the token from GitHub. please try again or contact us'})
    if 'access_token' not in d:
        print 'access_token is not there'
        return HttpResponseRedirect('/')

    access_token = d['access_token']
    request.session['access_token'] = access_token
    update_g(access_token)
    print 'access_token: ' + access_token

    if request.user.is_authenticated() and request.session['access_token_time'] == '1':
        request.session['access_token_time'] = '2'  # so we do not loop
        # isprivate = get_proper_loggedin_scope(OUser.objects.get(username=request.user.username),
        #                                      request.session['target_repo'])
        # print 'isprivate is: ' + str(isprivate)
        webhook_access_url, state = webhook_access(client_id, host + '/get_access_token', is_private)
        request.session['state'] = state
        return HttpResponseRedirect(webhook_access_url)

    rpy_wh = add_webhook(request.session['target_repo'], host + "/add_hook")
    rpy_coll = add_collaborator(request.session['target_repo'], ToolUser)
    error_msg = ""
    if rpy_wh['status'] == False:
        error_msg += str(rpy_wh['error'])
        print 'error adding webhook: ' + error_msg
    if rpy_coll['status'] == False:
        error_msg += str(rpy_coll['error'])
        print 'error adding collaborator: ' + rpy_coll['error']
    else:
        print 'adding collaborator: ' + rpy_coll['msg']
    if error_msg != "":
        if 'Hook already exists on this repository' in error_msg:
            error_msg = 'This repository already watched'
        elif '404' in error_msg:  # so no enough access according to Github troubleshooting guide
            error_msg = """You don\'t have permission to add collaborators and create webhooks to this repo or this
            repo does not exist. Note that if you can fork this repo, you can add it here"""
            return render_to_response('msg.html', {'msg': error_msg}, context_instance=RequestContext(request))
        else:
            print "error message not hook and not 404: " + error_msg
            print "target repo: " + request.session['target_repo']
            print "ToolUser: " + ToolUser
        msg = error_msg
    else:
        msg = 'webhook attached and user added as collaborator, Note that generating the documentation, diagrams and evaluation report takes sometime to be generated. In "My repositories" page, you can see the status of each repo.'
    target_repo = request.session['target_repo']
    try:
        repo = Repo.objects.get(url=target_repo)
    except Exception as e:
        print str(e)
        repo = Repo()
        repo.url = target_repo
        repo.save()
    if request.user.is_authenticated():
        ouser = OUser.objects.get(email=request.user.email)
        if repo not in ouser.repos:
            ouser.repos.append(repo)
            ouser.save()
            generateforall(repo.url, ouser.email)
    return render_to_response('msg.html', {'msg': msg},
                              context_instance=RequestContext(request))


def get_changed_files_from_payload(payload):
    commits = payload['commits']
    changed_files = []
    for c in commits:
        changed_files += c["added"] + c["modified"]
    return changed_files


@csrf_exempt
def add_hook(request):
    print "in add hook function"
    if settings.test_conf['local']:
        print 'We are in test mode'
    try:
        print "\n\nPOST DATA\n\n: " + str(request.POST)
        s = str(request.POST['payload'])
        print "payload: " + s
        j = json.loads(s, strict=False)
        print "json is loaded"
        if j["ref"] == "refs/heads/gh-pages":
            print "it is just gh-pages"
            return render(request, 'msg.html', {'msg': 'it is gh-pages, so nothing'})
        s = j['repository']['url'] + 'updated files: ' + str(j['head_commit']['modified'])
        print "just s: " + str(s)
        cloning_repo = j['repository']['git_url']
        target_repo = j['repository']['full_name']
        user = j['repository']['owner']['email']
        print "cloning_repo: " + str(cloning_repo)
        print "target_repo: " + str(target_repo)
        print "user email: " + str(user)
        changed_files = get_changed_files_from_payload(j)
        print "early changed files: " + str(changed_files)
        if 'Merge pull request' in j['head_commit']['message'] or 'OnToology Configuration' == j['head_commit'][
            'message']:
            print 'This is a merge request or Configuration push'
            try:
                repo = Repo.objects.get(url=target_repo)
                print 'got the repo'
                repo.last_used = datetime.today()
                repo.progress = 100.0
                repo.save()
                print 'repo saved'
            except DoesNotExist:
                repo = Repo()
                repo.url = target_repo
                repo.save()
            except Exception as e:
                print 'database_exception: ' + str(e)
            msg = 'This indicate that this merge request will be ignored'
            print msg
            if settings.test_conf['local']:
                print msg
                return
            else:
                return render_to_response('msg.html', {'msg': msg}, context_instance=RequestContext(request))
    except Exception as e:
        print "add hook exception: " + str(e)
        msg = 'This request should be a webhook ping'
        if settings.test_conf['local']:
            print msg
            return
        else:
            return render_to_response('msg.html', {'msg': msg}, context_instance=RequestContext(request))
    print '##################################################'
    print 'changed_files: ' + str(changed_files)
    # cloning_repo should look like 'git@github.com:AutonUser/target.git'
    tar = cloning_repo.split('/')[-2]
    cloning_repo = cloning_repo.replace(tar, ToolUser)
    cloning_repo = cloning_repo.replace('git://github.com/', 'git@github.com:')
    # comm = "python /home/ubuntu/OnToology/OnToology/autoncore.py "
    if 'virtual_env_dir' in os.environ:
        comm = "%s %s " % \
               (os.path.join(os.environ['virtual_env_dir'], 'bin', 'python'),
                (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'autoncore.py')))
    else:
        comm = "python %s " % \
               (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'autoncore.py'))
    print 'in addhook'
    print "target repo: %s" % target_repo
    print "user: %s" % user
    # comm += ' "' + target_repo + '" "' + user + '" '
    comm += '--magic --target_repo "' + target_repo + '" --useremail "' + user + '" --changedfiles '
    for c in changed_files:
        comm += '"' + c + '" '
    if settings.test_conf['local']:
        print 'will call git_magic with target=%s, user=%s, cloning_repo=%s, changed_files=%s' % (target_repo, user,
                                                                                                  cloning_repo,
                                                                                                  str(changed_files))
        git_magic(target_repo, user, changed_files)
        return
    else:
        print 'running autoncore code as: ' + comm
        try:
            subprocess.Popen(comm, shell=True)
        except Exception as e:
            error_msg = str(e)
            print 'error running generall all subprocess: ' + error_msg
            sys.stdout.flush()
            sys.stderr.flush()
            if 'execv() arg 2 must contain only strings' in error_msg:
                error_msg = 'make sure that your repository filenames does not have accents or special characters'
            else:
                error_msg = 'generic error, please report the problem to us ontoology@delicias.dia.fi.upm.es'
            s = error_msg
        # subprocess.Popen(comm, shell=True)
        return render_to_response('msg.html', {'msg': '' + s}, context_instance=RequestContext(request))


@login_required
def generateforall_view(request):
    if 'repo' not in request.GET:
        return HttpResponseRedirect('/')
    target_repo = request.GET['repo'].strip()
    found = False
    if target_repo[-1] == '/':
        target_repo = target_repo[:-1]
    print 'target_repo is <%s>' % target_repo
    # The below couple of lines are to check that the user currently have permission over the repository
    try:
        ouser = OUser.objects.get(email=request.user.email)
        for r in ouser.repos:
            if r.url == target_repo:
                found = True
                break
    except:
        return render(request, 'msg.html', {'msg': 'Please contact ontoology@delicias.dia.fi.upm.es'})
    if not found:
        return render(request, 'msg.html',
                      {'msg': 'You need to register/watch this repository while you are logged in'})
    res = generateforall(target_repo, request.user.email)
    if res['status'] is True:
        return render_to_response('msg.html', {
            'msg': 'Soon you will find generated files included in a pull request in your repository'},
                                  context_instance=RequestContext(request))
    else:
        return render(request, 'msg.html', {'msg': res['error']})


def generateforall(target_repo, user_email):
    user = user_email
    ontologies = get_ontologies_in_online_repo(target_repo)
    changed_files = ontologies
    print 'current file dir: %s' % str(os.path.dirname(os.path.realpath(__file__)))
    if 'virtual_env_dir' in os.environ:
        print 'virtual_env_dir is in environ'
        comm = "%s %s " % \
               (os.path.join(os.environ['virtual_env_dir'], 'bin', 'python'),
                (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'autoncore.py')))
    else:
        print 'virtual_env_dir is NOT in environ'
        comm = "python %s " % \
               (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'autoncore.py'))
    comm += '--magic --target_repo "' + target_repo + '" --useremail "' + user + '" --changedfiles '
    for c in changed_files:
        comm += '"' + c.strip() + '" '
    if settings.test_conf['local']:
        print "running autoncode in the same thread"
        git_magic(target_repo, user, changed_files)
    else:
        print 'running autoncore code as: ' + comm

        try:
            subprocess.Popen(comm, shell=True)
        except Exception as e:
            sys.stdout.flush()
            sys.stderr.flush()
            error_msg = str(e)
            print 'error running generall all subprocess: ' + error_msg
            if 'execv() arg 2 must contain only strings' in error_msg:
                return {'status': False,
                        'error': 'make sure that your repository filenames does not have accents or special characters'}
            else:
                return {'status': False,
                        'error': 'generic error, please report the problem to us at ontoology@delicias.dia.fi.upm.es'}
    sys.stdout.flush()
    sys.stderr.flush()
    return {'status': True}


def login(request):
    print '******* login *********'
    redirect_url = host + '/login_get_access'
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
    request.session['state'] = sec
    scope = 'user:email'  # get_proper_scope_to_login(username)
    # scope = 'admin:org_hook'
    # scope+=',admin:org,admin:public_key,admin:repo_hook,gist,notifications,delete_repo,repo_deployment,repo,public_repo,user,admin:public_key'
    redirect_url = "https://github.com/login/oauth/authorize?client_id=" + client_id_login + "&redirect_uri=" + redirect_url + "&scope=" + scope + "&state=" + sec
    return HttpResponseRedirect(redirect_url)


def logout(request):
    print '*** logout ***'
    django_logout(request)
    return HttpResponseRedirect('/')


def login_get_access(request):
    print '*********** login_get_access ************'
    if 'state' not in request.session:
        request.session['state'] = 'blah123'  # 'state'
    if request.GET['state'] != request.session['state']:
        return HttpResponseRedirect('/')
    data = {
        'client_id': client_id_login,
        'client_secret': client_secret_login,
        'code': request.GET['code'],
        'redirect_uri': host  # host+'/add_hook'
    }
    res = requests.post('https://github.com/login/oauth/access_token', data=data)
    atts = res.text.split('&')
    d = {}
    try:
        for att in atts:
            keyv = att.split('=')
            d[keyv[0]] = keyv[1]
        access_token = d['access_token']
        request.session['access_token'] = access_token
        print 'access_token: ' + access_token
    except Exception as e:
        print "exception: " + str(e)
        print "no access token"
        print "response: %s" % res.text
        return HttpResponseRedirect('/')

    g = Github(access_token)
    email = g.get_user().email
    username = g.get_user().login
    if email == '' or type(email) == type(None):
        return render(request, 'msg.html', {'msg': 'You have to make you email public and try again'})
    request.session['avatar_url'] = g.get_user().avatar_url
    print 'avatar_url: ' + request.session['avatar_url']
    try:
        user = OUser.objects.get(email=email)
        user.username = username
        user.backend = 'mongoengine.django.auth.MongoEngineBackend'
        user.save()
    except:
        try:
            user = OUser.objects.get(username=username)
            user.email = email
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            user.save()
        except:
            print '<%s,%s>' % (email, username)
            sys.stdout.flush()
            sys.stderr.flush()
            # The password is never important but we set it here because it is required by User class
            user = OUser.create_user(username=username, password=request.session['state'], email=email)
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            user.save()
    django_login(request, user)
    print 'access_token: ' + access_token
    sys.stdout.flush()
    sys.stderr.flush()
    return HttpResponseRedirect('/')


@login_required
def profile(request):
    print '************* profile ************'
    print str(datetime.today())
    if 'fake' in request.GET and request.user.email == 'ahmad88me@gmail.com':
        print 'faking the user: ' + request.GET['fake']
        user = OUser.objects.get(email=request.GET['fake'])
    else:
        print 'not faking'
        user = request.user
    error_msg = ''
    if 'repo' in request.GET and 'name' not in request.GET:  # asking for ontologies in a repo
        repo = request.GET['repo']
        print 'repo :<%s>' % (repo)
        print 'got the repo'
        try:
            print 'trying to validate repo'
            hackatt = True
            for repooo in user.repos:
                if repooo.url == repo:
                    hackatt = False
                    break
            if hackatt:  # trying to access a repo that does not belong to the use currently logged in
                return render(request, 'msg.html', {'msg': 'This repo is not added, please do so in the main page'})
            print 'try to get abs folder'
            if type(autoncore.g) == type(None):
                print 'access token is: ' + request.session['access_token']
                update_g(request.session['access_token'])
            try:
                ontologies = parse_online_repo_for_ontologies(repo)
                print 'ontologies: ' + str(len(ontologies))
                arepo = Repo.objects.get(url=repo)
                pnames = PublishName.objects.filter(user=user, repo=arepo)
                for o in ontologies:
                    print '--------\n%s\n' % o
                    o['published'] = False
                    o['pname'] = ''
                    for pn in pnames:
                        if pn.ontology == o['ontology']:
                            o['published'] = True
                            o['pname'] = pn.name
                            break
                    for d in o:
                        print '   ' + d + ': ' + str(o[d])
                print 'testing redirect'
                print 'will return the Json'
                jresponse = JsonResponse({'ontologies': ontologies})
                jresponse.__setitem__('Content-Length', len(jresponse.content))
                sys.stdout.flush()
                sys.stderr.flush()
                return jresponse
            except Exception as e:
                print "exception in getting the ontologies for the repo: " + str(repo)
                print "exception:  " + str(e)
                arepo = Repo.objects.get(url=repo)
                arepo.state = 'Invalid repository'
                arepo.save()
                ontologies = []
                jresponse = JsonResponse({'ontologies': ontologies})
                jresponse.__setitem__('Content-Length', len(jresponse.content))
                sys.stdout.flush()
                sys.stderr.flush()
                return jresponse
        except Exception as e:
            print 'exception: ' + str(e)
    # elif 'name' in request.GET:  # publish with a new name
    #     print request.GET
    #     name = request.GET['name']
    #     target_repo = request.GET['repo']
    #     ontology_rel_path = request.GET['ontology']
    #     found = False
    #     for r in user.repos:
    #         if target_repo == r.url:
    #             found = True
    #             repo = r
    #             break
    #     if found:  # if the repo belongs to the user
    #
    #         if len(PublishName.objects.filter(name=name)) > 1:
    #             error_msg = 'a duplicate published names, please contact us ASAP to fix it'
    #
    #         elif len(PublishName.objects.filter(name=name)) == 0 or (PublishName.objects.get(name=name).user == user and
    #                                                                  PublishName.objects.get(name=name).repo == repo and
    #                                                                  PublishName.objects.get(
    #                                                                      name=name).ontology == ontology_rel_path):
    #             if (len(PublishName.objects.filter(name=name)) == 0 and
    #                     len(PublishName.objects.filter(user=user, ontology=ontology_rel_path, repo=repo)) > 0):
    #                 error_msg += 'can not reserve multiple names for the same ontology'
    #             else:
    #                 autoncore.prepare_log(user.email)
    #                 # cloning_repo should look like 'git@github.com:user/reponame.git'
    #                 cloning_repo = 'git@github.com:%s.git' % target_repo
    #                 sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
    #                 folder_name = 'pub-' + sec
    #                 clone_repo(cloning_repo, folder_name, dosleep=True)
    #                 repo_dir = os.path.join(autoncore.home, folder_name)
    #                 doc_dir = os.path.join(repo_dir, 'OnToology', ontology_rel_path[1:], 'documentation')
    #                 print 'repo_dir: %s' % repo_dir
    #                 print 'doc_dir: %s' % doc_dir
    #                 htaccess_f = os.path.join(doc_dir, '.htaccess')
    #                 if not os.path.exists(htaccess_f):
    #                     print 'htaccess is not found'
    #                     # error_msg += 'make sure your ontology has documentation and htaccess'
    #                     error_msg += 'We couldn\'t reserve your w3id. Please make sure that your ontology has ' \
    #                                  'documentation and htacess. For that, click on "Generate documentation, diagrams' \
    #                                  ' and evaluation" on the menu, and once the process is completed, accept the ' \
    #                                  'pull request on you GitHub repository'
    #                 else:
    #                     print 'found htaccesss'
    #                     f = open(htaccess_f, 'r')
    #                     file_content = f.read()
    #                     f.close()
    #                     f = open(htaccess_f, 'w')
    #                     for line in file_content.split('\n'):
    #                         if line[:11] == 'RewriteBase':
    #                             f.write('RewriteBase /publish/%s \n' % name)
    #                         else:
    #                             f.write(line + '\n')
    #                     f.close()
    #                     # comm = 'rm -Rf /home/ubuntu/publish/%s' % name
    #                     comm = 'rm -Rf ' + os.path.join(publish_dir, name)
    #                     print(comm)
    #                     call(comm, shell=True)
    #                     # comm = 'mv %s /home/ubuntu/publish/%s' % (doc_dir, name)
    #                     comm = 'mv %s %s' % (doc_dir, os.path.join(publish_dir, name))
    #                     print comm
    #                     call(comm, shell=True)
    #                     if len(PublishName.objects.filter(name=name)) == 0:
    #                         p = PublishName(name=name, user=user, repo=repo, ontology=ontology_rel_path)
    #                         p.save()
    #         else:
    #             if PublishName.objects.get(name=name).user == user:
    #                 print 'same user'
    #             if PublishName.objects.get(name=name).repo == repo:
    #                 print 'same repo'
    #             if PublishName.objects.get(name=name).ontology == ontology_rel_path:
    #                 print 'same ontology'
    #             error_msg += ' Name already taken'
    #     else:  # not found
    #         error_msg += 'You should add this repo to OnToology first'

    elif 'delete-name' in request.GET:
        name = request.GET['delete-name']
        p = PublishName.objects.filter(name=name)
        if len(p) == 0:
            error_msg += 'This name is not reserved'
        elif p[0].user.id == user.id:
            pp = p[0]
            pp.delete()
            pp.save()
            # comm = 'rm -Rf /home/ubuntu/publish/%s' % name
            comm = 'rm -Rf ' + os.path.join(publish_dir, name)
            call(comm, shell=True)
        else:
            error_msg += 'You are trying to delete a name that does not belong to you'
    print 'testing redirect'
    repos = user.repos
    for r in repos:
        try:
            if len(r.url.split('/')) != 2:
                user.update(pull__repos=r)
                r.delete()
                user.save()
                continue
            r.user = r.url.split('/')[0]
            r.rrepo = r.url.split('/')[1]
        except:
            user.update(pull__repos=r)
            user.save()
    request.GET = []
    sys.stdout.flush()
    sys.stderr.flush()
    return render(request, 'profile.html', {'repos': repos, 'pnames': PublishName.objects.filter(user=user),
                                            'error': error_msg, 'manager': request.user.email in get_managers()})


def update_conf(request):
    print 'inside update_conf'
    if request.method == "GET":
        return render(request, "msg.html", {"msg": "This method expects POST only"})
    ontologies = request.POST.getlist('ontology')
    data = request.POST
    for onto in ontologies:
        print 'inside the loop'
        ar2dtool = onto + '-ar2dtool' in data
        print 'ar2dtool: ' + str(ar2dtool)
        widoco = onto + '-widoco' in data
        print 'widoco: ' + str(widoco)
        oops = onto + '-oops' in data
        print 'oops: ' + str(oops)
        print 'will call get_conf'
        new_conf = get_conf(ar2dtool, widoco, oops)
        print 'will call update_file'
        o = 'OnToology' + onto + '/OnToology.cfg'
        try:
            print "target_repo <%s> ,  path <%s> ,  message <%s> ,   content <%s>" % (
                data['repo'], o, 'OnToology Configuration', new_conf)
            update_file(data['repo'], o, 'OnToology Configuration', new_conf)
        except Exception as e:
            print 'Error in updating the configuration: ' + str(e)
            return render(request, 'msg.html', {'msg': str(e)})
        print 'returned from update_file'
    print 'will return msg html'
    return HttpResponseRedirect('/profile')


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


@login_required
def delete_repo(request):
    repo = request.GET['repo']
    user = OUser.objects.get(email=request.user.email)
    for r in user.repos:
        if r.url == repo:
            try:
                user.update(pull__repos=r)
                user.save()
                # for now we do not remove teh webhook for the sake of students
                # remove_webhook(repo, host + "/add_hook")
                return JsonResponse({'status': True})
            except Exception as e:
                print "error deleting the webhook: " + str(e)
                return JsonResponse({'status': False, 'error': str(e)})
    return JsonResponse({'status': False, 'error': 'You should add this repo first'})


@login_required
def previsual_toggle(request):
    user = OUser.objects.get(email=request.user.email)
    target_repo = request.GET['target_repo']
    found = False
    for repo in user.repos:
        if target_repo == repo.url:
            found = True
            target_repo = repo
            break
    if found:
        target_repo.previsual = not target_repo.previsual
        target_repo.save()
    return HttpResponseRedirect('/profile')


@login_required
def renew_previsual(request):
    user = OUser.objects.get(email=request.user.email)
    target_repo = request.GET['target_repo']
    found = False
    repo = None
    for r in user.repos:
        if target_repo == r.url:
            found = True
            repo = r
            break
    if found:
        repo.state = 'Generating Previsualization'
        repo.notes = ''
        repo.previsual_page_available = True
        repo.save()
        autoncore.prepare_log(user.email)
        # cloning_repo should look like 'git@github.com:AutonUser/target.git'
        cloning_repo = 'git@github.com:%s.git' % target_repo
        sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
        folder_name = 'prevclone-' + sec
        clone_repo(cloning_repo, folder_name, dosleep=True)
        repo_dir = os.path.join(autoncore.home, folder_name)
        msg = previsual.start_previsual(repo_dir, target_repo)
        if msg == "":  # not errors
            repo.state = 'Ready'
            repo.save()
            return HttpResponseRedirect('/profile')
        else:
            repo.notes = msg
            repo.state = 'Ready'
            repo.save()
            return render(request, 'msg.html', {'msg': msg})
    repo.state = 'Ready'
    repo.save()
    return render(request, 'msg.html',
                  {'msg': 'You should add the repo while you are logged in before the revisual renewal'})


def stepbystep(request):
    return render(request, 'stepbystep.html')


def about(request):
    return render(request, 'about.html')


@login_required
def superadmin(request):
    if request.user.email not in ['ahmad88me@gmail.com']:
        return HttpResponseRedirect('/')
    if 'newstatus' in request.POST:
        new_status = request.POST['newstatus']
        for r in Repo.objects.all():
            r.state = new_status
            r.save()
        return render(request, 'superadmin.html', {'msg': 'statuses of all repos are changed to: ' + new_status})

    return render(request, 'superadmin.html')


@login_required
def get_bundle(request):
    ontology = request.GET['ontology']
    repo = request.GET['repo']
    r = Repo.objects.filter(url=repo)
    if len(r) == 0:
        return render(request, 'msg.html', {'msg': 'Invalid repo'})
    elif r[0] not in request.user.repos:
        return render(request, 'msg.html', {'msg': 'Please add this repo first'})
    r[0].notes = ''
    r[0].save()
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(3)])
    folder_name = 'bundle-' + sec
    repo_dir = os.path.join(autoncore.home, folder_name)
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    os.makedirs(repo_dir)
    if ontology[0] == '/':
        ontology = ontology[1:]
    oo = os.path.join('OnToology', ontology)
    print 'oo: %s' % oo
    zip_dir = generate_bundle(base_dir=repo_dir, target_repo=repo, ontology_bundle=oo)
    if zip_dir is None:
        return render(request, 'msg.html', {'msg': 'error generating the bundle'})
    else:
        with open(zip_dir, 'r') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="%s"' % zip_dir.split('/')[-1]
        return response


@login_required
def get_outline(request):
    repos = []
    o_pairs = []
    for r in request.user.repos:
        if r.progress != 100:
            repos.append(r)
    for r in repos:
        o_pairs += r.ontology_status_pairs
    stages = {}
    stages_values = {}  # to draw the inner fill
    for i, s in enumerate(OntologyStatusPair.STATUSES):
        stages[s[0]] = []
        stages_values[s[0]] = i + 1

    for sp in o_pairs:
        if sp.status not in stages:
            stages[sp.status] = []
        stages[sp.status].append(sp.name)

    inner = 0
    if len(o_pairs) > 0:
        inner = min([stages_values[sp.status] for sp in o_pairs])
    return JsonResponse({"stages": stages, "inner": inner})


@login_required
def progress_page(request):
    return render(request, 'progress.html', {'repos': request.user.repos})


def handler500(request):
    return render(request, 'error.html', {'error_code': 500}, status=500)


def faqs(request):
    return render(request, 'faqs.html')


@login_required
def show_repos_list(request):
    if request.user.email in get_managers():
        return render(request, 'show_repos_list.html', {'repos': Repo.objects.all()})
    return HttpResponseRedirect('/')


@login_required
def get_repos_list_file(request):
    if request.user.email in get_managers():
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="repos.csv"'
        writer = csv.writer(response)
        for r in Repo.objects.all():
            writer.writerow([r.url])
        return response
    return HttpResponseRedirect('/')


def get_managers():
    return ['mpovedavillalon' + '@gmail.com', 'ahmad88me' + '@gmail.com']


@login_required
def publish_view(request):
    if 'name' not in request.GET:
        return HttpResponseRedirect('/')
    if 'repo' not in request.GET:
        return HttpResponseRedirect('/')
    if 'ontology' not in request.GET:
        return HttpResponseRedirect('/')
    name = request.GET['name']
    target_repo = request.GET['repo']
    ontology_rel_path = request.GET['ontology']
    # request.GET['target_repo'] = target_repo
    # error_msg = autoncore.previsual(user=OUser.objects.get(email=request.user.email),
    #                                 target_repo=target_repo, ontology_rel_path=ontology_rel_path)
    if 'virtual_env_dir' in os.environ:
        comm = "%s %s " % \
               (os.path.join(os.environ['virtual_env_dir'], 'bin', 'python'),
                (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'autoncore.py')))
    else:
        comm = "python %s " % \
               (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'autoncore.py'))
    comm += ' --target_repo "' + target_repo + '" --useremail "' + user.email + '" --ontology_rel_path "'
    comm += ontology_rel_path + '" ' + '--publishname "' + name + '" --previsual'
    try:
        subprocess.Popen(comm, shell=True)
        msg = '''%s is published successfully. This might take a few minutes for the published ontology to be
            available for GitHub pages''' % ontology_rel_path
    except Exception as e:
        print "publish_view> error : %s" % str(e)
        msg = "Error publishing your ontology. Please contact us to fix it."
    return render(request, 'msg.html', {'msg': msg})

    # if error_msg=="":
    #     error_msg = autoncore.publish(name=name, target_repo=target_repo, ontology_rel_path=ontology_rel_path, user=request.user)
    #     if error_msg == "":
    #         return render(request, 'msg.html', {
    #             'msg': '''%s is published successfully. This might take a few minutes for the published ontology to be
    #             available for GitHub pages''' % ontology_rel_path})
    # return render(request, 'msg.html', {'msg': error_msg})


def htaccess_github_rewrite(htaccess_content, target_repo, ontology_rel_path):
    """
    :param htaccess_content:
    :param target_repo: username/reponame
    :param ontology_rel_path: without leading or trailing /
    :return: htaccess with github rewrite as the domain
    """
    rewrites = [
        "RewriteRule ^$ index-en.html [R=303, L]",
        "RewriteRule ^$ ontology.n3 [R=303, L]",
        "RewriteRule ^$ ontology.xml [R=303, L]",
        "RewriteRule ^$ ontology.ttl [R=303, L]",
        "RewriteRule ^$ 406.html [R=406, L]",
        "RewriteRule ^$ ontology.json [R=303, L]",
        "RewriteRule ^$ ontology.nt [R=303, L]",

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
    new_htaccess = ""
    for line in htaccess_content.split('\n'):
        if line.strip() in rewrites:
            rewr_rule = line.split(' ')
            rewr_rule[2] = base_url + rewr_rule[2]
            new_htaccess += " ".join(rewr_rule) + "\n"
        else:
            if "RewriteRule" in line:
                print "NOTIN: " + line
            new_htaccess += line + "\n"
    return new_htaccess
