
from flask import Blueprint,render_template

paginas_bp = Blueprint('paginas', __name__)

@paginas_bp.route('/')
def index():
    return render_template('index.html')

@paginas_bp.route('/cadastro_clientes')
def dir_cadastro_clientes():
    return render_template('cadastro_clientes.html')

@paginas_bp.route('/cadastro_servicos')
def dir_cadastro_servicos():
    return render_template('cadastro_servicos.html')

@paginas_bp.route('/consulta_servicos')
def dir_consulta_servicos():
    return render_template('consulta_servico.html')

@paginas_bp.route('/frete')
def dir_pagina_frete():
    return render_template('frete.html')
