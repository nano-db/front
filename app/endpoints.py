import os
from flask import jsonify, send_file, request
from nanodb_driver.driver import ServerRequestError
from app import app, nano_db


def check_file_type(file_name, type):
    """Return True if file_name as type as extension
    :type file_name: str
    :type type: str
    :rtype: bool
    """
    return file_name.rsplit('.')[1] == type


@app.route('/api/cubes/', methods=['GET'])
def cubes():
    cube_list = nano_db.list_cubes()
    return jsonify(cubes=cube_list)


@app.route('/api/cubes/', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("files[]")

    if len(uploaded_files) != 2:
        err = ".CSV and .YML file necessary to create the cube"
        return jsonify(error=404, text=err), 404
    elif check_file_type(uploaded_files[0].filename, "csv") and\
            check_file_type(uploaded_files[1].filename, "yml"):
        input_file = uploaded_files[0]
        config_file = uploaded_files[1]
    elif check_file_type(uploaded_files[0].filename, "yml") and\
            check_file_type(uploaded_files[1].filename, "csv"):
        config_file = uploaded_files[0]
        input_file = uploaded_files[1]
    else:
        err = ".CSV and .YML file necessary to create the cube"
        return jsonify(error=404, text=err), 404

    input_path = os.path.join("/tmp", input_file.filename)
    config_path = os.path.join("/tmp", config_file.filename)
    input_file.save(input_path)
    config_file.save(config_path)

    try:
        ret = nano_db.create_cube(input_path, config_path)
    except ServerRequestError, e:
        return jsonify(error=404, text=str(e)), 404
    else:
        return jsonify(ret)


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