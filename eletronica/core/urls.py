from django.conf.urls import url
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^consertos/$', views.search_repair, name='search_repair'),
    url(r'^lista-de-consertos/$', views.conserto_list, name='conserto_list'),
    url(r'^consertos/(?P<pk>\d+)/$', views.conserto_detail, name='conserto_detail'),
    url(r'^$', views.HomePageView.as_view(), name='homepage'),
]
