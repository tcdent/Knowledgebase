import os
import sys
import site

site.addsitedir('/mnt/Tripe/Personal/Knowledgebase/Build/environment/lib/python2.6/site-packages')
sys.path.append('/mnt/Tripe/Personal/Knowledgebase/Build/')
sys.path.append('/mnt/Tripe/Personal/Knowledgebase/Build/app/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
