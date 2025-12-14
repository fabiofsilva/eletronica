from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico', permanent=True)),
    path('captcha/', include('captcha.urls')),
    path('', include('core.urls')),
]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
