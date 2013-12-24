import os
import sys
import site

site.addsitedir('/var/www/knowledgebase/environment/lib/python2.6/site-packages')
sys.path.append('/var/www/knowledgebase/')
sys.path.append('/var/www/knowledgebase/app/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
