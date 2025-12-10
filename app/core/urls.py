from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'core'

urlpatterns = [
    path('consertos/', views.search_repair, name='search_repair'),
    path('lista-de-consertos/', views.conserto_list, name='conserto_list'),
    path('consertos/<int:pk>/', views.conserto_detail, name='conserto_detail'),
    path('contato/', TemplateView.as_view(template_name='core/contato.html'), name='contato'),
    path('', views.HomePageView.as_view(), name='homepage'),
]
