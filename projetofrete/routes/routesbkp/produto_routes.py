
from flask import  request,  jsonify, render_template, Blueprint
from db import get_db_connection

produto_bp = Blueprint ('produto', __name__)

def max_prd_cod():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(PRD_CODIGO) FROM PRODUTO;")
    last_prd_cod = cur.fetchone()[0]

    if not last_prd_cod:
        last_prd_cod = 0

    cur.close()
    conn.close()
    return last_prd_cod

@produto_bp.route('/add_produto', methods=['POST'])
def add_produto():
    data = request.form
    ad_PRD_CODIGO  = max_prd_cod() + 1
    ad_PRD_NOME    = data.get('productName', '').strip()
    ad_PRD_PRECO   = data.get('productPrice', '').strip()
    ad_PRD_OBSERVA = data.get('productDesc', '').strip()

    if not ad_PRD_NOME or not ad_PRD_PRECO or not ad_PRD_CODIGO or not ad_PRD_OBSERVA:
        return render_template("cadastro_produtos.html", alert="Dados incompletos", rows=[])
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Chamando a procedure de inclusão de dados na tabela de cadastro de produtos
        # cur.callproc( 'add_cliente', ( ad_CLI_CODIGO, ad_CLI_NOME, ad_CLI_ENDERECO, ad_CLI_TEL, ad_CLI_DOC, ad_CLI_OBSERVA ))
        
        # Utilizar o comando abaixo enquanto a procedure não é consertada
        cur.execute( "Insert Into PRODUTO ( PRD_CODIGO, PRD_NOME, PRD_PRECO, PRD_OBSERVA, D_E_L_E_T_, R_E_C_N_O_, R_E_C_D_E_L_) Values ( %s, %s, %s, %s, NULL, 1, NULL);", ( ad_PRD_CODIGO, ad_PRD_NOME, ad_PRD_PRECO, ad_PRD_OBSERVA))
        conn.commit()
        rows = [(ad_PRD_CODIGO, ad_PRD_NOME, ad_PRD_PRECO, ad_PRD_OBSERVA)]

    except Exception as e:
        conn.rollback()
        render_template("cadastro_produtos.html", alert=f"Erro ao cadastrar: {str(e)}")
    
    finally:
        cur.close()
        conn.close()
    
    return render_template("cadastro_produtos.html", alert="Produto adicionado com sucesso!", rows=rows)

# Rota para deletar um cadastro de um produto
@produto_bp.route('/dlt_produto', methods=['POST'])
def dlt_produto():
    codigo = request.form.get('codigo')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE PRODUTO SET D_E_L_E_T_ = %s WHERE PRD_CODIGO = %s;", ('*', codigo))
        conn.commit()
        return render_template("cadastro_produtos.html", alert = "Produto excluído com sucesso")

    except Exception as e:
        conn.rollback()
        return render_template("cadastro_produtos.html",alert = f"Erro ao excluir produto: {e}")
    
    finally:
        cur.close()
        conn.close()

@produto_bp.route('/proc_prd', methods=["GET"])
def proc_produto():
    data = request.args
    CODIGO   = data.get('productID', '').strip()
    NOME     = data.get('productName', '').strip()
    OBSERVA  = data.get('productDesc', '').strip()
    src = 'SELECT PRD_CODIGO AS Código, PRD_NOME AS Nome, PRD_PRECO AS Preço, PRD_OBSERVA AS DESCRIÇÃO FROM PRODUTO WHERE D_E_L_E_T_ IS NULL'

    # FORMATA PARA BUSCA PARCIAL
    if CODIGO:
        src += f" AND PRD_CODIGO = {CODIGO}"
    
    if NOME:
        src += f" AND PRD_NOME ILIKE \'%{NOME}%\'"
    
    if OBSERVA:
        src += f" AND PRD_OBSERVA ILIKE \'%{OBSERVA}%\'"

    src += ' ORDER BY PRD_NOME ASC;'


    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(src)
        rows = cur.fetchall()

    except:
        mensagem = 'Produto não encontrado!'
        return redirect(url_for(dir_cadastro_produtos))

    cur.close()
    conn.close()

    return render_template("cadastro_produtos.html", rows=rows)

