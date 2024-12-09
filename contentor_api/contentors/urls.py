# contentors/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.contentor_views import ContentorViewSet, LastContentorViewSet, TodayContentorViewSet, ContentorByDateRangeViewSet
from .views.gps_views import ContentorGPSViewSet, LastContentorGPSViewSet, ContentorGoogleMapsViewSet, GPSByDateRangeViewSet, GPSLongerDistanceLocationViewSet
from .views.battery_views import BatteryViewSet, LastBatteryViewSet, BatteryByDateRangeViewSet
from .views.volume_views import VolumeViewSet, LastVolumeViewSet, VolumeByDateRangeViewSet
# from .views import ContentorViewSet, ContentorGPSViewSet, LastContentorGPSViewSet, LastContentorViewSet, ContentorGoogleMapsViewSet

router = DefaultRouter()
router.register(r'Contentors', ContentorViewSet, basename='Contentors')
router.register(r'last_contentor', LastContentorViewSet, basename='last-contentor')
router.register(r'today_contentor', TodayContentorViewSet, basename='today-contentor')
router.register(r'contentors_gps', ContentorGPSViewSet, basename='contentors-gps')
router.register(r'last_contentor_gps', LastContentorGPSViewSet, basename='last-contentor-gps')
router.register(r'google_maps', ContentorGoogleMapsViewSet, basename='contentor-google-maps')
router.register(r'contentors_batteries', BatteryViewSet, basename='contentor-batteries')
router.register(r'last_battery', LastBatteryViewSet, basename='last-battery')
router.register(r'contentors_volumes', VolumeViewSet, basename='contentor-volumes')
router.register(r'last_volume', LastVolumeViewSet, basename='last-volume')
router.register(r'Contentor-Date-Range', ContentorByDateRangeViewSet, basename='Contentor-Date-Range')
router.register(r'Volume-Date-Range', VolumeByDateRangeViewSet, basename='Volume-Date-Range')
router.register(r'GPS-Date-Range', GPSByDateRangeViewSet, basename='GPS-Date-Range')
router.register(r'Battery_Date_Range', BatteryByDateRangeViewSet, basename='Battery-Date-Range')
router.register(r'GPS-Longer-Distance-Location', GPSLongerDistanceLocationViewSet, basename='GPS-Longer-Distance-Location')




urlpatterns = [
    path('', include(router.urls)),
]
