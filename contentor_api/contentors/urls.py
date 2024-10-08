# contentors/urls.py
from rest_framework.routers import DefaultRouter
from .views import ContentorViewSet

router = DefaultRouter()
router.register(r'contentors', ContentorViewSet)

urlpatterns = router.urls
