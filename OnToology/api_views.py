from django.shortcuts import render
from django.http import JsonResponse

import github

import models


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']  # or token
        g = Github(username, password)
        try:
            g.get_user().login
            try:
                user = OUser.objects.get(username=username)
            except Exception as e:
                return JsonResponse({'message': 'authentication error'}, status_code=401)
        except Exception as e:
            return JsonResponse({'message': 'authentication error'}, status_code=401)
    return JsonResponse({'message': 'invalid method'}, status_code=405)


def home(request):
    return JsonResponse({"a": "full of A's", "b": "Bull of bulls"})


def list_repos(request):
    user_id = 0
    if request.method == 'GET':
        user = models.OUser.objects.filter(id=user_id)
        if len(user) == 1:
            user = user[0]
            repos = [r.json() for r in user.repos]
            return JsonResponse({'repos': repos})
        else:
            # user not found
            pass
    else:
        # POST
        pass


def add_repo(request):
    user_id = 0
    user = models.OUser.objects.filter(id=user_id)
    if len(user) == 1:
        user = user[0]
        repo = models.Repo()
        url = request.POST['url']
        owner = user.email
        repo.save()
        user.repos.append(repo)
        user.save()
        return JsonResponse({'status': True})
    # not valid user
    pass


def remove_repo(request):
    user_id = 0
    user = models.OUser.objects.filter(id=user_id)
    repo_id = 0
    if len(user) == 1:
        user = user[0]
        repo = repo.objects.filter(id=repo_id)
        if len(repo) == 1:
            # remove
            repo.delete()
            repo.save()
            user.save()





