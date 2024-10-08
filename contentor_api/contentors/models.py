# contentors/models.py
from django.db import models

class Contentor(models.Model):
    device_addr = models.CharField(max_length=255)
    battery_level = models.IntegerField()
    volume = models.FloatField()
    is_tipped_over = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.device_addr