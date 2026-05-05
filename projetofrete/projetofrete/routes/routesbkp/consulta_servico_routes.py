from flask import  request,  jsonify, render_template, Blueprint
from db import get_db_connection

servico_bp = Blueprint('servico',__name__)

def max_srv_cod():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT MAX(SRV_CODIGO) FROM SERVICO")
    last_srv_cod = cur.fetchall()[0][0]
    if not last_srv_cod:
        last_srv_cod = 0

    cur.close()
    conn.close()

    return last_srv_cod


@servico_bp.route('/dlt_servico', methods=['POST'])
def dlt_servico():
    codigo = request.form.get('codigo')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE SERVICO SET D_E_L_E_T_ = %s WHERE SRV_CODIGO = %s;", ('*', codigo))
        conn.commit()
        return render_template("consulta_servicos.html", alert = "Servico excluído com sucesso")

    except Exception as e:
        conn.rollback()
        return render_template("consulta_servicos.html",alert = f"Erro ao excluir produto: {e}")
    
    finally:
        cur.close()
        conn.close()

 
@servico_bp.route('/proc_srv', methods=["GET"])
def proc_service():

    data = request.args
    SRV_CODIGO   = data.get('srvID', '').strip()
    SRV_NOME     = data.get('serviceName', '').strip()
    SRV_OBSERVA      = data.get('serviceDesc', '').strip()
    
    # FORMATA PARA BUSCA PARCIAL
    src = "SELECT SRV_CODIGO, SRV_NOME, SRV_PRECO, SRV_OBSERVA FROM SERVICO WHERE D_E_L_E_T_ IS NULL"

    if SRV_CODIGO:
        src += f" AND SRV_CODIGO = {SRV_CODIGO}"

    if SRV_NOME:
        src += f" AND SRV_NOME ILIKE \'{SRV_NOME}\'"
    
    if SRV_OBSERVA:
        src += f" AND SRV_OBSERVA ILIKE \'{SRV_OBSERVA}\'"
    
    src += " ORDER BY SRV_NOME ASC"

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(src)
        rows = cur.fetchall()
        return render_template("cadastro_servicos.html", rows = rows)

    except Exception as e:
        conn.rollback()
        return render_template("cadastro_servicos.html", alert = f"Erro ao buscar serviço: {e}")
            
    finally:
        cur.close()
        conn.close()