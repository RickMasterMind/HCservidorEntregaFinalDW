from rest_framework.routers import DefaultRouter

from .views import AgricultorViewSet, CultivoViewSet

router = DefaultRouter()
router.register("agricultores", AgricultorViewSet, basename="agricultor")
router.register("cultivos", CultivoViewSet, basename="cultivo")

urlpatterns = router.urls
