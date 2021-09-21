import unittest
import os
from django.test import TestCase

from OnToology import settings
from OnToology.models import *

def suite():
    return unittest.TestLoader().discover("OnToology.tests", pattern="test*.py")

# def suite():
#     return unittest.TestLoader().discover("OnToology.tests", pattern="test*publish.py")

