# contentors/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.contentor_views import ContentorViewSet, LastContentorViewSet
from .views.gps_views import ContentorGPSViewSet, LastContentorGPSViewSet, ContentorGoogleMapsViewSet
from .views.battery_views import BatteryViewSet, LastBatteryViewSet
from .views.volume_views import VolumeViewSet, LastVolumeViewSet
# from .views import ContentorViewSet, ContentorGPSViewSet, LastContentorGPSViewSet, LastContentorViewSet, ContentorGoogleMapsViewSet

router = DefaultRouter()
router.register(r'contentors', ContentorViewSet)
router.register(r'last_contentor', LastContentorViewSet, basename='last-contentor')
router.register(r'contentors_gps', ContentorGPSViewSet, basename='contentors-gps')
router.register(r'last_contentor_gps', LastContentorGPSViewSet, basename='last-contentor-gps')
router.register(r'google_maps', ContentorGoogleMapsViewSet, basename='contentor-google-maps')
router.register(r'contentors_batteries', BatteryViewSet, basename='contentor-batteries')
router.register(r'last_battery', LastBatteryViewSet, basename='last-battery')
router.register(r'contentors_volumes', VolumeViewSet, basename='contentor-volumes')
router.register(r'last_volume', LastVolumeViewSet, basename='last-volume')


urlpatterns = [
    path('', include(router.urls)),
]
