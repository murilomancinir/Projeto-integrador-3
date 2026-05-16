from flask import request, render_template, Blueprint, redirect, url_for
from db import get_db_connection

consulta_servico_bp = Blueprint('consulta_servico', __name__)


@consulta_servico_bp.route('/consulta_servicos', methods=['GET'])
def tela_servicos():
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                srv.id_servico,
                vc.modelo,
                cli.nome,
                mot.nome,
                srv.origem,
                srv.destino,
                srv.distancia_km,
                srv.consumo_km_l,
                srv.valor_combustivel,
                srv.outras_despesas,
                srv.custo_combustivel,
                srv.custo_total,
                srv.data_cadastro
            FROM servicos srv
            INNER JOIN clientes cli ON cli.id_cliente = srv.id_cliente
            INNER JOIN motoristas mot ON mot.id_motorista = srv.id_motorista
            INNER JOIN veiculos vc ON vc.id_veiculo = srv.id_veiculo
            WHERE srv.ativo = TRUE
            ORDER BY srv.id_servico ASC
        """)

        rows = cur.fetchall()

        servicos = []
        for row in rows:
            servicos.append({
                "id_servico": row[0],
                "modelo": row[1],
                "cliente": row[2],
                "motorista": row[3],
                "origem": row[4],
                "destino": row[5],
                "distancia_km": row[6],
                "consumo_km_l": row[7],
                "valor_combustivel": row[8],
                "outras_despesas": row[9],
                "custo_combustivel": row[10],
                "custo_total": row[11],
                "data_cadastro": row[12]
            })

        return render_template(
            "consulta_servicos.html",
            servicos=servicos,
            alert=None
        )

    except Exception as e:
        return render_template(
            "consulta_servicos.html",
            servicos=[],
            alert=f"Erro ao carregar serviços: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


@consulta_servico_bp.route('/dlt_servico', methods=['POST'])
def dlt_servico():
    conn = None
    cur = None

    data = request.form
    id_servico = data.get('id_servico', '').strip()

    try:
        if not id_servico:
            return redirect(url_for('consulta_servico.tela_servicos'))

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE servicos
            SET ativo = FALSE
            WHERE id_servico = %s
        """, (id_servico,))

        conn.commit()
        return redirect(url_for('consulta_servico.tela_servicos'))

    except Exception as e:
        if conn:
            conn.rollback()

        return render_template(
            "consulta_servicos.html",
            servicos=[],
            alert=f"Erro ao excluir serviço: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()