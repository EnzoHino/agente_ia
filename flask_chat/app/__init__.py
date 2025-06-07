from flask import Flask, render_template

# a aplicacao que estah sendo implementada eh uma instancia da classe Flask
app = Flask(__name__)

# a importacao de "routes" eh feita no final
# para evitar referencia circular nos imports
# (no arquivo routes eh necessario importar app)
from routes import bp
app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)
