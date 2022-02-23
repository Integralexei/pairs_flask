from app.hello import db
from datetime import datetime
class Symbol(db.Model):
    __tablename__ = 'symbols'
    id = db.Column(db.Integer, primary_key=True)
    symbol_name = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return "< Symbol {}>".format(self.symbol_name)

#    https://smart-lab.ru/blog/422980.php db schema

# class Role(db.Model): 
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)

#     users = db.relationship('User', backref='role')

#     def __repr__(self):
#         return '<Role %r>' % self.name

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, index=True)

#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

#     posts = db.relationship('Post', backref='users')

#     def __repr__(self):
#         return '<User %r>' % self.username

# class Post(db.Model):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     content = db.Column(db.Text(), nullable=False)
#     created_on = db.Column(db.DateTime(), default=datetime.utcnow)

#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

#     def __repr__(self):
#         return "<{}:{}>".format(self.id,  self.title[:10])