from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


if __name__ == "__main__":
    app.run(debug=True)



# Initialize Flask app
app = Flask(__name__)

# Setup database and migration
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)

    pizzas = relationship('RestaurantPizza', back_populates='restaurant')

    serialize_only = ('id', 'name', 'address')  # Serialization rules

    def __repr__(self):
        return f"<Restaurant {self.name}>"

class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String)

    restaurant_pizzas = relationship('RestaurantPizza', back_populates='pizza')

    serialize_only = ('id', 'name', 'ingredients')  # Serialization rules

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    restaurant = relationship('Restaurant', back_populates='pizzas')
    pizza = relationship('Pizza', back_populates='restaurant_pizzas')

    serialize_only = ('id', 'price', 'restaurant_id', 'pizza_id')  # Serialization rules

    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price must be a positive integer")
        return value

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
