from flask import render_template

from server import app

@app.route("/")
def index():
    return render_template("index.html", title="KPKI")
