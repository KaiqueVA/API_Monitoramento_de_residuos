# contentors/views.py
from rest_framework import viewsets
from .models import Contentor
from .serializers import ContentorSerializer

class ContentorViewSet(viewsets.ModelViewSet):
    queryset = Contentor.objects.all()
    serializer_class = ContentorSerializer
