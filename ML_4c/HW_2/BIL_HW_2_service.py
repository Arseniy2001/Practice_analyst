from flask import request, abort, make_response
from flask import Flask
from flask import jsonify
from joblib import load
import attention
app = Flask(__name__)

# @app.before_first_request
# def load_global_data():
#     global model
#     model =load("../HW_1/model_Neighbors_fin.mdl")

@app.route('/')
def hello_world():
    return 'I am working! (/api/predict?r=..&g=..&b=..)'
    
@app.route('/api/predict', methods=['GET'])
def predict():
    r = request.args.get('r', type=int)
    g = request.args.get('g', type=int)
    b = request.args.get('b', type=int)


    if (r or g or b) is None:
        bad_request('r or g or b not specified')
    if (r or g or b) < 0:
        bad_request('r or g or b should be greater then 0')
    if (r or g or b) > 255:
        bad_request('r or g or b should be lesser then 255')

    #get prediction
    X_rgb=[[b,g,r]]
    y_pred = model.predict(X_rgb)

    return str(y_pred[0])


def bad_request(message, code=400):
    abort(make_response(jsonify(message=message), code))
    
if __name__ == '__main__':
    global model
    model =load("../HW_1/model_Neighbors_fin.mdl")
    app.run()