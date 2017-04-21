import random
import string

from github import Github

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from models import *


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        token = request.POST['password']  # or token
        g = Github(username, token)
        try:
            g.get_user().login
            try:
                user = OUser.objects.get(username=username)
                if user.token_expiry <= datetime.now():
                    user.token = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
                    user.token_expiry = datetime.now() + timedelta(days=1)
                    user.save()
                return JsonResponse({'token': user.token})
            except Exception as e:
                return JsonResponse({'message': 'authentication error 1'}, status=401)
        except Exception as e:
            return JsonResponse({'message': 'authentication error 2'}, status=401)
    return JsonResponse({'message': 'invalid method'}, status=405)

#
# def home(request):
#     return JsonResponse({"a": "full of A's", "b": "Bull of bulls"})
#
#
# def list_repos(request):
#     user_id = 0
#     if request.method == 'GET':
#         user = OUser.objects.filter(id=user_id)
#         if len(user) == 1:
#             user = user[0]
#             repos = [r.json() for r in user.repos]
#             return JsonResponse({'repos': repos})
#         else:
#             # user not found
#             pass
#     else:
#         # POST
#         pass
#
#
# def add_repo(request):
#     user_id = 0
#     user = OUser.objects.filter(id=user_id)
#     if len(user) == 1:
#         user = user[0]
#         repo = Repo()
#         url = request.POST['url']
#         owner = user.email
#         repo.save()
#         user.repos.append(repo)
#         user.save()
#         return JsonResponse({'status': True})
#     # not valid user
#     pass
#
#
# def remove_repo(request):
#     user_id = 0
#     user = OUser.objects.filter(id=user_id)
#     repo_id = 0
#     if len(user) == 1:
#         user = user[0]
#         repo = Repo.objects.filter(id=repo_id)
#         if len(repo) == 1:
#             # remove
#             repo.delete()
#             repo.save()
#             user.save()





