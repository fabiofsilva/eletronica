from rest_framework.routers import DefaultRouter

from core.api.views import ConsertoViewSet

router = DefaultRouter()
router.register('consertos', ConsertoViewSet, basename='consertos')

urlpatterns = router.urls
