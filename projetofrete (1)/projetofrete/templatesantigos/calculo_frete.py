# calculo_frete.py
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyD6E28qsnCIYEFTRP0JbtRwhM4gZlXs5Rk')

class Veiculo:
    def __init__(self, tipo, consumo_km_l, num_eixos=None):
        self.tipo = tipo
        self.consumo_km_l = consumo_km_l
        self.num_eixos = num_eixos if tipo == 'caminhao' else None

def calcular_distancia_e_pedagios(origem, destino):
    try:
        now = datetime.now()
        directions_result = gmaps.directions(origem, destino, mode="driving", departure_time=now)
        if not directions_result:
            return 0, 0
        route = directions_result[0]
        distance_meters = route['legs'][0]['distance']['value']
        distance_km = distance_meters / 1000.0
        return distance_km, 0  # pedágio não confiável
    except:
        return 0, 0

def calcular_custo_combustivel(distancia_km, veiculo, preco):
    if veiculo.consumo_km_l <= 0 or distancia_km <= 0:
        return 0.0
    return (distancia_km / veiculo.consumo_km_l) * preco

def calcular_custos_viagem(origem, destino, veiculo, preco):
    distancia, pedagio = calcular_distancia_e_pedagios(origem, destino)
    combustivel = calcular_custo_combustivel(distancia, veiculo, preco)
    total = pedagio + combustivel
    return total, pedagio, combustivel, distancia