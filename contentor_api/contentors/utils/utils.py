import math

def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  # Raio da Terra em quilômetros
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
# Função para encontrar a posição mais distante com mais detalhes
def encontrar_posicao_mais_longe(com_detalhes):
    max_distancia = 0
    posicao_mais_longe = None

    for i, (lat1, lon1, id1, timestamp1) in enumerate(com_detalhes):
        for j, (lat2, lon2, id2, timestamp2) in enumerate(com_detalhes):
            if i != j:
                distancia = haversine(lat1, lon1, lat2, lon2)
                if distancia > max_distancia:
                    max_distancia = distancia
                    posicao_mais_longe = {
                        "id": id2,
                        "latitude": lat2,
                        "longitude": lon2,
                        "google_maps_link": f"https://www.google.com/maps?q={lat2},{lon2}"
                    }

    return posicao_mais_longe