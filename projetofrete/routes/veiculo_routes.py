from flask import request, jsonify, render_template, Blueprint, redirect, url_for
from db import get_db_connection
import psycopg2

veiculo_bp = Blueprint("veiculo", __name__)

 # Busca veículos para ter disponível em qualquer situação de erro
def buscar_veiculos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_veiculo, placa, modelo, marca, consumo_medio FROM veiculos WHERE ativo = TRUE ORDER BY id_veiculo ASC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id_veiculo": r[0], "placa": r[1], "modelo": r[2], "marca": r[3], "consumo_medio": r[4]} for r in rows]
    except:
        render_template("cadastro_veiculos.html", alert="Veiculo não encontrado", veiculos=[])
        

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
    consumo = data.get('consumo', '').strip()

   
    #Se algum campo estiver vazio vai aparecer alerta antes de tentar inserir no banco
    if not placa or not modelo or not marca or not consumo:
       
        return render_template("cadastro_veiculos.html",
            veiculos=buscar_veiculos()
        )

    conn = None
    cur = None
    # Tenta inserir os dados no banco
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO veiculos (placa, modelo, marca, consumo_medio)
            VALUES (%s, %s, %s, %s)
        """, (placa, modelo, marca, consumo))
        conn.commit()
        return redirect(url_for('veiculo.tela_veiculos'))

    # Verifficação de placa 
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return render_template("cadastro_veiculos.html",
            
            alert="Veiculo já cadastrado, verifique!",veiculos=buscar_veiculos()  # busca os dados
        )

    except Exception as e:
        if conn:
            conn.rollback()
        return render_template("cadastro_veiculos.html", alert=f"Erro ao cadastrar veículo: {str(e)}",
            veiculos=buscar_veiculos()  #  agora busca os dados
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
            update veiculos set ATIVO = FALSE WHERE id_veiculo = %s
        """, (codigo,))
        conn.commit()
        return render_template(
            "cadastro_veiculos.html", alert="Veiculo excluido"
            ,alert_tipo="sucesso", veiculo=buscar_veiculos()
        )
    

    except Exception as e:
        if conn:
            conn.rollback()

        
        return render_template(
            "cadastro_veiculos.html",
            veiculos=buscar_veiculos()
            
        )
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()