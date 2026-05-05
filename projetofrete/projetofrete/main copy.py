from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
from flask_cors import CORS
import psycopg2
import googlemaps
from datetime import datetime
from calculo_frete import Veiculo, calcular_custos_viagem

app = Flask(__name__)
app.secret_key = 'logistica2025_frete_seguro'  # PODE SER QUALQUER STRING
CORS(app)  # permite que o frontend chame o backend, especialmente útil localmente
# teste commit
# Rotas das páginas

carrinho = []
cliente = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro_clientes')
def dir_cadastro_clientes():
    return render_template('cadastro_clientes.html')

@app.route('/cadastro_produtos')
def dir_cadastro_produtos():
    return render_template('cadastro_produtos.html')

@app.route('/cadastro_servicos')
def dir_cadastro_servicos():
    return render_template('cadastro_servicos.html')

@app.route('/frete')
def dir_pagina_frete():
    return render_template('frete.html')

@app.route('/vendas')
def dir_vendas():
    cliente = ()
    return render_template('vendas.html')


##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
# Configurações do banco de dados

DB_HOST = "localhost"
DB_NAME = "estetsys"
DB_USER = "estetsys"
DB_PASS = "estetsys"

# Função para conectar ao banco de dados do Estetsys como 
def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

# Função para determinar o CLI_CODIGO MÁXIMO

def max_cli_cod():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(CLI_CODIGO) FROM CLIENTE;")
    last_cli_cod = cur.fetchall()[0][0]

    if not last_cli_cod:
        last_cli_cod = 0

    cur.close()
    conn.close()
    return last_cli_cod

########################   Seção de Cliente   ########################

# Rota para adicionar um produto ao cadastro de produtos
@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    data = request.form
    ad_CLI_CODIGO     = max_cli_cod() + 1
    ad_CLI_NOME       = data.get('clientName', '').strip()
    ad_CLI_ENDERECO	  = data.get('clientAddress', '').strip()
    ad_CLI_COMPLEMENT = data.get('clientComplement', '').strip()
    ad_CLI_CEP        = data.get('clientCEP', '').strip()
    ad_CLI_TEL        = data.get('clientPhone', '').strip()
    ad_CLI_DOC        = data.get('clientCPF', '').strip()
    ad_CLI_OBSERVA    = data.get('clientNote', '').strip()

    if not ad_CLI_NOME or not ad_CLI_ENDERECO or not ad_CLI_TEL or not ad_CLI_DOC:
        return render_template("cadastro_clientes.html", alert="Dados incompletos", rows=[])
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Chamando a procedure de inclusão de dados na tabela de cadastro de produtos
        # cur.callproc( 'add_cliente', ( ad_CLI_CODIGO, ad_CLI_NOME, ad_CLI_ENDERECO, ad_CLI_TEL, ad_CLI_DOC, ad_CLI_OBSERVA ))
        
        # Utilizar o comando abaixo enquanto a procedure não é consertada
        cur.execute( "Insert Into CLIENTE ( CLI_CODIGO, CLI_NOME, CLI_ENDERECO, CLI_COMPLEMENT, CLI_CEP, CLI_TEL, CLI_DOC, CLI_OBSERVA, D_E_L_E_T_, R_E_C_N_O_, R_E_C_D_E_L_) Values ( %s, %s, %s, %s, %s, %s, %s, %s, NULL, 1, NULL);", ( ad_CLI_CODIGO, ad_CLI_NOME, ad_CLI_ENDERECO, ad_CLI_COMPLEMENT, ad_CLI_CEP, ad_CLI_TEL, ad_CLI_DOC, ad_CLI_OBSERVA ))
        conn.commit()
        rows = [(ad_CLI_NOME, ad_CLI_DOC, ad_CLI_TEL, ad_CLI_OBSERVA)]
    except Exception as e:
        conn.rollback()
        render_template("cadastro_clientes.html", alert=f"Erro ao cadastrar: {str(e)}")
    finally:
        cur.close()
        conn.close()
    
    return render_template("cadastro_clientes.html", alert=f"Cliente adicionado com sucesso!",rows=rows)

# Rota para deletar um cadastro de um cliente
@app.route('/dlt_cliente', methods=['POST'])
def dlt_cliente():
    codigo = request.form.get('codigo')
    codigo = str(codigo)

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE CLIENTE SET D_E_L_E_T_ = %s WHERE CLI_DOC = %s;", ('*', codigo))
        conn.commit()
        return render_template("cadastro_clientes.html", alert = "Cliente excluído com sucesso")

    except Exception as e:
        conn.rollback()
        return render_template("cadastro_clientes.html",alert = f"Erro ao excluir cliente: {e}")
    finally:
        cur.close()
        conn.close()

########################    Seção de Produtos   ########################

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


# Rota para adicionar um produto ao cadastro de produtos
@app.route('/add_produto', methods=['POST'])
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
@app.route('/dlt_produto', methods=['POST'])
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

########################    Seção de Serviços   ########################

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

# Rota para adicionar um produto ao cadastro de produtos
@app.route('/add_servico', methods=['POST'])
def add_servico():
    data = request.form
    ad_SRV_CODIGO  = max_srv_cod() + 1
    ad_SRV_NOME    = data.get('serviceName', '').strip()
    ad_SRV_PRECO   = data.get('servicePrice', '').strip()
    ad_SRV_OBSERVA = data.get('serviceDesc', '').strip()

    if not ad_SRV_NOME or not ad_SRV_PRECO or not ad_SRV_OBSERVA:
        return render_template("cadastro_servicos.html", alert="Dados incompletos", rows=[])
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Chamando a procedure de inclusão de dados na tabela de cadastro de produtos
        # cur.callproc( 'add_cliente', ( ad_CLI_CODIGO, ad_CLI_NOME, ad_CLI_ENDERECO, ad_CLI_TEL, ad_CLI_DOC, ad_CLI_OBSERVA ))
        
        # Utilizar o comando abaixo enquanto a procedure não é consertada
        cur.execute( "Insert Into SERVICO ( SRV_CODIGO, SRV_NOME, SRV_PRECO, SRV_OBSERVA, D_E_L_E_T_, R_E_C_N_O_, R_E_C_D_E_L_) Values ( %s, %s, %s, %s, NULL, 1, NULL);", ( ad_SRV_CODIGO, ad_SRV_NOME, ad_SRV_PRECO, ad_SRV_OBSERVA))
        conn.commit()
        rows = [(ad_SRV_CODIGO, ad_SRV_NOME, ad_SRV_PRECO, ad_SRV_OBSERVA)]
        
        return render_template("cadastro_servicos.html", alert="Serviço adicionado com sucesso!", rows=rows)

    except Exception as e:
        conn.rollback()
        return render_template("cadastro_servicos.html", alert=f"Erro ao cadastrar: {str(e)}")
    
    finally:
        cur.close()
        conn.close()

@app.route('/dlt_servico', methods=['POST'])
def dlt_servico():
    codigo = request.form.get('codigo')

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE SERVICO SET D_E_L_E_T_ = %s WHERE SRV_CODIGO = %s;", ('*', codigo))
        conn.commit()
        return render_template("cadastro_servicos.html", alert = "Servico excluído com sucesso")

    except Exception as e:
        conn.rollback()
        return render_template("cadastro_servicos.html",alert = f"Erro ao excluir produto: {e}")
    
    finally:
        cur.close()
        conn.close()

########################    Seção de FRETE   ########################
##############################################
###########   CÁLCULO DE FRETE   #############
##############################################

# Configuração da API Google Maps
gmaps = googlemaps.Client(key='AIzaSyA1VH8getQ9WABo7xCwL-2PCOyKbivJxs8')

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

# --- ROTA FRETE: CÁLCULO + SALVAR NO BANCO ---
@app.route('/frete', methods=['GET', 'POST'])
def pagina_frete():
    if request.method == 'POST':
        # 1. Dados do formulário
        origem = request.form['origem'].strip()
        destino = request.form['destino'].strip()
        veiculo_tipo = request.form['veiculo']
        try:
            preco_combustivel = float(request.form['preco_combustivel'])
        except:
            flash("Preço do combustível inválido!")
            return redirect(url_for('pagina_frete'))

        if not all([origem, destino, veiculo_tipo]):
            flash("Preencha todos os campos!")
            return redirect(url_for('pagina_frete'))

        # 2. Criar veículo
        veiculos = {
            'carro': Veiculo("carro", 12.0),
            'moto': Veiculo("moto", 25.0),
            'caminhao': Veiculo("caminhao", 4.5, 3)
        }
        veiculo = veiculos.get(veiculo_tipo)
        if not veiculo:
            flash("Veículo inválido!")
            return redirect(url_for('pagina_frete'))

        # 3. Calcular com Google Maps
        try:
            total, pedagio, combustivel, distancia = calcular_custos_viagem(
                origem, destino, veiculo, preco_combustivel
            )
        except Exception as e:
            flash(f"Erro na rota: {str(e)}")
            return redirect(url_for('pagina_frete'))

        # 4. Gerar próximo FRE_CODIGO
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT COALESCE(MAX(FRE_CODIGO), 0) FROM FRETE")
            proximo_codigo = int(cur.fetchone()[0]) + 1
            cur.close()
            conn.close()
        except Exception as e:
            flash(f"Erro ao gerar código: {e}")
            return redirect(url_for('pagina_frete'))

         # --- SALVAR NO BANCO (INSERT DIRETO) ---
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Gerar próximo código
            cur.execute("SELECT COALESCE(MAX(fre_codigo), 0) + 1 FROM frete")
            proximo_codigo = cur.fetchone()[0]

            # INSERT DIRETO (SEM PROCEDURE, SEM $$)
            cur.execute(
                "INSERT INTO frete ("
                "fre_codigo, fre_origem, fre_destino, fre_veiculo, "
                "fre_distancia, fre_pedagio, fre_combustivel, fre_total, fre_observa"
                ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    proximo_codigo,
                    origem,
                    destino,
                    veiculo_tipo,
                    round(distancia, 2),
                    round(pedagio, 2),
                    round(combustivel, 2),
                    round(total, 2),
                    f"Calculado em {datetime.now():%d/%m/%Y %H:%M}"
                )
            )

            conn.commit()
            cur.close()
            conn.close()

            flash("Frete salvo com sucesso!")
        except Exception as e:
            flash(f"Erro ao salvar: {e}")
        # =========================================

        # 6. Mostrar resultado ()
        return render_template('frete_resultado.html',
                               origem=origem,
                               destino=destino,
                               veiculo=veiculo_tipo.capitalize(),
                               distancia=distancia,
                               pedagio=pedagio,
                               combustivel=combustivel,
                               total=total)

    # GET: mostrar formulário
    return render_template('frete.html')

# ==================== FRETE MANUAL ====================

@app.route('/frete_manual', methods=['GET', 'POST'])
def adicionar_frete_manual():
    if request.method == 'POST':
        try:
            origem = request.form['origem']
            destino = request.form['destino']
            veiculo = request.form['veiculo']
            distancia = float(request.form['distancia'])
            pedagio = float(request.form['pedagio'])
            combustivel = float(request.form['combustivel'])
            total = float(request.form['total'])

            conn = get_db_connection()
            cur = conn.cursor()

            # Gerar próximo código
            cur.execute("SELECT COALESCE(MAX(fre_codigo), 0) + 1 FROM frete")
            proximo_codigo = cur.fetchone()[0]

            # INSERT direto
            cur.execute(
                "INSERT INTO frete (fre_codigo, fre_origem, fre_destino, fre_veiculo, "
                "fre_distancia, fre_pedagio, fre_combustivel, fre_total, fre_observa) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    proximo_codigo, origem, destino, veiculo,
                    round(distancia, 2), round(pedagio, 2),
                    round(combustivel, 2), round(total, 2),
                    f"Manual em {datetime.now():%d/%m/%Y %H:%M}"
                )
            )

            conn.commit()
            cur.close()
            conn.close()

            flash("Frete manual salvo com sucesso!")
            return redirect(url_for('historico_fretes'))

        except Exception as e:
            flash(f"Erro ao salvar frete manual: {e}")

    return render_template('frete_manual.html')

# =====================================================

##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################

#################################################################
###################     Consulta de dados       #################

@app.route('/proc_cliente', methods=["GET"])
def proc_cliente():
    data = request.args
    DOC   = data.get('clientCPF', '').strip()
    NOME     = data.get('clientName', '').strip()
    TEL      = data.get('clientPhone', '').strip()
    src = 'SELECT CLI_NOME AS NOME, CLI_DOC AS DOCUMENTO, CLI_TEL AS TELEFONE, CLI_OBSERVA AS OBSERVAÇÕES FROM CLIENTE WHERE D_E_L_E_T_ IS NULL'
    # FORMATA PARA BUSCA PARCIAL

    if DOC:
        src += f" AND CLI_DOC ILIKE \'%{DOC}%\'"
    
    if NOME:
        src += f" AND CLI_NOME ILIKE \'%{NOME}%\'"
    
    if TEL:
        src += f" AND CLI_TEL ILIKE \'%{TEL}%\'"
    
    src += ' ORDER BY CLI_NOME ASC;'

    conn = get_db_connection()
    cur = conn.cursor()


    try:
        cur.execute(src)
        rows = cur.fetchall()
    
    except:
        mensagem = 'Cliente não encontrado!'
        return redirect(url_for(dir_cadastro_clientes))

    cur.close()
    conn.close()

    return render_template("cadastro_clientes.html", rows=rows)


@app.route('/proc_prd', methods=["GET"])
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
 
@app.route('/proc_srv', methods=["GET"])
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

############################# ROTAS PARA VENDA #####################

@app.route("/buscar_cliente")
def buscar_cliente():
    cpf = request.args.get("cpf", "").strip()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT CLI_DOC, CLI_NOME, CLI_TEL FROM CLIENTE WHERE D_E_L_E_T_ IS NULL AND CLI_DOC ILIKE %s LIMIT 1", (f"%{cpf}%",))
    resultado = cur.fetchone()
    
    cur.close()
    conn.close()

    if resultado:
        doc   = resultado[0]
        nome  = resultado[1]
        tel   = resultado[2]
        global cliente
        cliente = [doc,nome,tel]
        return jsonify({"nome": nome, "telefone": tel, "doc": doc})
    return jsonify({"erro": "Cliente não encontrado"}), 404

@app.route("/vendas/carrinho")
def init_carrinho():
    global cliente
    global carrinho

    doc = cliente[0]
    nome = cliente[1]

    carrinho = []

    return render_template("carrinho.html", cli_doc = doc, cli_nome = nome )

@app.route('/buscar-item', methods=['GET'])
def buscar_item():
    tipo = request.args.get('tipo')
    termo = request.args.get('texto')

    if tipo not in ['produto', 'servico']:
        return jsonify({'erro': 'Tipo inválido'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    if tipo == 'produto':
        cur.execute("SELECT PRD_CODIGO AS id, PRD_NOME AS nome, PRD_OBSERVA AS observa, PRD_PRECO AS preco FROM produto WHERE PRD_NOME ILIKE %s OR PRD_CODIGO::text ILIKE %s",
                    (f"%{termo}%", f"%{termo}%"))
    else:
        cur.execute("SELECT SRV_CODIGO AS id, SRV_NOME AS nome, SRV_OBSERVA AS observa, SRV_PRECO AS preco FROM servico WHERE SRV_NOME ILIKE %s OR SRV_CODIGO::text ILIKE %s",
                    (f"%{termo}%", f"%{termo}%"))

    resultados = cur.fetchall()
    cur.close()
    conn.close()

    colnames = [desc[0] for desc in cur.description]
    dados = [dict(zip(colnames, row)) for row in resultados]


    return jsonify(dados)

def dltitemcart(item):
    global carrinho

    for i in carrinho:
        print(i)
        if i[1] == str(item):
            inx = carrinho.index(i)
            print(50*i)
            carrinho.pop(inx)
            break
    return

@app.route('/montar_cart')
def montar_cart():
    global cliente

    cli_nome = cliente[1]
    cli_doc = cliente[0]

    return render_template("carrinho.html", rows = carrinho, cli_nome = cli_nome, cli_doc = cli_doc)

@app.route('/add_item_cart', methods=['GET'])
def add_item_cart():
    global carrinho
    
    data = request.args
    id = data.get('id')
    # tipo = data.get('tipo')
    nome = data.get('itemnome')
    desc = data.get('descricao')
    preco = data.get('preco')

    newitemCart = (id,nome,desc,preco)

    if newitemCart:
        carrinho.append(newitemCart)
    else:
        print(newitemCart)

    return redirect(url_for('montar_cart'))

@app.route('/dlt_item_cart', methods=['POST'])
def dlt_item_cart():
    data = request.form
    item = data.get('codigo')

    print(item)
    dltitemcart(item)
    return redirect(url_for('montar_cart'))

if __name__ == '__main__':
    app.run(debug=True)