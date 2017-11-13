#!/usr/bin/env python

import os
import sys

from os.path import dirname, join, abspath, pardir

APP_ROOT = abspath(join(dirname(abspath(__file__)), pardir))
sys.path.append(APP_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'portal.settings'

import django

django.setup()
from django.contrib.auth.models import User

user = User.objects.create_superuser('admin', '', 'password')
user.is_superuser = True
user.is_staff = True
user.save()
