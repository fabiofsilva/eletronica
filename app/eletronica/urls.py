from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView, TemplateView

admin.autodiscover()

admin.site.site_header = _('Eletrônica Administração')
admin.site.site_title = _('Site de administração Eletrônica')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico', permanent=True)),
    path('captcha/', include('captcha.urls')),
    path(
        'robots.txt',
        cache_page(60 * 60 * 24)(TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
        name='robots',
    ),
    path('', include('core.urls')),
]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
