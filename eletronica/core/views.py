# coding: utf-8
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy as r

class HomePageRedirectView(RedirectView):
    url = r('admin:index')