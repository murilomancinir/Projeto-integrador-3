# from flask import jsonify


# @cadastro_servico_bp.route('/buscar_distancia', methods=['POST'])
# def buscar_distancia():
#     data = request.get_json()

#     origem = data.get('origem', '').strip()
#     destino = data.get('destino', '').strip()

#     if not origem or not destino:
#         return jsonify({"erro": "Origem e destino são obrigatórios"}), 400

#     try:
#         distancia_km = calcular_distancia(origem, destino)

#         if distancia_km <= 0:
#             return jsonify({"erro": "Não foi possível calcular a distância"}), 400

#         return jsonify({"distancia_km": distancia_km})

#     except Exception as e:
#         return jsonify({"erro": str(e)}), 500