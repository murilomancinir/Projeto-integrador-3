from flask import request, jsonify, render_template, Blueprint, redirect, url_for
from db import get_db_connection

cliente_bp = Blueprint('cliente', __name__)


@cliente_bp.route('/clientes', methods=['GET'])
def tela_clientes():
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_cliente, nome, telefone, email, cidade
            FROM clientes
            WHERE ativo = TRUE
            ORDER BY nome ASC
        """)

        rows = cur.fetchall()

        clientes = []
        for row in rows:
            clientes.append({
                "id_cliente": row[0],
                "nome": row[1],
                "telefone": row[2],
                "email": row[3],
                "cidade": row[4]
            })

        return render_template(
            "cadastro_clientes.html",
            clientes=clientes,
            alert=None
        )

    except Exception as e:
        return render_template(
            "cadastro_clientes.html",
            clientes=[],
            alert=f"Erro ao carregar clientes: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@cliente_bp.route('/add_cliente', methods=['POST'])
def add_cliente():
    data = request.form

    nome = data.get('nome', '').strip()
    telefone = data.get('telefone', '').strip()
    email = data.get('email', '').strip()
    cidade = data.get('cidade', '').strip()

    if not nome or not telefone or not email or not cidade:
        return render_template(
            "cadastro_clientes.html",
            alert="Dados incompletos",
            clientes=[]
        )

    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO clientes (nome, telefone, email, cidade)
            VALUES (%s, %s, %s, %s)
        """, (nome, telefone, email, cidade))

        conn.commit()

        return redirect(url_for('cliente.tela_clientes'))

    except Exception as e:
        if conn:
            conn.rollback()

        return render_template(
            "cadastro_clientes.html",
            alert=f"Erro ao cadastrar: {str(e)}",
            clientes=[]
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@cliente_bp.route("/dlt_cliente", methods=['POST'])
def dlt_cliente():
    conn = None 
    cur = None 

    data = request.form
    codigo = data.get('codigo').strip()

    try:
        conn = get_db_connection()
        cur = conn.cursor() 

        cur.execute("""
            UPDATE clientes SET ativo = FALSE WHERE id_cliente = %s
        """, (codigo))
        conn.commit()
        return redirect(url_for('cliente.tela_clientes'))
    

    except Exception as e:
        if conn:
            conn.rollback()

        return render_template(
            "cadastro_clientes.html",
            alert=f"Erro ao excluir cliente: {str(e)}",
            clientes=[]
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()