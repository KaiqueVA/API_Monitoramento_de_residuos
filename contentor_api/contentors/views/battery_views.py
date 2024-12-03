from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Contentor
from ..views.base_views import BaseDateRangeViewSet
from ..serializers import ContentorSerializer
from django.utils.timezone import make_aware, get_default_timezone, now
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ContentorBatteryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BatteryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContentorSerializer
    def get_queryset(self):
        
        if getattr(self, 'swagger_fake_view', False):
            return Contentor.objects.none()  

        return Contentor.objects.all()
    
    pagination_class = ContentorBatteryPagination
    
    def list(self, request):
        battery_data = Contentor.objects.values('id', 'battery_level', 'timestamp')
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(battery_data, request)
        return paginator.get_paginated_response(paginated_data)
    
class LastBatteryViewSet(viewsets.ViewSet):
    
    def list(self, request):
        try:
            # Consulta o último registro com base no campo 'timestamp'
            contentor = Contentor.objects.order_by('-timestamp').first()
            
            if contentor is None:
                return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)
            
            # Serializa o objeto encontrado
            serializer = ContentorSerializer(contentor)
            data = serializer.data
            
            # Filtra os dados que deseja retornar
            filtered_data = {
                "id": data["id"],
                "battery_level": data["battery_level"],  # Verifique o nome correto do campo
                "timestamp": data["timestamp"]
            }
            
            return Response(filtered_data, status=status.HTTP_200_OK)
            
        except Contentor.DoesNotExist:
            return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
class BatteryByDateRangeViewSet(BaseDateRangeViewSet):
    @swagger_auto_schema(
        manual_parameters=BaseDateRangeViewSet.get_swagger_parameters(),  # Chama a função de parâmetros da classe base
        responses=BaseDateRangeViewSet.get_swagger_responses(),  # Chama a função de respostas da classe base
    )
    def list(self, request):
        self.data_fields = ['id', 'battery_level', 'timestamp']
        return super().list(request)
    