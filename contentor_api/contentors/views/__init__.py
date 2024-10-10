from .contentor_views import ContentorViewSet
from .gps_views import ContentorGPSViewSet, LastContentorGPSViewSet, ContentorGoogleMapsViewSet
from .battery_views import BatteryViewSet, LastBatteryViewSet
from .volume_views import VolumeViewSet, LastVolumeViewSet

__all__ = [
    "ContentorViewSet",
    "ContentorGPSViewSet",
    "LastContentorGPSViewSet",
    "ContentorGoogleMapsViewSet",
    "BatteryViewSet",
    "LastBatteryViewSet",
    "VolumeViewSet",
    "LastVolumeViewSet",
    
]