from flask import render_template
from app import app


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)
