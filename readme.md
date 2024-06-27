# Connect on postgres on render
psql -h dpg-co5pdsu3e1ms73b9m8k0-a.singapore-postgres.render.com -U rupesh -d gokap_postgres -W
0GT4tckzjEYdWeMiOJvdBUzYk0qSYQlH

# Connect DBweaver or PgAdmin
<!-- Open DBeaver and create a new PostgreSQL connection.
Enter the following details: -->
Host: dpg-co5pdsu3e1ms73b9m8k0-a.singapore-postgres.render.com
Port: 5432
Database: gokap_postgres
Username: rupesh
Password: 0GT4tckzjEYdWeMiOJvdBUzYk0qSYQlH

# Debug Network Issue
ping dpg-co5pdsu3e1ms73b9m8k0-a.singapore-postgres.render.com 5432
telnet dpg-co5pdsu3e1ms73b9m8k0-a.singapore-postgres.render.com 5432
# If telnet is not available or you prefer other tools, you can use nc (netcat) or PowerShell to test connectivity:
nc -vz dpg-co5pdsu3e1ms73b9m8k0-a.singapore-postgres.render.com 5432
Test-NetConnection -ComputerName dpg-co5pdsu3e1ms73b9m8k0-a.singapore-postgres.render.com -Port 5432


# Connect phpmyadmin to database on render
1. install php-pgsql.
2. Open the config.inc.php file in the phpMyAdmin installation(xampp) directory.
'''
    <!-- add the following configuration to config.inc.php file (it only support MySQL and MariaDB -->
    $cfg['Servers'][$i]['verbose'] = 'Render PostgreSQL';
    $cfg['Servers'][$i]['host'] = 'dpg-co5pdsu3e1ms73b9m8k0-a.singapore-postgres.render.com';
    $cfg['Servers'][$i]['port'] = '5432';
    $cfg['Servers'][$i]['socket'] = '';
    $cfg['Servers'][$i]['connect_type'] = 'tcp';
    $cfg['Servers'][$i]['extension'] = 'pgsql';
    $cfg['Servers'][$i]['auth_type'] = 'config';
    $cfg['Servers'][$i]['user'] = 'rupesh';
    $cfg['Servers'][$i]['password'] = '0GT4tckzjEYdWeMiOJvdBUzYk0qSYQlH';
    $cfg['Servers'][$i]['AllowNoPassword'] = false;
'''


# Commands
1. connect to the database : \c database_name;
2. list all databse        : \l
3. list all schemas        : \dn
4. list all views          : \dv
5. list all tables         : \dt
6. more information        : \dt+ table_name
7. list all user           : \du


# Django Admin Page is not loading css after deployment in render
Step 1: Collect Static Files : python manage.py collectstatic
<!-- This command gathers all the static files from your apps and third-party packages into the directory specified by the STATIC_ROOT setting. -->
Step 2: Configure Static Files Settings
<!--
import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Ensure that the static files storage backend is configured
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
-->
Step 3: Use Whitenoise
Whitenoise helps serve static files in a production environment. Make sure you have it installed. Add Whitenoise to your MIDDLEWARE in settings.py:
<!-- pip install whitenoise
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
] -->
Step 4: Update Render Build Command
In your Render dashboard, ensure that the build command includes collectstatic. It should look something like this: 
<!-- python manage.py collectstatic --noinput -->

Step 5: Check Render Static File Settings
<!-- Ensure Render is configured to serve static files. In your Render service settings, you can specify the path to your static files. Typically, you might have a configuration similar to:

Environment: Python
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
Start Command: gunicorn your_project_name.wsgi -->


<!-- base urls of render -->
base url : https://gokap.onrender.com
base dir : /opt/render/project/src


# Fix Django Admin Page CSS not loading after Deployment, but works in localhost
1. Configure Static Files Settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

<!-- Ensure that the static files storage backend is configured -->
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

2. Install WhiteNoise and add WhiteNoise to the MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

3. Update Render Build Command
Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
Start Command: gunicorn your_project_name.wsgi


# PostgreSql Error
<!-- !postgres does not know where to find the server configuration file.
!You must specify the --config-file or -D invocation option or set the PGDATA environment variable. -->
-> The error message you're encountering indicates that PostgreSQL cannot locate its server configuration file (postgresql.conf). This file contains essential settings for running the database server. 
-> Setting the PGDATA Environment Variable : 
setx PGDATA "C:\Program Files\PostgreSQL\16\data"
<!-- !postgres does not know where to find the database system data. -->
-> The error message you're encountering indicates that PostgreSQL cannot find its database system data directory. This directory is crucial as it contains all the databases and transaction logs. You have three options to specify the location of the data directory:
-> 1. Using the -D Invocation Option
postgres -D "C:/Program Files/PostgreSQL/16/data"
-> 2. Setting the PGDATA Environment Variable
setx PGDATA "C:\Program Files\PostgreSQL\16\data"

//start postgres
pg_ctl -D "C:\Program Files\PostgreSQL\16\data" start

