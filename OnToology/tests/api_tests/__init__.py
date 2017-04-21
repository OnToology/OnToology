import os
import string
import random
from OnToology.models import *

user_password = os.environ['test_user_token']


def create_user():
    sec = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(9)])
    user = OUser()
    user.email = os.environ['test_user_email']
    user.username = user.email
    user.password = os.environ['test_user_token']
    user.token = sec
    user.save()

