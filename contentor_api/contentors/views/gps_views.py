from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Contentor
from ..serializers import ContentorSerializer
from django.utils.timezone import make_aware, get_default_timezone, now
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..views.base_views import BaseDateRangeViewSet

class ContentorGPSPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ContentorGPSViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContentorSerializer
    def get_queryset(self):
        
        if getattr(self, 'swagger_fake_view', False):
            return Contentor.objects.none() 

        
        return Contentor.objects.all()
    pagination_class = ContentorGPSPagination
    
    def list(self, request):
        gps_data = Contentor.objects.values('id', 'latitude', 'longitude', 'timestamp')
        paginator = self.pagination_class() 
        paginated_data = paginator.paginate_queryset(gps_data, request)
        return paginator.get_paginated_response(paginated_data)
    
class LastContentorGPSViewSet(viewsets.ViewSet):
    

    def list(self, request):
        """
        """
        try:
            contentor = Contentor.objects.order_by('-timestamp').first()

            if contentor is None:
                return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ContentorSerializer(contentor)
            data = serializer.data

            filtered_data = {
                "id": data["id"],
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "timestamp": data["timestamp"]
            }

            return Response(filtered_data, status=status.HTTP_200_OK)

        except Contentor.DoesNotExist:
            return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
class ContentorGoogleMapsViewSet(viewsets.ViewSet):
    
    def list(self, request):
        try:
            
            contentor = Contentor.objects.order_by('-timestamp').first()

            if contentor is None:
                return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)

            idContentor = contentor.id
            google_maps_link = f"https://www.google.com/maps?q={contentor.latitude},{contentor.longitude}"
            

            return Response({"id": idContentor, "google_maps_link": google_maps_link}, status=status.HTTP_200_OK)

        except Contentor.DoesNotExist:
            return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        
class GPSByDateRangeViewSet(BaseDateRangeViewSet):
    @swagger_auto_schema(
        manual_parameters=BaseDateRangeViewSet.get_swagger_parameters(),  # Chama a função de parâmetros da classe base
        responses=BaseDateRangeViewSet.get_swagger_responses(),  # Chama a função de respostas da classe base
    )
    def list(self, request):
        self.data_fields = ['id', 'latitude', 'longitude', 'timestamp']
        return super().list(request)