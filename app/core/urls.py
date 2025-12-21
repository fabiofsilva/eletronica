from django.urls import include, path

from . import views

app_name = 'core'

urlpatterns = [
    path('consertos/', views.search_repair, name='search_repair'),
    path('consertos/<slug:slug>/', views.conserto_detail, name='conserto_detail'),
    path('sugestao-de-solucao/', views.sugestao_solucao, name='sugestao_solucao'),
    path('api/', include('core.api.urls')),
    path('', views.HomePageView.as_view(), name='homepage'),
]
