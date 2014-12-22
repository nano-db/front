import json
from flask import jsonify
from nanodb_driver.driver import ServerRequestError
from app import app, nano_db


@app.route('/api/cubes/', methods=['GET'])
def cubes():
    cubes = nano_db.list_cubes()
    return json.dumps(cubes)


@app.route('/api/cubes/<string:cube_name>/', methods=['GET'])
def cube(cube_name):
    try:
        cube = nano_db.get_information(cube_name)
    except ServerRequestError, e:
        return jsonify(error=404, text=str(e)), 404
    else:
        return json.dumps(cube)