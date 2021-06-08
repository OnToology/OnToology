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
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
import requests
import traceback
from github import Github

from OnToology import settings
from OnToology.autoncore import *
from OnToology.models import *
from OnToology import autoncore
from OnToology.settings import host
from Integrator import previsual
from OnToology import rabbit


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


def get_repo_name_from_url(url):
    """
    :param url:
    :return: user/repo (or None if invalid)
    """
    url = url.replace(' ', '')
    #url = url.lower().strip()
    url = url.strip()
    if url[:19] == "https://github.com/":
        name = url[19:]
    else:
        name = url
    print("name: "+name)
    if name[-1] == "/":
        name = name[:-1]
    print(len(name.split('/')))
    if len(name.split('/')) == 2:
        return name
    return None


def home(request):
    global client_id, client_secret, is_private
    sys.stdout.flush()
    sys.stderr.flush()
    if 'target_repo' in request.GET:
        print("we are inside")
        target_repo = request.GET['target_repo']
        repo_name = get_repo_name_from_url(target_repo)
        if repo_name is None:
            return render(request, 'msg.html', {'msg': 'please enter a valid repo'})
        init_g()
        # if not has_access_to_repo(target_repo):# this for the organization
        # return render(request,'msg.html',{'msg': 'repos under organizations are not supported at the moment'})
        wgets_dir = os.environ['wget_dir']
        if call('cd %s; wget %s;' % (wgets_dir, 'http://github.com/' + repo_name.strip()), shell=True) == 0:
            is_private = False
            client_id = client_id_public
            client_secret = client_secret_public
        else:
            is_private = True
            client_id = client_id_private
            client_secret = client_secret_private
            msg = """ Private repos are not currently supported. You can make your private repos public and enjoy
            the functionalities of OnToology """
            return render(request, 'msg.html',  {'msg': msg})
        webhook_access_url, state = webhook_access(client_id, host + '/get_access_token', isprivate=is_private)
        request.session['target_repo'] = repo_name
        request.session['state'] = state
        request.session['access_token_time'] = '1'
        return HttpResponseRedirect(webhook_access_url)
    repos = Repo.objects.order_by('-last_used')[:10]
    num_of_users = len(OUser.objects.all())
    num_of_repos = len(Repo.objects.all())
    try:
        is_manager =  request.user.email in get_managers()
    except:
        is_manager = False
    return render(request, 'home.html', {'repos': repos, 'user': request.user, 'num_of_users': num_of_users,
                                         'num_of_repos': num_of_repos, 'manager': is_manager, 'stats': read_stats()})

def read_stats():
    stats_dir = os.path.join(settings.BASE_DIR, 'templates', 'stats.js')
    f = open(stats_dir)
    j = json.loads(f.read().replace('var stats =', ''))
    return {
        'users' : j['num_of_reg_users'],
        'repos': j['num_of_repos'],
        'pubs': j['num_of_pub']
    }


@login_required
def get_ontologies(request):
    user = request.user
    if 'branch' in request.GET and 'repo' in request.GET:
        branch = request.GET['branch'].strip()
        repo_url = request.GET['repo'].strip()
        repos = user.repos.filter(url=repo_url)
        if len(repos) == 0:
            return JsonReponse({'error': 'This repo does not belong to your user account. Make sure to add it.'}, status=400)
        else:
            try:
                print("going for: parse_online_repo_for_ontologies")
                ontologies = parse_online_repo_for_ontologies(repo_url, branch)
                print("ontologies: ")
                print(ontologies)
                print("add themis results")
                add_themis_results(repo_url, branch, ontologies)
                j = {'ontologies': ontologies}
                return JsonResponse(j)
            except Exception as e:
                #traceback.print_exc()
                print("Exception: "+str(e))
                j = {'error': 'Make sure you have the branch and the repository URL are correct'}
                return JsonResponse(j, status=400)
    else:
        return JsonResponse({'error': 'expecting the branch and repo'}, status=400)

def get_pub_page(repo):
    """
    :param repo: owner/repo-name
    :return:
    """
    wgets_dir = os.environ['wget_dir']
    owner_name, repo_name = repo.split('/')
    pub_page = 'http://%s.github.io/%s/index.html' % (owner_name, repo_name)
    if call('cd %s; wget %s;' % (wgets_dir, pub_page), shell=True) == 0:
        return pub_page
    return None


@login_required
def repos_view(request):
    user = request.user
    if 'repo' in request.GET:
        repo_url = request.GET['repo'].strip()
        branches = get_repo_branches(repo_url)
        if 'gh-pages' in branches:
            branches.remove('gh-pages')
        if 'branch' in request.GET:
            branch = request.GET['branch'].strip()
        else:
            branch = branches[0]
        pub_page = get_pub_page(repo_url)
        if not pub_page:
            pub_page = ""
        repos = user.repos.filter(url=repo_url)
        if len(repos) == 0:
            return render(request,'msg.html', {'msg': 'This repo does not belong to your user account. Make sure to add it.'})
        return render(request, 'repo.html', {'repo': repos[0], 'branch': branch, 'branches': branches, 'pub_url': pub_page})
    else:
        return render(request, 'repos.html', {'repos': user.repos.all()})


@login_required
def opub_view(request):
    return render(request, 'opub.html', {'opubs': PublishName.objects.filter(user=request.user)})


@login_required
def runs_view(request):
    user = request.user
    try:
        print("in runs view")
        if 'repo' in request.GET:
            print("in request GET")
            repo_name = request.GET['repo'].strip()
            repos = Repo.objects.filter(url=repo_name)
            if len(repos) == 1:
                print("single repo")
                repo = repos[0]
                if repo not in user.repos.all():
                    return render(request,'msg.html', {'msg': 'This repo does not belong to the loggedin user. Try to add it and try again.'})
                now_timestamp = timezone.now()
                latest_oruns = ORun.objects.filter(repo=repo)
                print("going to render")
                return render(request, 'runs.html', {'oruns': latest_oruns})
            else:
                print("runs_view> repo <"+str(repo_name)+"> does not exist for user: "+str(user))
        else:
            return render(request, 'user_repos.html', {'repos': user.repos.all()})
    except Exception as e:
        print("runs_view> exception: "+str(e))
    return HttpResponseRedirect(reverse('profile'))


def grant_update(request):
    return render(request, 'msg.html', {'msg': 'Magic is done'})


def get_access_token(request):
    print("get_access_token")
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
        print("Exception: %s" % str(e))
        print("response: %s" % str(res.text))
        return render(request, 'msg.html', {'msg':'Error getting the token from GitHub. please try again or contact us'})
    if 'access_token' not in d:
        print('access_token is not there')
        print(d)
        return HttpResponseRedirect('/')

    access_token = d['access_token']
    request.session['access_token'] = access_token
    update_g(access_token)
    print('access_token: ' + access_token)

    if request.user.is_authenticated and request.session['access_token_time'] == '1':
        request.session['access_token_time'] = '2'  # so we do not loop
        webhook_access_url, state = webhook_access(client_id, host + '/get_access_token', is_private)
        request.session['state'] = state
        return HttpResponseRedirect(webhook_access_url)

    rpy_wh = add_webhook(request.session['target_repo'], host + "/add_hook")
    rpy_coll = add_collaborator(request.session['target_repo'], ToolUser)
    error_msg = ""
    if rpy_wh['status'] == False:
        error_msg += str(rpy_wh['error'])
        print('error adding webhook: ' + error_msg)
    if rpy_coll['status'] == False:
        error_msg += str(rpy_coll['error'])
        print('error adding collaborator: ' + rpy_coll['error'])
    else:
        print('adding collaborator: ' + rpy_coll['msg'])
    if error_msg != "":
        if 'Hook already exists on this repository' in error_msg:
            error_msg = 'This repository already watched'
        elif '404' in error_msg:  # so no enough access according to Github troubleshooting guide
            error_msg = """You don\'t have permission to add collaborators and create webhooks to this repo or this
            repo does not exist. Note that if you can fork this repo, you can add it here"""
            return render(request, 'msg.html', {'msg': error_msg})
        else:
            print("error message not hook and not 404: " + error_msg)
            print("target repo: " + request.session['target_repo'])
            print("ToolUser: " + ToolUser)
        msg = error_msg
    else:
        msg = '''webhook attached and user added as collaborator, Note that generating the documentation,
         diagrams and evaluation report takes sometime to be generated. In "My repositories" page, you can see the
          status of each repo.'''
    target_repo = request.session['target_repo']
    try:
        repo = Repo.objects.get(url=target_repo)
    except Exception as e:
        print(str(e))
        repo = Repo()
        repo.url = target_repo
        repo.save()
    if request.user.is_authenticated:
        ouser = OUser.objects.get(email=request.user.email)
        if repo not in ouser.repos.all():
            ouser.repos.add(repo)
            ouser.save()
            # generateforall(repo.url, ouser.email, branch)
    return render(request, 'msg.html',  {'msg': msg})


def get_changed_files_from_payload(payload):
    commits = payload['commits']
    changed_files = []
    for c in commits:
        changed_files += c["added"] + c["modified"]
    return changed_files


@csrf_exempt
def add_hook(request):
    print("in add hook function")
    print("method: "+request.method)
    print("body: ")
    print(request.body)
    print("header: ")
    print(request.headers)
    changed_files = []
    if settings.test_conf['local']:
        print('We are in test mode')
    try:
        print("\n\nPOST DATA\n\n: " + str(request.POST))
        s = str(request.POST['payload'])
        print("payload: " + s)
        j = json.loads(s, strict=False)
        print("json is loaded")
        if "ref" in j:
            branch = j["ref"].split("/")[-1]
            if branch == "gh-pages":
                print("it is just gh-pages")
                return render(request, 'msg.html', {'msg': 'it is gh-pages, so nothing'})
            else:
                s = j['repository']['url'] + 'updated files: ' + str(j['head_commit']['modified'])
                print("just s: " + str(s))
                target_repo = j['repository']['full_name']
                user = j['repository']['owner']['email']
                print("target_repo: " + str(target_repo))
                print("user email: " + str(user))
                changed_files = get_changed_files_from_payload(j)
                print("early changed files: " + str(changed_files))
                if 'Merge pull request' in j['head_commit']['message'] or \
                        'OnToology Configuration' == j['head_commit']['message'] or \
                        'OnToology Publish' == j['head_commit']['message']:
                    print('This is a merge request or Configuration push')
                    try:
                        repo = Repo.objects.get(url=target_repo)
                        print('got the repo')
                        repo.last_used = timezone.now()
                        repo.progress = 100.0
                        repo.save()
                        print('repo saved')
                    except Model.DoesNotExist:
                        repo = Repo()
                        repo.url = target_repo
                        repo.save()
                    except Exception as e:
                        print('database_exception: ' + str(e))
                        traceback.print_exc()
                    msg = 'This indicate that this merge request will be ignored'
                    print(msg)
                    if settings.test_conf['local']:
                        print(msg)
                        return
                    else:
                        return render(request, 'msg.html', {'msg': msg})
    except Exception as e:
        print("add hook exception: " + str(e))
        traceback.print_exc()
        msg = 'This request should be a webhook ping'
        if settings.test_conf['local']:
            print(msg)
            return JsonResponse({'status': False, 'error': str(e)})
        else:
            return JsonResponse({'status': False, 'error': str(e)})
    try:
        print('##################################################')
        print('changed_files: ' + str(changed_files))
        j = {
            'action': 'magic',
            'repo': target_repo,
            'branch': branch,
            'useremail': user,
            'changedfiles': changed_files,
            'created': str(timezone.now()),
        }
        rabbit.send(j)
    except Exception as e:
        error_msg = str(e)
        print('error running generall all subprocess: ' + error_msg)
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        if 'execv() arg 2 must contain only strings' in error_msg:
            error_msg = 'make sure that your repository filenames does not have accents or special characters'
        else:
            error_msg = 'generic error, please report the problem to us ontoology@delicias.dia.fi.upm.es'
        s = error_msg
    return JsonResponse({'status': True})
    # return render(request, 'msg.html', {'msg': '' + s}, )


@login_required
def generateforall_view(request):
    if 'repo' not in request.GET:
        return HttpResponseRedirect('/')
    if 'branch' not in request.GET:
        return render(request, 'msg.html', {'msg': 'A beanch is expected as a GET parameter'})
    target_repo = request.GET['repo'].strip()
    branch = request.GET['branch'].strip()
    found = False
    if target_repo[-1] == '/':
        target_repo = target_repo[:-1]
    print('target_repo is <%s>' % target_repo)
    print("branch: <%s>" % (branch))
    # The below couple of lines are to check that the user currently have permission over the repository
    try:
        ouser = OUser.objects.get(email=request.user.email)
        for r in ouser.repos.all():
            if r.url == target_repo:
                found = True
                break
    except:
        return render(request, 'msg.html', {'msg': 'Please contact ontoology@delicias.dia.fi.upm.es'})
    if not found:
        return render(request, 'msg.html',
                      {'msg': 'You need to register/watch this repository while you are logged in'})
    try:
        res = generateforall(target_repo, request.user.email, branch)
    except Exception as e:
        print("generateforall_view exception: "+str(e))
        return render(request, 'msg.html', {'msg':  'Internal error in generating the resources'})
    if res['status'] is True:
        return render(request, 'msg.html',  {
            'msg': 'Soon you will find generated files included in a pull request in your repository. Once the pull request is generated, you can merge it using GitHub Merge function. If the resources (e.g., documentation, evaluation, ...) are not generated within a few minutes, you can contact us.'},)
    else:
        return render(request, 'msg.html', {'msg': res['error']})


def generateforall(target_repo, user_email, branch):
    user = user_email
    ontologies = get_ontologies_in_online_repo(target_repo)
    changed_files = ontologies
    print('current file dir: %s' % str(os.path.dirname(os.path.realpath(__file__))))

    try:
        r = Repo.objects.get(url=target_repo)
    except Exception as e:
        print(str(e))
        return {'status': False}
    if settings.test_conf['local']:
        print("running autoncode in the same thread")
        j = {
            'action': 'magic',
            'repo': target_repo,
            'branch': branch,
            'useremail': user,
            'changedfiles': changed_files,
            'created': str(timezone.now()),
        }
        rabbit.send(j)
    else:
        try:
            j = {
                'action': 'magic',
                'repo': target_repo,
                'branch': branch,
                'useremail': user,
                'changedfiles': changed_files,
                'created': str(timezone.now()),
            }
            rabbit.send(j)
        except Exception as e:
            sys.stdout.flush()
            sys.stderr.flush()
            error_msg = str(e)
            print('error running generall all subprocess: ' + error_msg)
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
    print('******* login *********')
    redirect_url = host + '/login_get_access'
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
    request.session['state'] = sec
    scope = 'user:email'  # get_proper_scope_to_login(username)
    # scope = 'admin:org_hook'
    # scope+=',admin:org,admin:public_key,admin:repo_hook,gist,notifications,delete_repo,repo_deployment,repo,public_repo,user,admin:public_key'
    redirect_url = "https://github.com/login/oauth/authorize?client_id=" + client_id_login + "&redirect_uri=" +\
                   redirect_url + "&scope=" + scope + "&state=" + sec
    return HttpResponseRedirect(redirect_url)


def logout(request):
    print('*** logout ***')
    django_logout(request)
    return HttpResponseRedirect('/')


def login_get_access(request):
    print('*********** login_get_access ************')
    if 'state' not in request.session:
        request.session['state'] = 'blah123'  # 'state'
    if request.GET['state'] != request.session['state']:
        print("login_get_access> get state: <%s> and session <%s>" % (request.GET['state'], request.session['state']))
        #return HttpResponseRedirect('/')
        return render(request, 'msg.html', {'msg': 'session is expired. Try to login again.'})
    data = {
        'client_id': client_id_login,
        'client_secret': client_secret_login,
        'code': request.GET['code'],
        'redirect_uri': host  # host+'/add_hook'
    }
    res = requests.post('https://github.com/login/oauth/access_token', data=data)
    print("response: ")
    print(res.text)
    atts = res.text.split('&')
    d = {}
    try:
        for att in atts:
            keyv = att.split('=')
            d[keyv[0]] = keyv[1]
        access_token = d['access_token']
        request.session['access_token'] = access_token
        print('access_token: ' + access_token)
    except Exception as e:
        print("exception: " + str(e))
        print("no access token")
        print("response: %s" % res.text)
        return render(request, 'msg.html', {'msg': 'Missing token from Github API. Try to login again'})

    g = Github(access_token)
    email = g.get_user().email
    username = g.get_user().login
    if email == '' or type(email) == type(None):
        return render(request, 'msg.html', {'msg': 'You have to make you email public and try again'})
    request.session['avatar_url'] = g.get_user().avatar_url
    print('avatar_url: ' + request.session['avatar_url'])
    try:
        print("looking for email: <%s>" % (str(email)))
        user = OUser.objects.get(email=email)
        user.username = username
        user.save()
    except Exception as e:
        try:
            print("number of users: %d" % (len(OUser.objects.all())))
            print("Exception: %s" % (str(e)))
            print("looking for username: <%s>" % (str(username)))
            user = OUser.objects.get(username=username)
            user.email = email
            user.save()
        except:
            print("Exception: %s" % (str(e)))
            print('<%s,%s>' % (email, username))
            # The password is never important but we set it here because it is required by User class
            print("Now will create the user: ")
            print("username: "+username)
            print("password: "+request.session['state'])
            print("email: "+email)
            user = OUser.objects.create_user(username=username, password=request.session['state'], email=email)
            user.save()
    django_login(request, user)
    print('The used access_token: ' + access_token)
    sys.stdout.flush()
    sys.stderr.flush()
    return HttpResponseRedirect('/')


@login_required
def profile(request):
    print('************* profile ************')
    print(str(timezone.now()))
    error_msg = ''
    user = request.user
    if 'repo' in request.GET and 'name' not in request.GET:  # asking for ontologies in a repo
        repo = request.GET['repo']
        print('repo :<%s>' % (repo))
        print('got the repo')
        try:
            print('trying to validate repo')
            hackatt = True
            for repooo in user.repos.all():
                if repooo.url == repo:
                    hackatt = False
                    break
            if hackatt:  # trying to access a repo that does not belong to the use currently logged in
                return render(request, 'msg.html', {'msg': 'This repo is not added, please do so in the main page'})
            print('try to get abs folder')
            if type(autoncore.g) == type(None):
                print('access token is: ' + request.session['access_token'])
                update_g(request.session['access_token'])
            try:
                ontologies = parse_online_repo_for_ontologies(repo)
                ontologies = autoncore.add_themis_results(repo, ontologies)
                print('ontologies: ' + str(len(ontologies)))
                arepo = Repo.objects.get(url=repo)
                pnames = PublishName.objects.filter(user=user, repo=arepo)
                for o in ontologies:
                    print('--------\n%s\n' % o)
                    o['published'] = False
                    o['pname'] = ''
                    for pn in pnames:
                        if pn.ontology == o['ontology']:  # to compare without the leading /
                            o['published'] = True
                            o['pname'] = pn.name
                            break
                    for d in o:
                        print('   ' + d + ': ' + str(o[d]))
                print('testing redirect')
                print('will return the Json')
                jresponse = JsonResponse({'ontologies': ontologies})
                jresponse.__setitem__('Content-Length', len(jresponse.content))
                sys.stdout.flush()
                sys.stderr.flush()
                return jresponse
            except Exception as e:
                print("exception in getting the ontologies for the repo: " + str(repo))
                print("exception:  " + str(e))
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
            print('exception: ' + str(e))

    # elif 'delete-name' in request.GET:
    #     name = request.GET['delete-name']
    #     p = PublishName.objects.filter(name=name)
    #     if len(p) == 0:
    #         error_msg += 'This name is not reserved'
    #     elif p[0].user.id == user.id:
    #         pp = p[0]
    #         pp.delete()
    #         pp.save()
    #         comm = 'rm -Rf ' + os.path.join(publish_dir, name)
    #         call(comm, shell=True)
    #     else:
    #         error_msg += 'You are trying to delete a name that does not belong to you'
    print('testing redirect')
    repos = user.repos.all()
    for r in repos:
        try:
            if len(r.url.split('/')) != 2:
                user.repos.remove(r)
                r.delete()
                user.save()
                continue
            r.user = r.url.split('/')[0]
            r.rrepo = r.url.split('/')[1]
        except:
            user.repos.remove(r)
            user.save()
    request.GET = []
    sys.stdout.flush()
    sys.stderr.flush()

    if request.user.email in get_managers():
        num_pending_msgs = rabbit.get_pending_messages()
        num_of_rabbit_processes = get_num_of_processes_of_rabbit()
    else:
        num_pending_msgs = -2
        num_of_rabbit_processes = -2

    return render(request, 'profile.html', {'repos': repos, 'pnames': PublishName.objects.filter(user=user),
                                            'num_pending_msgs': num_pending_msgs,
                                            'num_of_rabbit_processes': num_of_rabbit_processes,
                                            'error': error_msg, 'manager': request.user.email in get_managers()})


def get_num_of_processes_of_rabbit():
    import os
    out = os.popen('ps -ef | grep rabbit.py').read()
    lines = out.split('\n')
    one = False
    for line in lines:
        if 'python' in line and 'rabbit.py' in line:
            print("line: ")
            print(line)
            p_tokens = line.split('rabbit.py')
            if len(p_tokens) > 1:
                tokens = p_tokens[1].strip().split(' ')
                if tokens[0].strip().isdigit():
                    return int(tokens[0].strip())
                else:
                    print("ptokens: ")
                    print(p_tokens)
                    print("tokens: ")
                    print(tokens)
                    # return 1
                    one = True
    if one:
        return 1
    return -1


def update_conf(request):
    print('inside update_conf')
    if request.method == "GET":
        return render(request, "msg.html", {"msg": "This method expects POST only"})
    ontologies = request.POST.getlist('ontology')
    data = request.POST
    target_repo = data['repo'].strip()
    j = {
        'action': 'change_conf',
        'repo': target_repo,
        'useremail': request.user.email,
        'ontologies': ontologies,
        'data': data,
        'created': str(timezone.now()),
    }
    rabbit.send(j)
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
    for r in user.repos.all():
        if r.url == repo:
            try:
                user.update(pull__repos=r)
                user.save()
                # for now we do not remove the webhook for the sake of students
                # remove_webhook(repo, host + "/add_hook")
                return JsonResponse({'status': True})
            except Exception as e:
                print("error deleting the webhook: " + str(e))
                return JsonResponse({'status': False, 'error': str(e)})
    return JsonResponse({'status': False, 'error': 'You should add this repo first'})


@login_required
def previsual_toggle(request):
    # user = OUser.objects.get(email=request.user.email)
    # target_repo = request.GET['target_repo']
    # found = False
    # for repo in user.repos.all():
    #     if target_repo == repo.url:
    #         found = True
    #         target_repo = repo
    #         break
    # if found:
    #     # target_repo.previsual = not target_repo.previsual
    #     target_repo.save()
    return HttpResponseRedirect('/profile')


@login_required
def renew_previsual(request):
    user = OUser.objects.get(email=request.user.email)
    target_repo = request.GET['target_repo']
    found = False
    repo = None
    for r in user.repos.all():
        if target_repo == r.url:
            found = True
            repo = r
            break
    if found:
        repo.state = 'Generating Previsualization'
        repo.notes = ''
        # repo.previsual_page_available = True
        repo.save()
        autoncore.prepare_log(user.email)
        # cloning_repo should look like 'git@github.com:user/target.git'
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
    if 'ontology' in request.GET and 'repo' in request.GET and 'branch' in request.GET:
        try:
            ontology = request.GET['ontology']
            repo = request.GET['repo']
            branch = request.GET['branch']
            r = Repo.objects.filter(url=repo)
            if len(r) == 0:
                return render(request, 'msg.html', {'msg': 'Invalid repo'})
            elif r[0] not in request.user.repos.all():
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
            print('oo: %s' % oo)
            zip_dir = generate_bundle(base_dir=repo_dir, target_repo=repo, ontology_bundle=oo, branch=branch)
            if zip_dir is None:
                return render(request, 'msg.html', {'msg': 'error generating the bundle'})
            else:
                with open(zip_dir, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename="%s"' % zip_dir.split('/')[-1]
                return response
        except Exception as e:
            print("Exception in get_bundle> "+str(e))
            traceback.print_exc()
            return render(request, 'msg.html', {'msg': 'Error getting the bundle. You can contact us to resolve this issue'})
    else:
        return render(request, 'msg.html', {'msg': 'Expects the repo, the branch, and the ontology'})

@login_required
def delete_published(request):
    name = request.GET['name']
    p = PublishName.objects.filter(name=name)
    if len(p) == 0:
        msg = 'This name is not reserved'
    elif p[0].user.id == request.user.id:
        pp = p[0]
        pp.delete()
        comm = 'rm -Rf ' + os.path.join(publish_dir, name)
        call(comm, shell=True)
        msg = "The reserved name is deleted successfully"
    else:
        msg = 'You are trying to delete a name that does not belong to you'
    return render(request,'msg.html', {'msg': msg})


@login_required
def get_outline(request):
    try:
        repos = []
        o_pairs = []
        for r in request.user.repos.all():
            if r.progress != 100:
                repos.append(r)
        for r in repos:
            for onto_pair in r.ontology_status_pairs.all():
                o_pairs.append(onto_pair)

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
    except Exception as e:
        print("Getting exceptions")
        print("get_outline exception: "+str(e))
        traceback.print_exc()
        # raise Exception(str(e))
        return JsonResponse({'error': 'Internal error'}, status=500)

@login_required
def progress_page(request):
    return render(request, 'progress.html', {'repos': request.user.repos.all()})


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


@login_required
def update_stats_view(request):
    if request.user.email not in get_managers():
        return render(request, 'msg.html', {'msg': 'This functionality is only available for the admins'})
    else:
        comm = "%s %s " % \
               (os.path.join(os.environ['virtual_env_dir'], 'bin', 'python'),
                (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cmd.py updatestats')))

        subprocess.Popen(comm, shell=True)
        return render(request, 'msg.html', {'msg': 'The stats file is being updated'})


def show_stats(request):
    return render(request, 'stats.html')


def get_managers():
    return ['mpovedavillalon' + '@gmail.com', 'ahmad88me' + '@gmail.com']


@login_required
def publish_view(request):
    if 'name' not in request.GET:
        print("missing name")
        return HttpResponseRedirect('/')
    if 'repo' not in request.GET:
        print("missing repo")
        return HttpResponseRedirect('/')
    if 'ontology' not in request.GET:
        print("missing ontology")
        return HttpResponseRedirect('/')
    if 'branch' not in request.GET:
        print("missing branch")
        return HttpResponseRedirect('/')
    name = request.GET['name'].strip()
    target_repo = request.GET['repo'].strip()
    ontology_rel_path = request.GET['ontology'].strip()
    branch = request.GET['branch'].strip()
    print("name: "+name)
    pns = PublishName.objects.filter(name=name)
    if len(pns)> 0:
        return JsonResponse({'msg': 'This name is already taken, try to choose another name'}, status=400)
    try:
        j = {
            'action': 'publish',
            'repo': target_repo,
            'branch': branch,
            'useremail': request.user.email,
            'ontology_rel_path': ontology_rel_path,
            'name': name,
            'created': str(timezone.now()),
        }
        rabbit.send(j)
        msg = '''<i>%s</i> will be published soon. This might take a few minutes for the published ontology to be
            available for GitHub pages. If it is not published within a few minutes you can contact us.''' % ontology_rel_path[1:]
        return JsonResponse({'msg': msg})
        # return render(request, 'msg.html', {'msg': msg, 'img': 'https://github.com/OnToology/OnToology/raw/master/media/misc/gh-pages.png'})
    except Exception as e:
        print("publish_view> error : %s" % str(e))
        msg = "Error publishing your ontology. Please contact us to fix it."
        # return render(request, 'msg.html', {'msg': msg})
        return JsonResponse({'msg': msg}, status=500)

@login_required
def syntax_check_view(request):
    import rdflib
    valid_formats = ["xml", "n3", "turtle", "nt", "pretty-xml", "trix", "trig", "nquads"]
    if 'url' not in request.GET:
        return render(request, 'syntax.html', {'formats': valid_formats})
    if 'format' not in request.GET:
        return render(request, 'syntax.html', {'error': 'Format is expected','formats': valid_formats})
        # return render(request, 'msg.html', {'msg': 'Format is expected'})
    # if 'url' not in request.GET:
    #     return render(request, 'msg.html', {'msg': 'url is expected'})
    format = request.GET['format']
    url = request.GET['url']
    if format not in valid_formats:
        return render(request, 'syntax.html', {'error': '<%s> format is not supported'%format, 'formats': valid_formats})
        # return render(request, 'msg.html', {'msg': '<%s> format is not supported'})
    if 'https://' not in url[:8] and 'http://' not in url[:7]:
        return render(request, 'syntax.html', {'error': 'Invalid URL', 'formats': valid_formats})
        # return render(request, 'msg.html', {'msg': 'Invalid URL'})
    g = rdflib.Graph()
    try:
        g.parse(url, format=format)
        return render(request, 'syntax.html', {'msg': 'The syntax of the ontology is correct', 'formats': valid_formats})
    except Exception as e:
        return render(request, 'syntax.html',
                      {'formats': valid_formats,
                        'error': 'The syntax of the ontology is incorrect. The error message is: '+str(e)})

def publications(request):
    return render(request, 'publications.html')


def error_test(request):
    raise Exception("error")
    return render(request, 'msg.html',  {'msg': 'expecting an exception'})


@login_required
def get_branches(request):
    if 'repo' not in request.GET:
        return JsonReponse({'error': 'repo is not passed'}, status=400)
    try:
        repo = request.GET['repo'].strip()
        #branches = [str(i)+"-abc" for i in range(20)]
        branches = get_repo_branches(repo)
        return JsonResponse({'branches': branches})
    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'Internal Error: %s' % str(e)}, status=500)


