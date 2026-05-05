
from flask import  request,  jsonify, render_template, Blueprint
from db import get_db_connection

# Cria um bluprint para separar da rota principal (app)
cliente_bp = Blueprint('cliente', __name__)

# Busca o último código de cliente
def max_cli_cod():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(CLI_CODIGO) FROM CLIENTE;")
    last_cli_cod = cur.fetchone()[0]

    if not last_cli_cod:
        last_cli_cod = 0

    cur.close()
    conn.close()
    return last_cli_cod

# Adiciona um cliente
@cliente_bp.route('/add_cliente', methods=['POST'])
def add_cliente():
    data = request.form
    ad_CLI_CODIGO     = max_cli_cod() + 1
    ad_CLI_NOME       = data.get('clientName', '').strip()
    ad_CLI_ENDERECO   = data.get('clientAddress', '').strip()
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
        cur.execute("""
            INSERT INTO CLIENTE (
                CLI_CODIGO, CLI_NOME, CLI_ENDERECO, CLI_COMPLEMENT,
                CLI_CEP, CLI_TEL, CLI_DOC, CLI_OBSERVA,
                D_E_L_E_T_, R_E_C_N_O_, R_E_C_D_E_L_
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL, 1, NULL);
        """, (
            ad_CLI_CODIGO, ad_CLI_NOME, ad_CLI_ENDERECO, ad_CLI_COMPLEMENT,
            ad_CLI_CEP, ad_CLI_TEL, ad_CLI_DOC, ad_CLI_OBSERVA
        ))
        conn.commit()
        rows = [(ad_CLI_NOME, ad_CLI_DOC, ad_CLI_TEL, ad_CLI_OBSERVA)]
        return render_template("cadastro_clientes.html", alert="Cliente adicionado com sucesso!", rows=rows)

    except Exception as e:
        conn.rollback()
        return render_template("cadastro_clientes.html", alert=f"Erro ao cadastrar: {str(e)}", rows=[])
 
    finally:
        cur.close()
        conn.close()

# Deletar cliente # usado post como metodo para náo excluir apenas esconder para o usuário
@cliente_bp.route('/dlt_cliente', methods=['POST'])
def dlt_cliente():
    codigo = request.form.get('codigo')
    codigo = str(codigo)

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("UPDATE CLIENTE SET D_E_L_E_T_ = %s WHERE CLI_DOC = %s;", ('*', codigo))
        conn.commit()
        return render_template("cadastro_clientes.html", alert="Cliente excluído com sucesso")

    except Exception as e:
        conn.rollback()
        return render_template("cadastro_clientes.html", alert=f"Erro ao excluir cliente: {e}")

    finally:
        cur.close()
        conn.close()


@cliente_bp.route('/proc_cliente', methods=['GET'])
def proc_cliente():
    data = request.args
    DOC  = data.get('clientCPF', '').strip()
    NOME = data.get('clientName', '').strip()
    TEL  = data.get('clientPhone', '').strip()

    src = '''
        SELECT CLI_NOME AS NOME,
               CLI_DOC AS DOCUMENTO,
               CLI_TEL AS TELEFONE,
               CLI_OBSERVA AS OBSERVACOES
        FROM CLIENTE
        WHERE D_E_L_E_T_ IS NULL
    '''

    params = []

    if DOC:
        src += " AND CLI_DOC ILIKE %s"
        params.append(f"%{DOC}%")

    if NOME:
        src += " AND CLI_NOME ILIKE %s"
        params.append(f"%{NOME}%")

    if TEL:
        src += " AND CLI_TEL ILIKE %s"
        params.append(f"%{TEL}%")

    src += " ORDER BY CLI_NOME ASC;"

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(src, params)
        rows = cur.fetchall()
        return render_template("cadastro_clientes.html", rows=rows)

    except Exception as e:
        return render_template("cadastro_clientes.html", alert=f"Erro ao buscar cliente: {e}", rows=[])

    finally:
        cur.close()
        conn.close()

@cliente_bp.route("/buscar_cliente")
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