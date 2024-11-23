from flask import Flask, render_template
from natalidad import natalidad_bp
from mortalidad import mortalidad_bp
from crecimiento_natural import crecimiento_bp

app = Flask(__name__)
app.register_blueprint(mortalidad_bp)
app.register_blueprint(natalidad_bp)
app.register_blueprint(crecimiento_bp)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mortalidad")
def mortalidad():
    return render_template("mortalidad.html")

@app.route('/natalidad')
def natalidad():
    return render_template("natalidad.html")

@app.route('/crecimiento')
def crecimiento():
    return render_template("crecimiento_natural.html")

if __name__ == '__main__':
    app.run(debug=True)
