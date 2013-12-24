from haystack import indexes, site
from .models import Page


class PageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

site.register(Page, PageIndex)


