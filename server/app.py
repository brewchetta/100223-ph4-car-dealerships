#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

from models import db, Dealership, Owner, Car

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

# OWNERS #

@app.get('/owners')
def get_all_owners():
    owners = Owner.query.all()
    owners_to_dict = [ o.to_dict( rules=["-cars"] ) for o in owners ]
    return owners_to_dict, 200


@app.get('/owners/<int:id>')
def get_owner_by_id(id):
    found_owner = Owner.query.filter(Owner.id == id).first()
    if found_owner:
        return found_owner.to_dict(), 200
    else:
        return { "message": "Not found" }, 404


@app.delete('/owners/<int:id>')
def delete_owner(id):
    found_owner = Owner.query.filter(Owner.id == id).first()
    if found_owner:
        db.session.delete(found_owner)
        db.session.commit()
        return {}, 204
    else:
        return { "message": "Not found" }, 404 


# CARS #

@app.post('/cars')
def create_car():
    data = request.json
    try:
        date_sold = datetime.datetime.strptime(data["date_sold"], "%Y-%M-%d")
        new_car = Car(
            make=data.get("make"),
            model=data.get("model"),
            date_sold=date_sold,
            owner_id=data.get("owner_id"),
            dealership_id=data.get("dealership_id")
        )
        db.session.add(new_car)
        db.session.commit()

        return new_car.to_dict(), 201

    except Exception as e:
        return {"error": f"{e}"} ,406


if __name__ == '__main__':
    app.run(port=5555, debug=True)
