from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Contentor
from ..serializers import ContentorSerializer


class ContentorGPSViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContentorSerializer
    
    def list(self, request):
        gps_data = Contentor.objects.values('id', 'latitude', 'longitude', 'timestamp')
        return Response(gps_data)
    
class LastContentorGPSViewSet(viewsets.ViewSet):
    

    def list(self, request):
        """
        """
        try:
            contentor = Contentor.objects.order_by('-timestamp').first()

            if contentor is None:
                return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ContentorSerializer(contentor)
            data = serializer.data

            filtered_data = {
                "id": data["id"],
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "timestamp": data["timestamp"]
            }

            return Response(filtered_data, status=status.HTTP_200_OK)

        except Contentor.DoesNotExist:
            return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
class ContentorGoogleMapsViewSet(viewsets.ViewSet):
    
    def list(self, request):
        try:
            
            contentor = Contentor.objects.order_by('-timestamp').first()

            if contentor is None:
                return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)

            idContentor = contentor.id
            google_maps_link = f"https://www.google.com/maps?q={contentor.latitude},{contentor.longitude}"
            

            return Response({"id": idContentor, "google_maps_link": google_maps_link}, status=status.HTTP_200_OK)

        except Contentor.DoesNotExist:
            return Response({"detail": "Nenhum dado encontrado."}, status=status.HTTP_404_NOT_FOUND)