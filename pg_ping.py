# -*- coding: utf-8 -*-
import psycopg2
import os
import sys
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

url = urlparse(os.environ['DATABASE_URL'])
database = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

try:
    connection = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
except psycopg2.OperationalError as e:
    sys.exit("The database is not ready.")
