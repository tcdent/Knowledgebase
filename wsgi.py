import os
import sys
import site

site.addsitedir('/home/knowledgebase/environment/lib/python2.6/site-packages')
sys.path.append('/home/knowledgebase/')
sys.path.append('/home/knowledgebase/app/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
