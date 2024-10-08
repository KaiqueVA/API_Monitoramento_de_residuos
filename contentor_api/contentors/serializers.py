from rest_framework import serializers
from .models import Contentor

class ContentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contentor
        fields = ['id', 'device_addr', 'battery_level', 'volume', 'is_tipped_over', 'latitude', 'longitude', 'timestamp']
