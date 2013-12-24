import reversion
from django.contrib import admin
from .models import Page

class PageAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Page, PageAdmin)


