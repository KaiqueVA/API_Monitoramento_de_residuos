from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Contentor
from ..serializers import ContentorSerializer

class VolumeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContentorSerializer
    
    def get_queryset(self):
        
        if getattr(self, 'swagger_fake_view', False):
            return Contentor.objects.none()  

        return Contentor.objects.all()
    
    def list(self, request):
        volume_data = Contentor.objects.values('id', 'volume', 'timestamp')
        return Response(volume_data)

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


