from .contentor_views import ContentorViewSet
from .gps_views import ContentorGPSViewSet, LastContentorGPSViewSet, ContentorGoogleMapsViewSet
from .battery_views import BatteryViewSet, LastBatteryViewSet

__all__ = [
    "ContentorViewSet",
    "ContentorGPSViewSet",
    "LastContentorGPSViewSet",
    "ContentorGoogleMapsViewSet"
]