from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))  # max name size is 80 char

    # item = db.relationship('ItemModel') #this says there is a relationship between Storemodel and itemmodel
    # this is a many to one relationship so
    # item is a list of items
    # and it will be created an object for every item in the Store
    # to reduce the amount of memory used we will use
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }  # .all transform self.items in a query builder insted of a list and .all retrieves all the items in that table
        # this will make this method slower (it's a trade off.. previous version will have store creation slower)

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
