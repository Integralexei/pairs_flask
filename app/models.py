from enum import unique
from hello import db
from datetime import datetime
class Symbol(db.Model):
    __tablename__ = 'symbols'
    id = db.Column(db.Integer, primary_key=True)
    symbol_name = db.Column(db.String(16), nullable=False)

    prices = db.relationship('Price', backref='symbol', uselist = False)
    
    def __repr__(self):
        return "<Symbol {}>".format(self.symbol_name)

class Price(db.Model):
    __tablename__ = 'prices'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True)
    symbol_name = db.Column(db.String(64), nullable=False, unique=True)
    price = db.Column(db.Numeric(16, 4), nullable=False)

    symbol_id = db.Column(db.Integer(), db.ForeignKey('symbols.id'), nullable=False)
    
    def __repr__(self):
        return "<Symbol {}, Date: {} , Price: {}>".format(self.symbol_name, self.date, self.price)

#    https://smart-lab.ru/blog/422980.php db schema

