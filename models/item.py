from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))  # max name size is 80 char
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id")
    )  # we can link items that have same store id to the store and viceversa
    store = db.relationship(
        "StoreModel"
    )  # we can find a store in the database that matches the store id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        # using sql alchemy to make queries

        return cls.query.filter_by(
            name=name
        ).first()  # same as Select * from items where name= name LIMIT 1
        # is returning an object

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
