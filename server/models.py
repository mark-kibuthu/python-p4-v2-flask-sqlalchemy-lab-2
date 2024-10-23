from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Define metadata with naming conventions for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    # Specify which fields to serialize and exclude
    serialize_only = ('id', 'name', 'reviews')
    serialize_rules = ('-reviews.customer',)  # Exclude customer from reviews

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship to Review
    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy to access items through reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    # Specify which fields to serialize and exclude
    serialize_only = ('id', 'name', 'price', 'reviews')
    serialize_rules = ('-reviews.item',)  # Exclude item from reviews

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship to Review
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    # Specify which fields to serialize and exclude
    serialize_only = ('id', 'comment', 'customer', 'item')
    serialize_rules = ('-customer.reviews', '-item.reviews')  # Exclude reviews from customer and item

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)

    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, Customer {self.customer_id}, Item {self.item_id}>'