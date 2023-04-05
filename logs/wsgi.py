
#PATH TO ENV PACKAGES
activate_this = 'C:/xampp/htdocs/logs/env/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with

#PATH TO ENV PACKAGES
site.addsitedir('C:/xampp/htdocs/logs/env/Lib/site-packages')


#PATH TO ENV PACKAGES

# Add the app's directory to the PYTHONPATH
sys.path.append('C:/xampp/htdocs/logs')
sys.path.append('C:/xampp/htdocs/logs/logs')

os.environ['DJANGO_SETTINGS_MODULE'] = 'logs.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logs.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()