from flask import render_template, abort
from jinja2 import TemplateNotFound
from app import app


@app.route('/', defaults={'page_name': 'index'})
@app.route('/<string:page_name>/')
def static_page(page_name):
    try:
        return render_template('%s.html' % page_name)
    except TemplateNotFound:
        abort(404)
