
from flask import Blueprint,render_template

paginas_bp = Blueprint('paginas', __name__)

@paginas_bp.route('/')
def index():
    return render_template('index.html')

@paginas_bp.route('/cadastro_clientes')
def dir_cadastro_clientes():
    return render_template('cadastro_clientes.html')

@paginas_bp.route('/cadastro_veiculos')
def dir_cadastro_veiculos():
    return render_template('cadastro_veiculos.html')

@paginas_bp.route('/cadastro_motoristas')
def dir_cadastro_motoristas():
    return render_template('cadastro_motoristas.html')




@paginas_bp.route('/frete')
def dir_pagina_frete():
    return render_template('frete.html')
