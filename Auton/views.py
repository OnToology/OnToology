

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from mongoengine.django.auth import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from datetime import datetime
from autoncore import get_updated_files

def home(request):
    if request.method=='GET':
        return render_to_response('home.html',{'today': datetime.today()},context_instance=RequestContext(request))
    else:
        year = int(request.POST['year'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        hour = int(request.POST['hour'])
        minute = int(request.POST['minute'])
        target_repo = request.POST['target_repo']
        target_datetime = datetime(year=year,month=month,day=day,hour=hour,minute=minute)
        result = get_updated_files(target_repo, target_datetime)
        print len(result)
        return render_to_response('home.html',{'today': target_datetime, 'result': result},context_instance=RequestContext(request))



