from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Contentor
from ..serializers import ContentorSerializer

class ContentorBatteryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BatteryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContentorSerializer
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