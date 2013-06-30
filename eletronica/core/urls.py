# coding: utf-8
from django.conf.urls import patterns, url
from eletronica.core.views import HomePageRedirectView


urlpatterns = patterns('eletronica.core.views',
                       url(r'^consertos/$', 'search_repair', name='search_repair'),
                       url(r'^lista-de-consertos/$', 'conserto_list', name='conserto_list'),
                       url(r'^consertos/(?P<pk>\d+)/$', 'conserto_detail', name='conserto_detail'),
                       url(r'^$', HomePageRedirectView.as_view(), name='homepage'),
)