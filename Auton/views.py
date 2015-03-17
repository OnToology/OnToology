from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from mongoengine.django.auth import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

import string
import random
from datetime import datetime
from autoncore import get_updated_files,git_magic, add_webhook, webhook_access, update_g, add_collaborator
from models import *
import requests
import json


host = 'http://54.172.63.231'
client_id = 'bbfc39dd5b6065bbe53b'
client_secret = '60014ba718601441f542213855607810573c391e'



def home(request):
    if 'target_repo' in request.GET:
        target_repo = request.GET['target_repo']
        webhook_access_url, state = webhook_access(client_id,host+'/get_access_token')
        request.session['target_repo'] = target_repo
        request.session['state'] = state
        return  HttpResponseRedirect(webhook_access_url)
    return render_to_response('home.html',context_instance=RequestContext(request))

        



def grant_update(request):
#     print request.POST
#     target_repo = request.POST['target_repo']
#     l = request.POST['files_list'].strip()
#     try:
#         fil = l.split('&')[:-1]
#     except:
#         fil = []
#     u = AutonUser.objects.get(id=request.user.id)
#     r = None
#     for i in u.repos:
#         if i.repo_url == target_repo:
#             r=i
#     r.last_update = datetime.today()
#     result = git_magic(target_repo,request.user.username,'git@github.com:'+target_repo+'.git',fil)
#     r.save()
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
    rpy_wh = add_webhook(request.session['target_repo'], host+"/add_hook")
    rpy_coll = add_collaborator(request.session['target_repo'], 'AutonUser')
    error_msg = ""
    if rpy_wh['status'] == False:
        error_msg+=str(rpy_wh['error'])
    if rpy_coll['status'] == False:
        error_msg+=str(rpy_coll['error'])
    if error_msg != "":
        return render_to_response('msg.html',{'msg':error_msg },context_instance=RequestContext(request))
    return render_to_response('msg.html',{'msg':'webhook attached and user added as collaborator' },context_instance=RequestContext(request))
    

      

@csrf_exempt
def add_hook(request):
    s = str(request.POST['payload'])
    j = json.loads(s)
    s = j['repository']['url']+'updated files: '+str(j['head_commit']['modified'])
    #request.session['updated_files'] = j['head_commit']['modified']
    return render_to_response('msg.html',{'msg': 'webhook created: '+s},context_instance=RequestContext(request))


