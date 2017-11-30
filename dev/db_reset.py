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

from django.conf import settings
from django.core.management.base import CommandError
import logging
from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import execute_from_command_line

help = "Resets a database."

"""
Resets a database.

Note: Transaction wrappers are in reverse as a work around for
autocommit, anybody know how to do this the right way?
"""

engine = settings.DATABASES['default']['ENGINE'].split('.')[-1]

if engine == 'sqlite3':
    try:
        logging.info("Unlinking sqlite3 database")
        os.unlink(settings.DATABASES['default']['NAME'])
    except OSError:
        pass
elif engine == 'mysql':
    import MySQLdb as Database

    kwargs = {
        'user': settings.DATABASES['default']['USER'],
        'passwd': settings.DATABASES['default']['PASSWORD'],
    }
    if settings.DATABASES['default']['HOST'].startswith('/'):
        kwargs['unix_socket'] = settings.DATABASES['default']['HOST']
    else:
        kwargs['host'] = settings.DATABASES['default']['HOST']
    if settings.DATABASE_PORT:
        kwargs['port'] = int(settings.DATABASES['default']['PORT'])
    connection = Database.connect(**kwargs)
    drop_query = 'DROP DATABASE IF EXISTS %s' % settings.DATABASES['default']['NAME']
    create_query = 'CREATE DATABASE %s' % settings.DATABASES['default']['NAME']
    logging.info('Executing... "' + drop_query + '"')
    connection.query(drop_query)
    logging.info('Executing... "' + create_query + '"')
    connection.query(create_query)
elif engine == 'postgresql' or engine == 'postgresql_psycopg2':
    if engine == 'postgresql':
        import psycopg as Database
    elif engine == 'postgresql_psycopg2':
        import psycopg2 as Database

    if settings.DATABASE_NAME == '':
        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured("You need to specify DATABASE_NAME in your Django settings file.")
    if settings.DATABASES['default']['USER']:
        conn_string = "user=%s" % (settings.DATABASES['default']['USER'])
    if settings.DATABASES['default']['PASSWORD']:
        conn_string += " password='%s'" % settings.DATABASES['default']['PASSWORD']
    if settings.DATABASES['default']['HOST']:
        conn_string += " host=%s" % settings.DATABASES['default']['HOST']
    if settings.DATABASES['default']['PORT']:
        conn_string += " port=%s" % settings.DATABASES['default']['PORT']
    connection = Database.connect(conn_string)
    connection.set_isolation_level(0)  # autocommit false
    cursor = connection.cursor()
    drop_query = 'DROP DATABASE %s' % settings.DATABASES['default']['NAME']
    logging.info('Executing... "' + drop_query + '"')

    try:
        cursor.execute(drop_query)
    except Database.ProgrammingError as e:
        logging.info("Error: " + str(e))

    # Encoding should be SQL_ASCII (7-bit postgres default) or prefered UTF8 (8-bit)
    create_query = ("""
CREATE DATABASE %s
    WITH OWNER = %s
        ENCODING = 'UTF8'
        TABLESPACE = pg_default;
""" % (settings.DATABASES['default']['NAME'], settings.DATABASES['default']['USER']))
    logging.info('Executing... "' + create_query + '"')
    cursor.execute(create_query)

else:
    raise CommandError("Unknown database engine {}".format(engine))

logging.info("Reset success")  # makemigrations and migrate

execute_from_command_line(["manage.py", "makemigrations"])
execute_from_command_line(["manage.py", "migrate"])

# create a super user


print('creating admin user')
user = User.objects.create_superuser('admin', '', 'password')
user.is_superuser = True
user.is_staff = True
user.save()
