from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

flows = {}


class UpdataFLow(Resource):

    def get(self, control_id):
        return {control_id: flows[control_id]}

    def put(self, control_id):
        flows[control_id] = request.form['data']
        print {control_id: flows[control_id]}
        return {control_id: flows[control_id]}


api.add_resource(UpdataFLow, '/<string:control_id>')

if __name__ == '__main__':
    app.run(debug=True)

