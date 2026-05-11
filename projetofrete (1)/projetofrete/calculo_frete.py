import os
# Importa o módulo os, usado aqui para acessar variáveis de ambiente do sistema

import googlemaps
# Importa a biblioteca googlemaps, que permite usar a API do Google Maps no Python

from datetime import datetime
# Importa a classe datetime, usada para pegar a data e hora atual


gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))
# Cria um cliente de conexão com o Google Maps
# os.getenv("GOOGLE_API_KEY") pega a chave da API que foi salva no sistema
# Essa chave é usada para autorizar as requisições ao Google


def calcular_distancia(origem, destino):
    # Define uma função chamada calcular_distancia
    # Ela recebe dois valores: origem e destino

    try:
        # Tenta executar o bloco abaixo
        # Se der erro, o código vai para o except

        now = datetime.now()
        # Pega a data e hora atual do sistema

        directions_result = gmaps.directions(
            origem,
            destino,
            mode="driving",
            departure_time=now
        )
        # Faz uma consulta ao Google Maps pedindo a rota entre origem e destino
        # origem = local de saída
        # destino = local de chegada
        # mode="driving" = rota de carro
        # departure_time=now = considera o horário atual como saída

        if not directions_result:
            # Verifica se a API retornou vazio, ou seja, nenhuma rota encontrada
            return 0.0
            # Se não encontrou rota, retorna 0.0

        route = directions_result[0]
        # Pega a primeira rota retornada pela API

        distance_meters = route["legs"][0]["distance"]["value"]
        # Acessa a estrutura da resposta e pega a distância em metros
        # route["legs"][0] = primeiro trecho da rota
        # ["distance"] = parte da distância
        # ["value"] = valor numérico em metros

        return round(distance_meters / 1000, 2)
        # Converte metros para quilômetros dividindo por 1000
        # round(..., 2) arredonda para 2 casas decimais
        # Exemplo: 72543 metros -> 72.54 km

    except Exception as e:
        # Se qualquer erro acontecer dentro do try, cai aqui

        print(f"Erro ao calcular distância: {e}")
        # Mostra a mensagem do erro no terminal

        return 0.0
        # Em caso de erro, retorna 0.0


def calcular_custo_combustivel(distancia_km, consumo_km_l, preco_combustivel):
    # Define uma função para calcular o custo do combustível
    # distancia_km = distância da viagem em km
    # consumo_km_l = quantos km o veículo faz por litro
    # preco_combustivel = preço do litro do combustível

    if consumo_km_l <= 0 or distancia_km <= 0:
        # Verifica se o consumo ou a distância são inválidos
        # Se for zero ou negativo, não dá para calcular
        return 0.0
        # Retorna 0.0

    return round((distancia_km / consumo_km_l) * preco_combustivel, 2)
    # Faz o cálculo do combustível:
    # distancia_km / consumo_km_l = litros gastos
    # litros gastos * preco_combustivel = custo total
    # round(..., 2) arredonda para 2 casas decimais


def calcular_custo_total(origem, destino, consumo_km_l, preco_combustivel):
    # Define uma função principal que junta tudo
    # Ela recebe origem, destino, consumo do veículo e preço do combustível

    distancia_km = calcular_distancia(origem, destino)
    # Chama a função calcular_distancia para descobrir os km da rota

    combustivel = calcular_custo_combustivel(
        distancia_km,
        consumo_km_l,
        preco_combustivel
    )
    # Chama a função calcular_custo_combustivel usando a distância calculada

    return {
        "distancia_km": distancia_km,
        # Guarda a distância calculada

        "custo_combustivel": combustivel,
        # Guarda o valor gasto com combustível

        "pedagio": 0.0,
        # Por enquanto o pedágio está fixo como zero

        "total": round(combustivel, 2)
        # O total por enquanto é só o combustível
        # round é usado para garantir 2 casas decimais
    }