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
