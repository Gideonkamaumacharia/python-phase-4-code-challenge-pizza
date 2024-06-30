#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response,jsonify
from flask_restful import Api, Resource
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address}for restaurant in restaurants]), 200

#route to retrieve restaurant by id
@app.route('/restaurants/<int:id>', methods=['GET'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({'error': 'Restaurant not found'}),404
    #prepare JSON response with specific format
    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'restaurant_pizzas': []
    }
    for rp in restaurant.restaurantpizzas:
        pizza_data = {
            'id':rp.id,
            'restaurant_id': rp.restaurant_id,
            'pizza_id': rp.pizza_id,
            'price': rp.price,
            'pizza': {
                'id':rp.pizza,
                'name': rp.pizza.name,
                'ingredients': rp.pizza.ingredients
            }
        }
        restaurant_data['restaurant_pizzas'].append(pizza_data)
    return jsonify(restaurant_data)

   #route to delete a restaurant
@app.route('/restaurants/<int:id>',methods=['DELETE'])
def delete_restaurant(id):
    session = Session()

    try:
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return jsonify({'error': 'Restaurant not found'}),404
    
    # Delete associated RestauurantPizzas 
        RestaurantPizza.query.filter_by(restaurant_id=id).delete()

        #Delete restaurant
        db.session.delete(restaurant)
        db.session.commit()
        return jsonify({'message': 'Restaurant deleted successfully'}), 204
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Intergrity error occured'}),500
    finally:
        session.close()
    
@app.route('/pizzas')
def get_pizza():
    pizzas = Pizza.query.all()
   
    return jsonify([{'id': pizza.id, 'name':pizza.name, 'ingredients': pizza.ingredients} for pizza in pizzas])

if __name__ == "__main__":
    app.run(port=5555, debug=True)
