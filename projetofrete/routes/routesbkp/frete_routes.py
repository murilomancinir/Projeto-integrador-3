import googlemaps
from config import GOOGLE_MAPS_KEY

from flask import  request,  jsonify, render_template,flash, Blueprint
from db import get_db_connection

frete_bp = Blueprint('frete', __name__)

gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)


@frete_bp.route('/frete', methods=['GET', 'POST'])
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


@frete_bp.route('/frete_manual', methods=['GET', 'POST'])
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
