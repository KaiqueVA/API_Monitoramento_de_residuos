from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Contentor
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
        
class BatteryByDayViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Filtrar registros de bateria por data no formato YYYY-MM-DD. Se não fornecido, será usado o dia atual.",
                type=openapi.TYPE_STRING,
                format='date',
                required=False,
            ),
        ],
        responses={
            200: "Lista de níveis de bateria para a data escolhida.",
            404: "Nenhum dado encontrado para a data escolhida.",
        },
    )
    def list(self, request):
        try:
            date_str = request.query_params.get('date', None)

            if date_str:
                try:
                    naive_date = datetime.strptime(date_str, '%Y-%m-%d')
                    chosen_date = make_aware(naive_date, timezone=get_default_timezone())
                except ValueError:
                    return Response({"detail": "Formato de data inválido. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                chosen_date = now()

            start_of_day = chosen_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            battery_data = Contentor.objects.filter(timestamp__gte=start_of_day, timestamp__lt=end_of_day)

            if not battery_data.exists():
                return Response({"detail": "Nenhum dado encontrado para a data escolhida."}, status=status.HTTP_404_NOT_FOUND)

            serialized_data = [
                {
                    "id": contentor.id,
                    "battery_level": contentor.battery_level,
                    "timestamp": contentor.timestamp,
                }
                for contentor in battery_data
            ]

            # Remove a paginação
            return Response(serialized_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)