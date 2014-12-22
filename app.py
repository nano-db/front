import json
import falcon
from nanodb_driver import Driver
from wsgiref import simple_server


class CubesResource(object):
    def __init__(self, connector):
        """Cubes Resource API

        :param connector: NanoDB connector
        :type connector: Driver
        """
        self.connector = connector

    def on_get(self, req, resp):
        list = self.connector.list_cubes()
        resp.data = json.dumps(list)
        resp.status = falcon.HTTP_200


class CubeResource(object):
    def __init__(self, connector):
        """Cube Resource API

        :param connector: NanoDB connector
        :type connector: Driver
        """
        self.connector = connector

    def on_get(self, req, resp, name):
        try:
            info = self.connector.get_information(name)
        except Exception, e:
            resp.status = falcon.HTTP_404
        else:
            resp.data = json.dumps(info)
            resp.status = falcon.HTTP_200


app = falcon.API()
driver = Driver(port=5000)

cubes = CubesResource(driver)
cube = CubeResource(driver)

app.add_route('/cubes', cubes)
app.add_route('/cubes/{name}', cube)

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()