#!/usr/bin/env python3

from app import app
from models import db, Dealership, Owner, Car
from faker import Faker
import random
import datetime

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        Car.query.delete()
        Owner.query.delete()
        Dealership.query.delete()



        print("Making owners...")

        owners_list = []

        for _ in range(0, 10):
            owner = Owner(first_name=faker.first_name(), last_name=faker.last_name())
            owners_list.append(owner)

        db.session.add_all(owners_list)
        db.session.commit()



        print("Making dealerships...")

        dealerships_list = []

        for _ in range(0, 10):
            d = Dealership(name=faker.name(), address=faker.address())
            dealerships_list.append(d)

        db.session.add_all(dealerships_list)
        db.session.commit()



        print("Making cars...")

        cars_list = []

        for _ in range(0, 100):
            date = datetime.datetime.strptime(faker.date(), "%Y-%M-%d")
            c = Car(
                make=faker.company(), 
                model=faker.first_name(), 
                date_sold=date,
                dealership=random.choice(dealerships_list),
                owner=random.choice(owners_list)
            )
            cars_list.append(c)

        db.session.add_all(cars_list)
        db.session.commit()

        print("Seeding complete!")
