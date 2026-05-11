from flask import request, render_template, Blueprint, redirect, url_for
from db import get_db_connection

cadastro_servico_bp = Blueprint('servico', __name__)


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


@cadastro_servico_bp.route('/cadastro_servicos', methods=['GET'])
def tela_servicos():
    
    try:
        clientes = carregar_clientes()
        print(clientes)
        return render_template(
            "cadastro_servicos.html",
            clientes=clientes,
            alert=None
        )
    except Exception as e:
        return render_template(
            "cadastro_servicos.html",
            clientes=[],
            alert=f"Erro ao carregar clientes: {str(e)}"
        )


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
    distancia_km = data.get('distancia', '').strip()
    consumo_km_l = data.get('consumo', '').strip()
    valor_combustivel = data.get('combustivel', '').strip()
    outras_despesas = data.get('despesas', '').strip()
    observacao = 'obs'

    if not id_cliente or not id_motorista or not id_veiculo or not origem or not destino or not distancia_km or not consumo_km_l or not valor_combustivel:
        return render_template(
            "cadastro_servicos.html",
            clientes=carregar_clientes(),
            alert="Dados incompletos"
        )

    try:
        id_cliente = int(id_cliente)
        id_motorista = int(id_motorista)
        id_veiculo = int(id_veiculo)
        distancia_km = float(distancia_km)
        consumo_km_l = float(consumo_km_l)
        valor_combustivel = float(valor_combustivel)
        outras_despesas = float(outras_despesas) if outras_despesas else 0.0

        if consumo_km_l <= 0:
            return render_template(
                "cadastro_servicos.html",
                clientes=carregar_clientes(),
                alert="O consumo deve ser maior que zero"
            )

        custo_combustivel = (distancia_km / consumo_km_l) * valor_combustivel
        custo_total = custo_combustivel + outras_despesas

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
            outras_despesas,
            custo_combustivel,
            custo_total,
            observacao
        ))

        conn.commit()
        return redirect(url_for('servico.tela_servicos'))

    except ValueError:
        return render_template(
            "cadastro_servicos.html",
            clientes=carregar_clientes(),
            alert="Verifique os valores numéricos informados"
        )

    except Exception as e:
        if conn:
            conn.rollback()
        return render_template(
            "cadastro_servicos.html",
            clientes=carregar_clientes(),
            alert=f"Erro ao cadastrar: {str(e)}"
        )

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()