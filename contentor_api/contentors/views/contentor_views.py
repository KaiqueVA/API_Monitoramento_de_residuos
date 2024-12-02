from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils.timezone import now
from ..models import Contentor
from ..serializers import ContentorSerializer
from datetime import timedelta, datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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
        
class FilteredContentorViewSet(viewsets.ViewSet):
    # Define o parâmetro para o Swagger
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'date',  # Nome do parâmetro
                openapi.IN_QUERY,  # Tipo (query param)
                description="Filtrar registros por data no formato YYYY-MM-DD. Se não fornecido, será usado o dia atual.",
                type=openapi.TYPE_STRING,  # Tipo esperado
                format='date',  # Formato do parâmetro
                required=False,  # Opcional
            ),
        ],
        responses={200: ContentorSerializer(many=True), 404: "Nenhum dado encontrado para a data escolhida."},
    )
    def list(self, request):
        try:
            # Obtém o parâmetro de data da query string (formato: YYYY-MM-DD)
            date_str = request.query_params.get('date', None)
            
            if date_str:
                # Converte o parâmetro de data para objeto datetime
                try:
                    chosen_date = datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    return Response({"detail": "Formato de data inválido. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Se nenhuma data for fornecida, usa o dia atual
                chosen_date = now()

            # Define o início e o fim do dia escolhido
            start_of_day = chosen_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            # Filtra os contentores pela data escolhida
            contentores = Contentor.objects.filter(timestamp__gte=start_of_day, timestamp__lt=end_of_day)

            if not contentores.exists():
                return Response({"detail": "Nenhum dado encontrado para a data escolhida."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ContentorSerializer(contentores, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)