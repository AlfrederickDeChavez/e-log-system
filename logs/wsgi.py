"""
WSGI config for logs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application


# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logs.settings')
# # os.environ["DJANGO_SETTINGS_MODULE"] = "logs.settings"

# os.environ["DJANGO_SETTINGS_MODULE"] = "logs.settings"

# application = get_wsgi_application()


activate_this = 'C:/xampp/htdocs/logs/env/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/xampp/htdocs/logs/env/Lib/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append('C:/xampp/htdocs/logs')
sys.path.append('C:/xampp/htdocs/logs/logs')

os.environ['DJANGO_SETTINGS_MODULE'] = 'logs.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logs.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()