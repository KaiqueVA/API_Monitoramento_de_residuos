from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils.timezone import make_aware, get_default_timezone
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Contentor
from ..serializers import ContentorSerializer

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 10  
    max_page_size = 100  

class BaseDateRangeViewSet(viewsets.ViewSet):
    serializer_class = ContentorSerializer
    pagination_class = CustomPageNumberPagination  # Use a paginação customizada

    def __init__(self, data_fields=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_fields = data_fields

    def get_filtered_data(self, queryset):
        
        return queryset.values(*self.data_fields)
    
    def get_paginated_response(self, data, request):
        
        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(data, request)
        return paginator.get_paginated_response(paginated_data)

    def get_swagger_parameters():
        return [
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Data inicial no formato YYYY-MM-DD.",
                type=openapi.TYPE_STRING,
                format='date',
                required=True,
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Data final no formato YYYY-MM-DD.",
                type=openapi.TYPE_STRING,
                format='date',
                required=True,
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Número da página de resultados. Padrão é 1.",
                type=openapi.TYPE_INTEGER,
                default=1,
                required=False,
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Número de itens por página. Padrão é 100.",
                type=openapi.TYPE_INTEGER,
                default=100,
                required=False,
            ),
        ]
    
    def get_swagger_responses():
        return {
            200: "Lista de dados no intervalo de datas escolhido.",
            400: "Parâmetros de data inválidos.",
            404: "Nenhum dado encontrado no intervalo especificado.",
        }

    def list(self, request):
        try:
            # Obtém os parâmetros de data da requisição
            start_date_str = request.query_params.get('start_date', None)
            end_date_str = request.query_params.get('end_date', None)

            if not start_date_str or not end_date_str:
                return Response({"detail": "Os parâmetros 'start_date' e 'end_date' são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                naive_start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                naive_end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

                start_date = make_aware(naive_start_date, timezone=get_default_timezone())
                end_date = make_aware(naive_end_date, timezone=get_default_timezone())
            except ValueError:
                return Response({"detail": "Formato de data inválido. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                return Response({"detail": "A 'start_date' não pode ser posterior à 'end_date'."}, status=status.HTTP_400_BAD_REQUEST)

            # Filtra os dados de acordo com o intervalo de datas
            battery_data = Contentor.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date)

            if not battery_data.exists():
                return Response({"detail": "Nenhum dado encontrado no intervalo especificado."}, status=status.HTTP_404_NOT_FOUND)

            # Obtém os dados filtrados
            serialized_data = self.get_filtered_data(battery_data)

            # Aplica a paginação e retorna a resposta paginada
            return self.get_paginated_response(serialized_data, request)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
