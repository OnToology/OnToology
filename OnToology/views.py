from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from mongoengine.django.auth import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
import settings


import string
import random
from datetime import datetime
from autoncore import git_magic, add_webhook,ToolUser, webhook_access, update_g, add_collaborator, get_auton_configuration, clone_repo, prepare_log
from models import *
import requests
import json
import os
import sys
import subprocess

from github import Github
from settings import client_id,client_secret, host



# client_id = settings.GITHUB_APP_ID#'bbfc39dd5b6065bbe53b'
# client_secret = settings.GITHUB_API_SECRET#'60014ba718601441f542213855607810573c391e'
# host = 'http://54.172.63.231'
# local=False
# if 'OnToology_home' in os.environ and os.environ['OnToology_home'].lower()=="true":
#     local=True
#     host = 'http://127.0.0.1'
#     client_id = ''




def get_repos_formatted(the_repos):
    repos = []
    for orir in the_repos:
        r = {}
        for ke in orir:
            r[ke]  = orir[ke]
        tools = r['monitoring'].split(",")
        monit=""
        for t in tools:   
            keyval = t.split("=")
            if len(keyval) != 2:
                break
            if keyval[1].lower().strip()=='true':
                keyval[1]='Yes'
            else:
                keyval[1]='No'
            print r['url']+" "+keyval[0]+"="+str(keyval[1])
            r[keyval[0].strip()]=keyval[1]
            monit+="=".join(keyval) +","
        r['monitoring'] = monit
        repos.append(r)
    return repos




def home(request):
    if 'target_repo' in request.GET:
        #print request.GET
        target_repo = request.GET['target_repo']
        webhook_access_url, state = webhook_access(client_id,host+'/get_access_token')
        request.session['target_repo'] = target_repo
        request.session['state'] = state 
        
        try: 
            repo = Repo.objects.get(url=target_repo)
        except Exception as e:
            print str(e)
            repo = Repo()
            repo.url=target_repo
            repo.save()
            
        if request.user.is_authenticated():
            ouser = OUser.objects.get(email=request.user.email)
            ouser.repos.append(repo)
            ouser.save()
        return  HttpResponseRedirect(webhook_access_url)
#     repos = []
#     for orir in Repo.objects.all():
#         r = {}
#         for ke in orir:
#             r[ke]  = orir[ke]
#         tools = r['monitoring'].split(",")
#         monit=""
#         for t in tools:   
#             keyval = t.split("=")
#             if len(keyval) != 2:
#                 break
#             if keyval[1].lower().strip()=='true':
#                 keyval[1]='Yes'
#             else:
#                 keyval[1]='No'
#             print r['url']+" "+keyval[0]+"="+str(keyval[1])
#             r[keyval[0].strip()]=keyval[1]
#             monit+="=".join(keyval) +","
#         r['monitoring'] = monit
#         repos.append(r)
    repos = get_repos_formatted(Repo.objects.all())
#     if not request.user.is_authenticated():
#         request.session['avatar_url'] ='https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png'
        #request.session['avatar_url'] = 'https://assets-cdn.github.com/images/modules/logos_page/Octocat.png'
    #return render_to_response('home.html',{'repos': repos, 'user': request.user, 'avatar_url': request.session['avatar_url']},context_instance=RequestContext(request))
    #return render('home.html',{'repos': repos, 'user': request.user, 'avatar_url': request.session['avatar_url']})
    return render(request,'home.html',{'repos': repos, 'user': request.user })    






def grant_update(request):
    return render_to_response('msg.html',{'msg': 'Magic is done'},context_instance=RequestContext(request))



  
def get_access_token(request):
    if request.GET['state'] != request.session['state']:
        return render_to_response('msg.html',{'msg':'Error, ; not an ethical attempt' },context_instance=RequestContext(request))
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': request.GET['code'],
        'redirect_uri': host+'/add_hook'
    }
    res = requests.post('https://github.com/login/oauth/access_token',data=data)
    atts = res.text.split('&')
    d={}
    for att in atts:
        keyv = att.split('=')
        d[keyv[0]] = keyv[1]
    access_token = d['access_token']
    request.session['access_token'] = access_token
    update_g(access_token)
    print 'access_token: '+access_token
    rpy_wh = add_webhook(request.session['target_repo'], host+"/add_hook")
    rpy_coll = add_collaborator(request.session['target_repo'], ToolUser)
    error_msg = ""
    if rpy_wh['status'] == False:
        error_msg+=str(rpy_wh['error'])
        print 'error adding webhook: '+error_msg
    if rpy_coll['status'] == False:
        error_msg+=str(rpy_coll['error'])
        print 'error adding collaborator: '+rpy_coll['error']
    else:
        print 'adding collaborator: '+rpy_coll['msg']
    if error_msg != "":
        return render_to_response('msg.html',{'msg':error_msg },context_instance=RequestContext(request))
    return render_to_response('msg.html',{'msg':'webhook attached and user added as collaborator' },context_instance=RequestContext(request))
    

      

@csrf_exempt
def add_hook_test(request):
    # cloning_repo should look like 'git@github.com:AutonUser/target.git'
    cloning_repo = 'git://github.com/ahmad88me/target.git'#request.POST['cloning_repo']
    tar = cloning_repo.split('/')[-2]
    cloning_repo = cloning_repo.replace(tar,ToolUser)
    cloning_repo = cloning_repo.replace('git://github.com/','git@github.com:')
    target_repo = 'ahmad88me/target'#request.POST['target_repo']
    user = 'test_user'#request.POST['username']
    changed_files = ['a.txt']
    r = git_magic(target_repo, user, cloning_repo, changed_files)
    s='add_hook_test'
    #request.session['updated_files'] = j['head_commit']['modified']
    return render_to_response('msg.html',{'msg': ''+s+'<>'+r},context_instance=RequestContext(request))



@csrf_exempt
def add_hook(request):
    try:
        s = str(request.POST['payload'])
        j = json.loads(s)
        s = j['repository']['url']+'updated files: '+str(j['head_commit']['modified'])
        cloning_repo = j['repository']['git_url']
        target_repo = j['repository']['full_name']
        user = j['repository']['owner']['email']
        changed_files = j['head_commit']['modified']
        #changed_files+= j['head_commit']['removed']
        changed_files+= j['head_commit']['added']
        if 'Merge pull request' in  j['head_commit']['message'] :
            print 'This is a merge request'
            mont = get_auton_configuration(user)
            s = ""
            print "the configuration: "+str(mont)
            for i in mont:
                s+=i+"="+str(mont[i])+", "
                try:
                    repo = Repo.objects.get(url=target_repo)
                    print 'got the repo'
                    repo.last_used = datetime.today()
                    print 'monitoring is: '+s
                    repo.monitoring = s
                    repo.save()
                    print 'repo saved'
                except DoesNotExist:
                    repo = Repo()
                    repo.url=target_repo
                    repo.monitoring = s
                    repo.save()
                except Exception as e:
                    print 'database_exception: '+str(e)
            return render_to_response('msg.html',{'msg': 'This indicate that this merge request will be ignored'},context_instance=RequestContext(request))
    except:
        return render_to_response('msg.html',{'msg': 'This request should be a webhook ping'},context_instance=RequestContext(request))
    print '##################################################'
    print 'changed_files: '+str(changed_files)
    # cloning_repo should look like 'git@github.com:AutonUser/target.git'
    tar = cloning_repo.split('/')[-2]
    cloning_repo = cloning_repo.replace(tar,ToolUser)
    cloning_repo = cloning_repo.replace('git://github.com/','git@github.com:')
    comm = "python /home/ubuntu/auton/Auton/autoncore.py "
    comm+=' "'+target_repo+'" "'+user+'" "'+cloning_repo+'" '
    for c in changed_files:
        comm+='"'+c+'" '
    print 'running autoncore code as: '+comm
    subprocess.Popen(comm,shell=True)
    r=""
    return render_to_response('msg.html',{'msg': ''+s+'<>'+r},context_instance=RequestContext(request))








##The below line is for login
def login(request):
    redirect_url = host+'/login_get_access'
    sec = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(9)])
    request.session['state'] = sec
    scope = 'admin:org_hook'
    scope+=',admin:org,admin:public_key,admin:repo_hook,gist,notifications,delete_repo,repo_deployment,repo,public_repo,user,admin:public_key'
    redirect_url = "https://github.com/login/oauth/authorize?client_id="+client_id+"&redirect_uri="+redirect_url+"&scope="+scope+"&state="+sec
    return HttpResponseRedirect(redirect_url)



def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/')
    #return render_to_response('msg.html',{'msg':'logged out' },context_instance=RequestContext(request))




def login_get_access(request):
    if request.GET['state'] != request.session['state']:
        return render_to_response('msg.html',{'msg':'Error, ; not an ethical attempt' },context_instance=RequestContext(request))
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': request.GET['code'],
        'redirect_uri': host#host+'/add_hook'
    }
    res = requests.post('https://github.com/login/oauth/access_token',data=data)
    atts = res.text.split('&')
    d={}
    for att in atts:
        keyv = att.split('=')
        d[keyv[0]] = keyv[1]
    access_token = d['access_token']
    request.session['access_token'] = access_token
    g = Github(access_token)
    email = g.get_user().email
    request.session['avatar_url'] = g.get_user().avatar_url
    print 'avatar_url: '+request.session['avatar_url']
    try:
        user = OUser.objects.get(email=email)
        user.backend = 'mongoengine.django.auth.MongoEngineBackend'
        user.save()
    except:#The password is never important but we set it here because it is required by User class
        user = OUser.create_user(email, password=request.session['state'], email=email)
        user.backend = 'mongoengine.django.auth.MongoEngineBackend'
        user.save()
    #user.backend = 'mongoengine.django.auth.MongoEngineBackend'
    django_login(request, user)
    print 'access_token: '+access_token
    return HttpResponseRedirect('/')





@login_required
def profile(request):
    #print '**************************************'
    f=prepare_log('webinterface-'+request.user.email)
    print str(datetime.today())
    print '**************************************'
    print '**************************************'
    print '**************************************'
    ouser = OUser.objects.get(email=request.user.email)
    if 'repo' in request.GET:
        print 'got the repo'
        try:
            print 'trying to validate repo' 
            hackatt = True
            for repo  in  ouser.repos:
                if repo.url == request.GET['repo']:
                    hackatt=False
                    break
            if hackatt: # trying to access a repo that does not belong to the use currently logged in
                return render(request,'msg.html',{'msg': 'This repo is not added, please do so in the main page'})
            print 'try to get abs folder'
            ontologies_abs_folder = clone_repo('git@github.com:'+request.GET['repo'], request.user.email, dosleep=False)
            print 'abs folder: '+ontologies_abs_folder
            ontologies = parse_folder_for_ontologies(ontologies_abs_folder)
            print 'ontologies: '+str(len(ontologies))
            for o in ontologies:
                for d in o:
                    print d+': '+str(o[d])
            sys.stdout= sys.__stdout__
            sys.stderr = sys.__stderr__
            print 'testing redirect'
            f.close()
            return render_to_response('profile.html',{'repos': get_repos_formatted(ouser.repos), 'ontologies': ontologies},context_instance=RequestContext(request))
        except:
            pass
    sys.stdout= sys.__stdout__
    sys.stderr = sys.__stderr__
    print 'testing redirect'
    f.close()
    return render_to_response('profile.html',{'repos': get_repos_formatted(ouser.repos)},context_instance=RequestContext(request))




def parse_folder_for_ontologies(ontologies_abs_folder):        
    ontologies=[] 
    print 'will be searching in: '+ontologies_abs_folder
    for root, dirs, files in os.walk(ontologies_abs_folder):
        for name in files:
            if name=="auton.cfg":
                ontologies.append({'ontology': root})#os.path.join(root, name)})
    for o in ontologies:
        confs = get_auton_configuration(f=None, abs_folder=o['ontology'])
        for c in confs:
            tool = c.replace('_enable','')
            o[tool] = confs[c]
    return ontologies


 
# ontologies=[] 
# print 'will be searching in: '+ontologies_abs_folder
# for root, dirs, files in os.walk(ontologies_abs_folder):
#     for name in files:
#         if name=="auton.cfg":
#             ontologies.append({'ontology': root})#os.path.join(root, name)})
#         else:
#             print 'name: '+name
#  
#  
# for o in ontologies:
#     confs =get_auton_configuration(f=None, abs_folder=o['ontology'])
#     for c in confs:
#         tool = c.replace('_enable','')
#         o[tool] = confs[c]
# 
# 
# 
# for o in ontologies:
#     for d in o:
#         print d+': '+str(o[d])





