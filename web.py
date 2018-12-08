from flask import Flask
from json import dumps
app = Flask(__name__)

flow = {}


@app.route("/addflow/<flow_t>")
def addflow(flow_t):
    flow['flow'] = flow_t
    return flow_t


@app.route('/getflow')
def getflow():
    return dumps(flow)


if __name__ == '__main__':
    app.run(debug=True)

