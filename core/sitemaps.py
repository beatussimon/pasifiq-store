from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:contact', 'products:list']

    def location(self, item):
        return reverse(item)
