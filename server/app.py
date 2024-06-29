#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
   # restaurants_json = [restaurant.to_dict() for restaurant in restaurants]
    return jsonify([{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address}for restaurant in restaurants]), 200

@app.route('/restaurants/<int:id>')
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id = id).all()
    if restaurant:
        body = {'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address}
        status = 200
    else:
        body = { "error": "Restaurant not found"}
        status = 404

    response = make_response(body,status)
    return response
    
if __name__ == "__main__":
    app.run(port=5555, debug=True)
