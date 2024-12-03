from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.timezone import now, make_aware, get_default_timezone
from ..models import Contentor
from ..serializers import ContentorSerializer
from datetime import timedelta, datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..views.base_views import BaseDateRangeViewSet  # Adjust the import path as necessary


class ContentorPagination(PageNumberPagination):
    page_size = 10  # Número de itens por página
    page_size_query_param = 'page_size'  # Permite que o cliente defina o tamanho da página
    max_page_size = 100  # Tamanho máximo da página que o cliente pode pedir

class ContentorViewSet(viewsets.ModelViewSet):
    queryset = Contentor.objects.all()
    serializer_class = ContentorSerializer
    pagination_class = ContentorPagination
    
class LastContentorViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            contentor = Contentor.objects.order_by('-timestamp').first()

            if contentor is None:
                return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ContentorSerializer(contentor)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Contentor.DoesNotExist:
            return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
class TodayContentorViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            # Pega o início e fim do dia atual
            start_of_day = now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            # Filtra os contentores do dia atual
            contentores = Contentor.objects.filter(timestamp__gte=start_of_day, timestamp__lt=end_of_day)

            if not contentores.exists():
                return Response({"detail": "Nenhum dado encontrado para o dia atual."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ContentorSerializer(contentores, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContentorByDateRangeViewSet(BaseDateRangeViewSet):
    @swagger_auto_schema(
        manual_parameters=BaseDateRangeViewSet.get_swagger_parameters(),  # Chama a função de parâmetros da classe base
        responses=BaseDateRangeViewSet.get_swagger_responses(),  # Chama a função de respostas da classe base
    )
    def list(self, request):
        self.data_fields = ['id', 'device_addr', 'battery_level', 'volume', 'is_tipped_over', 'latitude', 'longitude', 'timestamp']
        return super().list(request) 

