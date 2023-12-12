from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Car(db.Model, SerializerMixin):
    
    __tablename__ = "cars_table"

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    date_sold = db.Column(db.DateTime, nullable=False)

    # foreign keys

    owner_id = db.Column(db.Integer, db.ForeignKey("owners_table.id"))
    dealership_id = db.Column(db.Integer, db.ForeignKey("dealerships_table.id"))

    # relationships

    dealership = db.relationship("Dealership", back_populates="cars")
    owner = db.relationship("Owner", back_populates="cars")

    serialize_rules = ("-dealership.cars", "-owner.cars")

    # custom validation
    @validates('model')
    def validate_model(self, key, val):
        if 3 <= len(val) <= 25 and val.istitle():
            return val
        else:
            raise ValueError("Model must be between 3 and 25 characters and title cased")


class Owner(db.Model, SerializerMixin):
    
    __tablename__ = "owners_table"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    # relationships

    cars = db.relationship("Car", back_populates="owner", cascade="all, delete-orphan")
    dealerships = association_proxy("cars", "dealership")

    serialize_rules = ("-cars.owner",)


class Dealership(db.Model, SerializerMixin):
    
    __tablename__ = "dealerships_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # relationships

    cars = db.relationship("Car", back_populates="dealership", cascade="all, delete-orphan")
    owners = association_proxy("cars", "owner")

    serialize_rules = ("-cars.dealership",)