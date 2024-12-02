from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Contentor
from ..serializers import ContentorSerializer
from django.utils.timezone import now, make_aware, get_default_timezone
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
        

class VolumeByDayViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Filtrar volumes de registros por data no formato YYYY-MM-DD. Se não fornecido, será usado o dia atual.",
                type=openapi.TYPE_STRING,
                format='date',
                required=False,
            ),
        ],
        responses={
            200: "Lista de volumes para a data escolhida.",
            404: "Nenhum dado encontrado para a data escolhida.",
        },
    )
    def list(self, request):
        try:
            # Obtém o parâmetro de data da query string (formato: YYYY-MM-DD)
            date_str = request.query_params.get('date', None)

            if date_str:
                # Converte o parâmetro de data para objeto datetime
                try:
                    naive_date = datetime.strptime(date_str, '%Y-%m-%d')  # Converte string para naive datetime
                    chosen_date = make_aware(naive_date, timezone=get_default_timezone())  # Torna timezone-aware
                except ValueError:
                    return Response({"detail": "Formato de data inválido. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Se nenhuma data for fornecida, usa o dia atual
                chosen_date = now()

            # Define o início e o fim do dia escolhido
            start_of_day = chosen_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            # Filtra os registros de volume pela data escolhida
            contentores = Contentor.objects.filter(timestamp__gte=start_of_day, timestamp__lt=end_of_day)

            if not contentores.exists():
                return Response({"detail": "Nenhum dado encontrado para a data escolhida."}, status=status.HTTP_404_NOT_FOUND)

            # Serializa os dados necessários (id, volume, timestamp)
            serialized_data = [
                {
                    "id": contentor.id,
                    "volume": contentor.volume,
                    "timestamp": contentor.timestamp,
                }
                for contentor in contentores
            ]

            return Response(serialized_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)