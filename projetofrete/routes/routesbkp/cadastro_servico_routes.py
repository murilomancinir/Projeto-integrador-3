from flask import  request,  jsonify, render_template, Blueprint
from db import get_db_connection

cadastro_servico_bp = Blueprint('servico',__name__)

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


@cadastro_servico_bp.route('/add_servico', methods=['POST'])
def add_servico():
    data = request.form
    ad_SRV_CODIGO  = max_srv_cod() + 1
    ad_SRV_ORIGEM    = data.get('origem', '').strip()
    ad_SRV_DESTINO = data.get('destino', '').strip()
    ad_SRV_DISTANCIA = data.get('distancia', '').strip()
    ad_SRV_CONSUMO = data.get('consumo', '').strip()
    ad_SRV_COMBUSTIVEL = data.get('combustivel', '').strip()
    ad_SRV_DESPESAS = data.get('despesas', '').strip()
  
    if not ad_SRV_ORIGEM or not ad_SRV_DESTINO or not ad_SRV_DISTANCIA or not ad_SRV_CONSUMO or not ad_SRV_COMBUSTIVEL or not ad_SRV_DESPESAS:
        return render_template("cadastro_servicos.html", alert="Dados incompletos", rows=[])
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Chamando a procedure de inclusão de dados na tabela de cadastro de produtos
        # cur.callproc( 'add_cliente', ( ad_CLI_CODIGO, ad_CLI_NOME, ad_CLI_ENDERECO, ad_CLI_TEL, ad_CLI_DOC, ad_CLI_OBSERVA ))
        
        # Utilizar o comando abaixo enquanto a procedure não é consertada
        cur.execute( "Insert Into SERVICO ( SRV_CODIGO,SRV_ORIGEM, SRV_DESTINO, SRV_CONSUMO,SRV_DESPESAS,SRV_DISTANCIA,SRV_COMBUSTIVEL) Values ( %s, %s, %s, %s, %s, %s, %s);", ( ad_SRV_CODIGO, ad_SRV_ORIGEM, ad_SRV_DESTINO, ad_SRV_CONSUMO,ad_SRV_DESPESAS,ad_SRV_DISTANCIA,ad_SRV_COMBUSTIVEL))
        conn.commit()
        rows = [(ad_SRV_CODIGO,ad_SRV_ORIGEM, ad_SRV_DESTINO, ad_SRV_CONSUMO,ad_SRV_DESPESAS,ad_SRV_DISTANCIA,ad_SRV_COMBUSTIVEL)]
        
        return render_template("cadastro_servicos.html", alert="Serviço adicionado com sucesso!", rows=rows)

    except Exception as e:
        conn.rollback()
        return render_template("cadastro_servicos.html", alert=f"Erro ao cadastrar: {str(e)}")
    
    finally:
        cur.close()
        conn.close()

