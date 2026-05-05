from flask import request, jsonify, render_template, Blueprint, redirect, url_for
from db import get_db_connection

veiculo_bp = Blueprint("veiculo", __name__)


@veiculo_bp.route('/veiculos', methods=['GET'])
def tela_veiculos():
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_veiculo, placa, modelo, marca,consumo_medio
            FROM veiculos
            WHERE ativo = TRUE
            ORDER BY modelo ASC
        """)

        rows = cur.fetchall()

        veiculos = []
        for row in rows:
            veiculos.append({
                "id_veiculo": row[0],
                "placa": row[1],
                "modelo": row[2],
                "marca": row[3],
                "consumo": row[4]
            })

        return render_template(
            "cadastro_veiculos.html",
            veiculos=veiculos,
            alert=None
        )

    except Exception as e:
        return render_template("cadastro_veiculos.html", veiculos=[],
            alert=f"Erro ao carregar veiculos: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@veiculo_bp.route('/add_veiculo', methods=['POST'])
def add_veiculo():
    data = request.form

    placa = data.get('placa', '').strip()
    modelo = data.get('modelo', '').strip()
    marca = data.get('marca', '').strip()
    consumo= data.get('consumo', '').strip()

    if not placa or not modelo or not marca or not consumo:
        return render_template(
            "cadastro_veiculos.html",
            alert="Dados incompletos",
            veiculos=[]
        )

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO veiculos (placa, modelo, marca, consumo_medio)
            VALUES (%s, %s, %s, %s)
        """, (placa, modelo, marca, consumo))

        conn.commit()

        return redirect(url_for('veiculo.tela_veiculos'))

    except Exception as e:
        if conn:
            conn.rollback()

        return render_template(
            "cadastro_veiculos.html",
            alert=f"Erro ao cadastrar: {str(e)}",
            veiculos=[]
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@veiculo_bp.route("/dlt_veiculo", methods=['POST'])
def dlt_veiculo():
    conn = None 
    cur = None 

    data = request.form
    codigo = data.get('codigo','').strip()

    try:
        conn = get_db_connection()
        cur = conn.cursor() 

        cur.execute("""
            UPDATE veiculos SET ativo = FALSE WHERE id_veiculo = %s
        """, (codigo))
        conn.commit()
        return redirect(url_for('veiculo.tela_veiculos'))
    

    except Exception as e:
        if conn:
            conn.rollback()

        return render_template(
            "cadastro_veiculos.html",
            alert=f"Erro ao excluir veiculo: {str(e)}",
            veiculos=[]
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()