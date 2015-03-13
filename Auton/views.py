from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from mongoengine.django.auth import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.urlresolvers import reverse

from datetime import datetime
from autoncore import get_updated_files,git_magic
from models import *



@login_required
def home(request):
    if request.method=='GET':
        return render_to_response('home.html',{'today': datetime.today(), 'repos': request.user.repos},context_instance=RequestContext(request))
    else:
        print request.POST
        target_repo = request.POST['target_repo']
        u = AutonUser.objects.get(id=request.user.id)
        r = None
        for i in u.repos:
            if i.repo_url == target_repo:
                r=i
        target_datetime = r.last_update        
        result = get_updated_files(target_repo, target_datetime)
        return render_to_response('home.html',{'today': target_datetime,'repos': request.user.repos, 'result': result, 'viewproceed':True},context_instance=RequestContext(request))



@login_required
def grant_update(request):
    print request.POST
    target_repo = request.POST['target_repo']
    l = request.POST['files_list'].strip()
    try:
        fil = l.split('&')[:-1]
    except:
        fil = []
    u = AutonUser.objects.get(id=request.user.id)
    r = None
    for i in u.repos:
        if i.repo_url == target_repo:
            r=i
    r.last_update = datetime.today()
    result = git_magic(target_repo,request.user.username,'git@github.com:'+target_repo+'.git',fil)
    r.save()
    return render_to_response('msg.html',{'msg': 'Magic is done'},context_instance=RequestContext(request))



@login_required
def delete_repo(request):
    repo = request.POST['target_repo']
    r = Repof.objects.get(repo_url=repo)
    r.delete()
    return render_to_response('msg.html',{'msg': 'repo deleted'},context_instance=RequestContext(request))
    #return redirect('repos')




@login_required
def repos(request):
    user = request.user
    user = AutonUser.objects.get(id=user.id)
    print str(user.id)+", "+user.email
    if request.method=='POST':
        repo = Repof()
        repo.repo_url=request.POST['newrepo']
        repo.save()
        user.repos.append(repo)
        user.save()
    return render_to_response('repos.html',{'repos': user.repos},context_instance=RequestContext(request))
    
    
    

def signup(request):
    if request.method=='GET':
        return render_to_response('signinup.html',context_instance=RequestContext(request))
    else:
        if 'next' in request.GET:
            next_url = request.GET['next']
        else:
            next_url = "/"
        print request.GET
        print request.POST
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        if password != confirm_password:
            return render_to_response('signinup',{'error_signup': 'password does not match'},context_instance=RequestContext(request))
        u = AutonUser.create_user(username=username,email=username,password=password)
        u = authenticate(username=username,password=password)
        login(request,u)
        return redirect('home')

    
    
def signin(request):
    if request.method=='GET':
        return render_to_response('signinup.html',context_instance=RequestContext(request))
    else:
        username = request.POST['username']
        password = request.POST['password'] 
        next_url = '/'
        u = authenticate(username=username, password=password)
        if u == None:
            return render_to_response('signinup.html', {'error_signin': 'wrong username/password combination'}, context_instance=RequestContext(request))
        else:
            login(request, u)    
            return HttpResponseRedirect(next_url)

    
    
def signout(request):
    logout(request)
    return redirect('home')

    
