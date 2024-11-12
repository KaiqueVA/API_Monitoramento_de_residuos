from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Contentor
from ..serializers import ContentorSerializer


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