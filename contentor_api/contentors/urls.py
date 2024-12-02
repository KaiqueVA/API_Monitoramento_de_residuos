# contentors/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.contentor_views import ContentorViewSet, LastContentorViewSet, TodayContentorViewSet, FilteredContentorViewSet
from .views.gps_views import ContentorGPSViewSet, LastContentorGPSViewSet, ContentorGoogleMapsViewSet, GPSByDayViewSet
from .views.battery_views import BatteryViewSet, LastBatteryViewSet, BatteryByDayViewSet
from .views.volume_views import VolumeViewSet, LastVolumeViewSet, VolumeByDayViewSet
# from .views import ContentorViewSet, ContentorGPSViewSet, LastContentorGPSViewSet, LastContentorViewSet, ContentorGoogleMapsViewSet

router = DefaultRouter()
router.register(r'contentors', ContentorViewSet)
router.register(r'last_contentor', LastContentorViewSet, basename='last-contentor')
router.register(r'today_contentor', TodayContentorViewSet, basename='today-contentor')
router.register(r'contentors_gps', ContentorGPSViewSet, basename='contentors-gps')
router.register(r'last_contentor_gps', LastContentorGPSViewSet, basename='last-contentor-gps')
router.register(r'google_maps', ContentorGoogleMapsViewSet, basename='contentor-google-maps')
router.register(r'contentors_batteries', BatteryViewSet, basename='contentor-batteries')
router.register(r'last_battery', LastBatteryViewSet, basename='last-battery')
router.register(r'contentors_volumes', VolumeViewSet, basename='contentor-volumes')
router.register(r'last_volume', LastVolumeViewSet, basename='last-volume')
router.register(r'filtered-contentores', FilteredContentorViewSet, basename='filtered-contentor')
router.register(r'volume_by_day', VolumeByDayViewSet, basename='volume-by-day')
router.register(r'gps_by_day', GPSByDayViewSet, basename='gps-by-day')
router.register(r'battery_by_day', BatteryByDayViewSet, basename='battery-by-day')




urlpatterns = [
    path('', include(router.urls)),
]
