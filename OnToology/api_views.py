import random
import string
import os
from subprocess import call
import traceback

from github import Github

from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from OnToology.views import generateforall
from OnToology.djangoperpmod import *
from OnToology.autoncore import publish, previsual
from OnToology import autoncore
from OnToology.models import *
from OnToology.views import publish_dir
from django.utils import timezone


def token_required(func):
    def inner(request, *args, **kwargs):
        request.META.update(request.environ)
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header is not None:
            tokens = auth_header.split(' ')
            if len(tokens) == 2 and tokens[0] == 'Token':
                token = tokens[1]
                try:
                    request.user = OUser.objects.get(token=token)
                    if request.user.is_active:
                        return func(request, *args, **kwargs)
                    else:
                        return JsonResponse({'message': 'User account is inactive'}, status=403)
                except OUser.DoesNotExist:
                    return JsonResponse({'message': 'authentication error'}, status=401)
        return JsonResponse({'message': 'Invalid Header', 'status': False}, status=401)
    return inner


###################################################################
#                          Model Level                            #
###################################################################

@csrf_exempt
def login(request):
    if request.method == 'POST':
        if 'username' not in request.POST or 'password' not in request.POST:
            return JsonResponse({'message': 'username or password is missing'}, status=400)
        username = request.POST['username']
        token = request.POST['password']  # or token
        g = Github(username, token)
        try:
            g.get_user().login
            try:
                user = OUser.objects.get(username=username)
                if user.token_expiry <= timezone.now():
                    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
                    while len(OUser.objects.filter(token=sec)) > 0:  # to ensure a unique token
                        sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
                    user.token = sec
                    user.token_expiry = datetime.now() + timedelta(days=1)
                    user.save()
                return JsonResponse({'token': user.token})
            except Exception as e:
                return JsonResponse({'message': 'authentication error'}, status=401)
        except Exception as e:
            return JsonResponse({'message': 'authentication error'}, status=401)
    return JsonResponse({'message': 'Invalid method'}, status=405)


class ReposView(View):
    @method_decorator(token_required)
    def get(self, request):
        user = request.user
        repos = [r.json() for r in user.repos.all()]
        return JsonResponse({'repos': repos})

    @method_decorator(token_required)
    def post(self, request):
        try:
            if 'url' not in request.POST:
                return JsonResponse({'message': 'url is missing'}, status=400)
            user = request.user
            url = request.POST['url']
            owner = user.username
            repo = Repo()
            repo.url = url
            #repo.owner = owner
            repo.save()
            user.repos.add(repo)
            user.save()
            return JsonResponse({'message': 'Repo is added successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'exception: '+str(e)}, status=500)

    @method_decorator(token_required)
    def delete(self, request, repoid):
        try:
            # print("delete start")
            user = request.user
            r = Repo.objects.filter(id=repoid)
            if len(r) == 0 or r[0] not in user.repos.all():
                return JsonResponse({'message': 'Invalid repo'}, status=404)
            r = r[0]
            # user.repos.remove(r)
            # user.update(pull__repos=r)
            r.delete()
            #user.save()
            return JsonResponse({'message': 'The repo is deleted successfully'}, status=204)
        except Exception as e:
            # print("delete exception")
            traceback.print_exc(file=sys.stdout)
            return JsonResponse({'message': 'Internal error: '+str(e)}, status=500)


class PublishView(View):
    @method_decorator(token_required)
    def post(self, request):
        user = request.user
        if 'name' in request.POST and 'repo' in request.POST and 'ontology' in request.POST:
            name = request.POST['name']
            target_repo = request.POST['repo']
            ontology_rel_path = request.POST['ontology']
            print("going to previsual")
            error_msg = previsual(useremail=request.user.email, target_repo=target_repo)
            if error_msg != "":
                return JsonResponse({'message': error_msg}, status=400)
            print("going to publish")
            error_msg = publish(name=name, target_repo=target_repo, ontology_rel_path=ontology_rel_path, useremail=request.user.email)
            if error_msg != "":
                return JsonResponse({'message': error_msg}, status=400)
            return JsonResponse({'message': 'The ontology is published successfully'}, status=200)

    @method_decorator(token_required)
    def get(self, request):
        user = request.user
        pns = PublishName.objects.filter(user=user)
        pns_j = [p.json() for p in pns]
        return JsonResponse({'publishnames': pns_j}, status=200)

###################################################################
#                         Action Level                            #
###################################################################


@token_required
def generate_all(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid method'}, status=405)
    try:
        user = request.user
        if 'url' not in request.POST:
            return JsonResponse({'message': 'url is missing'}, status=400)
        if 'branch' not in request.POST:
            return JsonResponse({'message': 'branch is missing'}, status=400)
        branch = request.POST['branch'].strip()
        print("url: 1")
        url =request.POST['url'].strip()
        print("url: 2")
        if url[-1] == '/':
            url = url[:-1]
        found = False
        print("user.repos: ")
        print(user.repos.all())
        for r in user.repos.all():
            print("url for user")
            print(r.json())
            if r.url == url:
                print("url in")
                found = True
                break
            else:
                print("url not in")
        if found:
            print("generate for all url")
            res = generateforall(url, user.email, branch)
            print("res from renerate all")
            return JsonResponse({'message': 'generation is in process'}, status=202)
        else:
            print("generate for all url Not found")
            return JsonResponse({'message': 'Invalid repo'}, status=404)

    except Exception as e:
        return JsonResponse({'message': 'Internal Error: '+str(e)}, status=500)












