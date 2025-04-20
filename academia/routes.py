from academia import app
from flask import render_template 


@app.route("/")
def page_home():
    return render_template("home.html")

@app.route("/registrar_plano")
def page_registrar_plano():
    return render_template("registrar_plano.html")