from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Contentor
from ..serializers import ContentorSerializer
from django.utils.timezone import now, make_aware, get_default_timezone
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..views.base_views import BaseDateRangeViewSet 

class ContentorVolumePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class VolumeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContentorSerializer
    pagination_class = ContentorVolumePagination
    
    def get_queryset(self):
        
        if getattr(self, 'swagger_fake_view', False):
            return Contentor.objects.none()  

        return Contentor.objects.all()
    
    def list(self, request):
        volume_data = Contentor.objects.values('id', 'volume', 'timestamp')
        paginator = self.pagination_class()
        paginate_data = paginator.paginate_queryset(volume_data, request)
        return paginator.get_paginated_response(paginate_data)

class LastVolumeViewSet(viewsets.ViewSet):
    
    def list(self, request):
        try:
            
            contentor = Contentor.objects.order_by('-timestamp').first()
            
            if contentor is None:
                return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ContentorSerializer(contentor)
            data = serializer.data
            
            filtered_data = {
                "id": data["id"],
                "volume": data["volume"],
                "timestamp": data["timestamp"]
            }
            return Response(filtered_data, status=status.HTTP_200_OK)
        
        except Contentor.DoesNotExist:
            return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)
        

class VolumeByDateRangeViewSet(BaseDateRangeViewSet):
    @swagger_auto_schema(
        manual_parameters=BaseDateRangeViewSet.get_swagger_parameters(),  # Chama a função de parâmetros da classe base
        responses=BaseDateRangeViewSet.get_swagger_responses(),  # Chama a função de respostas da classe base
    )
    def list(self, request):
        self.data_fields = ['id', 'volume', 'timestamp']
        return super().list(request)
    