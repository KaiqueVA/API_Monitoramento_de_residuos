from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Contentor
from ..serializers import ContentorSerializer





class ContentorViewSet(viewsets.ModelViewSet):
    queryset = Contentor.objects.all()
    serializer_class = ContentorSerializer
    
    
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