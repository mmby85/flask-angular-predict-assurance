import numpy as np
from flask import Flask, request, render_template, jsonify
import pickle
from flask_sqlalchemy import SQLAlchemy 
import json
import os

# Init app
flask_app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(flask_app)

# uncomment next ligne to create database for the first time then run app.py and finilly comment it again, important !!!!!!!!
# db.create_all()

# Product Class/Model
class Data(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  gender = db.Column(db.Integer)
  age = db.Column(db.Integer)
  licence = db.Column(db.Integer)
  prev_insured = db.Column(db.Integer)
  vehiicle_age = db.Column(db.Integer)
  vehicle_Damage = db.Column(db.Integer)
  prediction = db.Column(db.String(100) , unique=False)


  def __init__(self, gender, age, licence, prev_insured, vehiicle_age, vehicle_Damage, prediction):
    self.gender = gender
    self.age = age
    self.licence = licence
    self.prev_insured = prev_insured
    self.vehiicle_age = vehiicle_age
    self.vehicle_Damage = vehicle_Damage
    self.prediction = prediction


def Valuepredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 6)
    loaded_model = pickle.load(open("pima.pickle", "rb"))
    # pred = loaded_model.predict(to_predict)
    return  np.random.choice([0,1])#'pred[0]'

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods = ["POST"])
def predict():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        print(to_predict_list)
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        print(to_predict_list)
        pred = Valuepredictor(to_predict_list)

        if int(pred) == 1:
                prediction = 'decline this contract'
        else:
                prediction = 'accept this contract'

        new_data = Data(to_predict_list[0] ,to_predict_list[1] ,to_predict_list[2] ,to_predict_list[3] ,to_predict_list[4] ,to_predict_list[5] ,prediction)
        
        db.session.add(new_data)
        db.session.commit()
        
        return render_template("index.html")


@flask_app.route("/data", methods = ["GET"])
def get_data():
    if request.method == "GET":
        data = Data.query.all()
        data =  [{ elm : vars(d)[elm] for i, elm in enumerate(vars(d)) if i != 0} for d in data ]
        print(data)
        return jsonify(data)
if __name__ == "__main__":
    flask_app.run(debug=True)