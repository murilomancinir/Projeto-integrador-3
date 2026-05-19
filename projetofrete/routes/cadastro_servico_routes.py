from flask import request, render_template, Blueprint, redirect, url_for, jsonify
from db import get_db_connection

import os
import requests

cadastro_servico_bp = Blueprint('servico', __name__)

GOOGLE_API_KEY = "AIzaSyDG8oIrpPO45gkrikn4p2hHoGZct2KmaXs"

if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não foi configurada.")

def calcular_distancia(origem, destino):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "routes.distanceMeters"
    }

    body = {
        "origin": {
            "address": origem
        },
        "destination": {
            "address": destino
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_UNAWARE",
        "languageCode": "pt-BR",
        "units": "METRIC"
    }

    try:
        response = requests.post(url, json=body, headers=headers, timeout=20)
        response.raise_for_status()

        data = response.json()

        if "routes" not in data or not data["routes"]:
            return 0.0

        distancia_metros = data["routes"][0]["distanceMeters"]
        return round(distancia_metros / 1000, 2)

    except Exception as e:
        print(f"Erro ao calcular distância: {e}")
        return 0.0
    
def carregar_clientes():
    conn = None
    cur = None
    clientes = []

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_cliente, nome
            FROM clientes
            WHERE ativo = TRUE
            ORDER BY nome ASC
        """)

        rows = cur.fetchall()

        for row in rows:
            clientes.append({
                "id_cliente": row[0],
                "nome": row[1]
            })

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return clientes

def carregar_veiculos():
    conn = None
    cur = None
    veiculos = []

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_veiculo, modelo
            FROM veiculos
            WHERE ativo = TRUE
            ORDER BY modelo ASC
        """)

        rows = cur.fetchall()

        for row in rows:
            veiculos.append({
                "id_veiculo": row[0],
                "modelo": row[1]
            })

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return veiculos

def carregar_motoristas():
    conn = None
    cur = None
    motoristas = []

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_motorista, nome
            FROM motoristas
            WHERE ativo = TRUE
            ORDER BY nome ASC
        """)

        rows = cur.fetchall()

        for row in rows:
            motoristas.append({
                "id_motorista": row[0],
                "nome": row[1]
            })

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return motoristas

@cadastro_servico_bp.route('/cadastro_servicos', methods=['GET'])
def tela_servicos():
    
    try:
        clientes = carregar_clientes()
        veiculos = carregar_veiculos()
        motoristas = carregar_motoristas()

        return render_template(
            "cadastro_servicos.html",
            clientes=clientes,
            veiculos=veiculos,
            motoristas=motoristas,

        )
    except Exception as e:
        return render_template(
            "cadastro_servicos.html",
            clientes=[],
            veiculos=[],
            motoristas=[],
            alert=f"Erro ao cadastrar viagem: {str(e)}",
            alert_tipo="erro"
        )

@cadastro_servico_bp.route('/buscar_distancia', methods=['POST'])
def buscar_distancia():
    data = request.get_json()

    origem = data.get('origem', '').strip()
    destino = data.get('destino', '').strip()

    if not origem or not destino:
        return jsonify({"erro": "Origem e destino são obrigatórios"}), 400

    try:
        distancia_km = calcular_distancia(origem, destino)

        if distancia_km <= 0:
            return jsonify({"erro": "Não foi possível calcular a distância"}), 400

        return jsonify({"distancia_km": distancia_km})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@cadastro_servico_bp.route('/add_servico', methods=['POST'])
def add_servico():
    conn = None
    cur = None

    data = request.form

    id_cliente = data.get('id_cliente', '').strip()
    id_motorista = data.get('id_motorista', '').strip()
    id_veiculo = data.get('id_veiculo', '').strip()
    origem = data.get('origem', '').strip()
    destino = data.get('destino', '').strip()
    distancia_km_informada = data.get('distancia', '').strip()
    distancia_manual = data.get('distancia_manual', '0').strip()
    consumo_km_l = data.get('consumo', '').strip()
    valor_combustivel = data.get('combustivel', '').strip()
    
    valor = data.get('valor','').strip()
    observacao = 'obs'

    if not id_cliente or not id_motorista or not id_veiculo or not origem or not destino or not consumo_km_l or not valor_combustivel:
        return render_template(
            "cadastro_servicos.html",
            clientes=carregar_clientes(),
            veiculos=carregar_veiculos(),
            motoristas=carregar_motoristas(),
            alert="Dados incompletos"
        )

    try:
        id_cliente = int(id_cliente)
        id_motorista = int(id_motorista)
        id_veiculo = int(id_veiculo)
        consumo_km_l = float(consumo_km_l)
        valor_combustivel = float(valor_combustivel)
        valor = float(valor) if valor else 0.0

        if consumo_km_l <= 0:
            return render_template(
                "cadastro_servicos.html",
                clientes=carregar_clientes(),
                veiculos=carregar_veiculos(),
                motoristas=carregar_motoristas(),
                alert="O consumo deve ser maior que zero"
            )

        if distancia_manual == '1':
            if not distancia_km_informada:
                return render_template(
                    "cadastro_servicos.html",
                    clientes=carregar_clientes(),
                    veiculos=carregar_veiculos(),
                    motoristas=carregar_motoristas(),
                    alert="Informe a distância manualmente ou desligue o modo manual"
                )
            
            distancia_km = float(distancia_km_informada)

            if distancia_km <= 0:
                return render_template(
                    "cadastro_servicos.html",
                    clientes=carregar_clientes(),
                    veiculos=carregar_veiculos(),
                    motoristas=carregar_motoristas(),
                    alert="A distância deve ser maior que zero"
                )
        else:
            
            distancia_km = calcular_distancia(origem, destino)

            if distancia_km <= 0:
                return render_template(
                    "cadastro_servicos.html",
                    clientes=carregar_clientes(),
                    veiculos=carregar_veiculos(),
                    motoristas=carregar_motoristas(),
                    alert="Não foi possível calcular a distância com a origem e destino informados"
                )

        custo_combustivel = (distancia_km / consumo_km_l) * valor_combustivel
        custo_total = custo_combustivel + valor

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO servicos (
                id_cliente,
                id_motorista,
                id_veiculo,
                origem,
                destino,
                distancia_km,
                consumo_km_l,
                valor_combustivel,
                outras_despesas,
                custo_combustivel,
                custo_total,
                observacao
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            id_cliente,
            id_motorista,
            id_veiculo,
            origem,
            destino,
            distancia_km,
            consumo_km_l,
            valor_combustivel,
            valor,
            custo_combustivel,
            custo_total,
            observacao
        ))

        conn.commit()
        return render_template(
            "cadastro_servicos.html",
            alert="Serviço incluido com sucesso",
            alert_tipo="sucesso",
            servicos = tela_servicos()
        )

    except ValueError:
        return render_template(
            "cadastro_servicos.html",
            clientes=carregar_clientes(),
            veiculos=carregar_veiculos(),
            motoristas=carregar_motoristas(),
            alert="Verifique os valores numéricos informados"
        )

    except Exception as e:
        if conn:
            conn.rollback()
        return render_template(
            "cadastro_servicos.html",
            clientes=carregar_clientes(),
            veiculos=carregar_veiculos(),
            motoristas=carregar_motoristas(),
            alert=f"Erro ao cadastrar: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



