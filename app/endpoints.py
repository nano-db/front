import os
from flask import jsonify, send_file, request, _request_ctx_stack
from nanodb_driver.driver import ServerRequestError
from app import app, nano_db


@app.before_request
def before_request():
    print("bite")
    method = request.form.get('_method', '').upper()
    if method:
        request.environ['REQUEST_METHOD'] = method
        ctx = _request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method


@app.route('/api/cubes/', methods=['GET'])
def cubes():
    cube_list = nano_db.list_cubes()
    return jsonify(cubes=cube_list)


@app.route('/api/cubes/<string:cube_name>/', methods=['GET'])
def cube(cube_name):
    try:
        c = nano_db.get_information(cube_name)
    except ServerRequestError, e:
        return jsonify(error=404, text=str(e)), 404
    else:
        return jsonify(c)


@app.route('/api/cubes/<string:cube_name>/serialize', methods=['GET'])
def serialize(cube_name):
    path = "/tmp/" + cube_name + ".nano"
    if not os.path.isfile(path):
        try:
            nano_db.serialize(cube_name, path=path)
        except ServerRequestError, e:
            return jsonify(error=404, text=str(e)), 404
    return send_file(path,  mimetype="application/nanodb",
                     attachment_filename=cube_name + ".nano")

@app.route('/api/cubes/<string:cube_name>/delete', methods=['GET'])
def drop(cube_name):
    try:
        nano_db.drop(cube_name)
    except ServerRequestError, e:
        return jsonify(error=404, text=str(e)), 404
    else:
        return jsonify({})