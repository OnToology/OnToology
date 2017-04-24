import random
import string
import os
from subprocess import call

from github import Github

from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from OnToology.views import generateforall
from OnToology import autoncore
from models import *
from views import publish_dir


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
                if user.token_expiry <= datetime.now():
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
        repos = [r.json() for r in user.repos]
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
            repo.owner = owner
            repo.save()
            user.repos.append(repo)
            user.save()
            return JsonResponse({'message': 'Repo is added successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'exception: '+str(e)}, status=500)

    @method_decorator(token_required)
    def delete(self, request, repoid):
        try:
            user = request.user
            r = Repo.objects.filter(id=repoid)
            if len(r) == 0 or r[0] not in user.repos:
                return JsonResponse({'message': 'Invalid repo'}, status=404)

            r = r[0]
            user.update(pull__repos=r)
            r.delete()
            user.save()
            return JsonResponse({'message': 'The repo is deleted successfully'}, status=204)
        except Exception as e:
            return JsonResponse({'message': 'Internal error: '+str(e)}, status=500)


class PublishView(View):
    @method_decorator(token_required)
    def post(self, request):
        user = request.user
        if 'name' in request.POST and 'repo' in request.POST and 'ontology' in request.POST:
            name = request.POST['name']
            target_repo = request.POST['repo']
            ontology_rel_path = request.POST['ontology']
            found = False
            for r in user.repos:
                if target_repo == r.url:
                    found = True
                    repo = r
                    break
            error_msg = ''
            if found:
                if len(PublishName.objects.filter(name=name)) > 1:
                    return JsonResponse({'message': 'duplicate published names, please contact us ASAP to fix it'},
                                        status=500)

                # publishing a new name or updating a published name under the same user/repo/ontology
                elif len(PublishName.objects.filter(name=name)) == 0 or (
                                    PublishName.objects.get(name=name).user == user and
                                    PublishName.objects.get(name=name).repo == repo and
                                PublishName.objects.get(name=name).ontology == ontology_rel_path):

                    if (len(PublishName.objects.filter(name=name)) == 0 and
                                len(PublishName.objects.filter(user=user, ontology=ontology_rel_path, repo=repo)) > 0):
                        error_msg += 'can not reserve multiple names for the same ontology'
                    else:
                        autoncore.prepare_log(user.email)
                        # cloning_repo should look like 'git@github.com:user/reponame.git'
                        cloning_repo = 'git@github.com:%s.git' % target_repo
                        sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(4)])
                        folder_name = 'pub-' + sec
                        autoncore.clone_repo(cloning_repo, folder_name, dosleep=True)
                        repo_dir = os.path.join(autoncore.home, folder_name)
                        doc_dir = os.path.join(repo_dir, 'OnToology', ontology_rel_path[1:], 'documentation')
                        print 'repo_dir: %s' % repo_dir
                        print 'doc_dir: %s' % doc_dir
                        htaccess_f = os.path.join(doc_dir, '.htaccess')
                        if not os.path.exists(htaccess_f):
                            print 'htaccess is not found'
                            error_msg += 'We couldn\'t reserve your w3id. Please make sure that your ontology has' \
                                         ' documentation and htacess. For that, click on "Generate documentation, ' \
                                         'diagrams and evaluation" on the menu, and once the process is completed, ' \
                                         'accept the pull request on you GitHub repository'
                        else:
                            print 'found htaccesss'
                            f = open(htaccess_f, 'r')
                            file_content = f.read()
                            f.close()
                            f = open(htaccess_f, 'w')
                            for line in file_content.split('\n'):
                                if line[:11] == 'RewriteBase':
                                    f.write('RewriteBase /publish/%s \n' % name)
                                else:
                                    f.write(line + '\n')
                            f.close()
                            # comm = 'rm -Rf /home/ubuntu/publish/%s' % name
                            comm = 'rm -Rf ' + os.path.join(publish_dir, name)
                            print(comm)
                            call(comm, shell=True)
                            # comm = 'mv %s /home/ubuntu/publish/%s' % (doc_dir, name)
                            comm = 'mv %s %s' % (doc_dir, os.path.join(publish_dir, name))
                            print comm
                            call(comm, shell=True)
                            if len(PublishName.objects.filter(name=name)) == 0:
                                p = PublishName(name=name, user=user, repo=repo, ontology=ontology_rel_path)
                                p.save()
                            return JsonResponse({'message': 'Ontology is published'}, status=200)
            else:
                error_msg += 'This repo should belongs to the user first'
            return JsonResponse({'message': error_msg}, status=400)
        else:
            return JsonResponse({'message': 'missing parameter'}, status=400)

    @method_decorator(token_required)
    def get(self, request):
        user = request.user
        pns = PublishName.objects.filter(user=user)
        return JsonResponse({'publishnames': pns}, status=200)

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
        url =request.POST['url'].strip()
        if url[-1] == '/':
            url = url[:-1]
        found = False
        for r in user.repos:
            if r.url == url:
                found = True
                break
        if found:
            res = generateforall(url, user.email)
            return JsonResponse({'message': 'generation is in process'}, status=202)
        else:
            return JsonResponse({'message': 'Invalid repo'}, status=404)

    except Exception as e:
        return JsonResponse({'message': 'Internal Error: '+str(e)}, status=500)












