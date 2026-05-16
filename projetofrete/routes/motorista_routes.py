from flask import request, jsonify, render_template, Blueprint, redirect, url_for
from db import get_db_connection
import psycopg2

motorista_bp = Blueprint("motorista", __name__)

def buscar_motoristas():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id_motorista, nome, telefone, cnh ,validade_cnh
            FROM motoristas
            WHERE ativo = TRUE
            ORDER BY nome ASC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id_motorista": r[0], "nome": r[1], "telefone": r[2], "cnh": r[3], "validade_cnh": r[4]} for r in rows]
    except:
        render_template("cadastro_veiculos.html", alert="Preencha todos os campos!", veiculos=[])


@motorista_bp.route('/motoristas', methods=['GET'])
def tela_motoristas():
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_motorista, nome, telefone, cnh ,validade_cnh
            FROM motoristas
            WHERE ativo = TRUE
            ORDER BY nome ASC
        """)

        rows = cur.fetchall()

        motoristas = []
        for row in rows:
            motoristas.append({
                "id_motorista": row[0],
                "nome": row[1],
                "telefone": row[2],
                "cnh": row[3],
                "validade": row[4]
            })

        return render_template(
            "cadastro_motoristas.html",
            motoristas=motoristas,
            alert=None
        )

    except Exception as e:
        return render_template("cadastro_motoristas.html", motoristas=[],
            alert=f"Erro ao carregar motoristas: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@motorista_bp.route('/add_motorista', methods=['POST'])
def add_motorista():
    data = request.form

    nome = data.get('nome', '').strip()
    telefone = data.get('telefone', '').strip()
    cnh = data.get('cnh', '').strip()
    validade= data.get('validade', '').strip()

    if not nome or not telefone or not cnh or not validade:
        return render_template("cadastro_motoristas.html", motoristas=buscar_motoristas(),
        alert=f"Erro ao cadastrar motorista: {str(e)}",
        alert_tipo="erro")

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO motoristas (nome, telefone, cnh , validade_cnh)
            VALUES (%s, %s, %s, %s)
        """, (nome, telefone, cnh, validade))

        conn.commit()

        #return redirect(url_for('motorista.tela_motoristas'))
        return render_template(
            "cadastro_motoristas.html",
            alert="Motorista cadastrado com sucesso",
            alert_tipo="sucesso",
            motoristas = buscar_motoristas()
        )
    
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return render_template("cadastro_motoristas.html",
            alert="Erro ao cadastrar. Registro duplicado",
            alert_tipo="erro",
            veiculos=buscar_motoristas()  # busca os dados
        )
    
    except Exception as e:
        if conn:
            conn.rollback()

        return render_template(
            "cadastro_motoristas.html",
            alert=f"Erro ao cadastrar motorista: {str(e)}",
            alert_tipo="erro",
            motoristas=buscar_motoristas()
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@motorista_bp.route("/dlt_motorista", methods=['POST'])
def dlt_motorista():
    conn = None 
    cur = None 

    data = request.form
    codigo = data.get('codigo','').strip()

    try:
        conn = get_db_connection()
        cur = conn.cursor() 

        cur.execute("""
            UPDATE motoristas SET ativo = FALSE WHERE id_motorista = %s
        """, (codigo,))
        conn.commit()
        return render_template(
            "cadastro_motoristas.html",
            alert="Motorista cadastrado com sucesso",
            alert_tipo="sucesso",
            motoristas=buscar_motoristas()
        )
    

    except Exception as e:
        if conn:
            conn.rollback()

        return render_template(
            "cadastro_motoristas.html",
            alert=f"Erro ao cadastrar motorista {str(e)}",
            alert_tipo = "erro",
            motoristas=buscar_motoristas()
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()