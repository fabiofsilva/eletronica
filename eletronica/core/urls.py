# coding: utf-8
from django.conf.urls import patterns, url
from eletronica.core.views import HomePageRedirectView


urlpatterns = patterns('eletronica.core.views',
                       url(r'^$', HomePageRedirectView.as_view(), name='homepage'),
)