from flask import Flask
from flask_cors import CORS

from routes.cliente_routes import cliente_bp
from routes.veiculo_routes import veiculo_bp
from routes.motorista_routes import motorista_bp
from routes.consulta_servico_routes import consulta_servico_bp
from routes.cadastro_servico_routes import cadastro_servico_bp
from routes.views import paginas_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(paginas_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(veiculo_bp)
app.register_blueprint(motorista_bp)
app.register_blueprint(cadastro_servico_bp)
app.register_blueprint(consulta_servico_bp)


if __name__ == '__main__':
    app.run(debug=True)