from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import time
from datetime import datetime
import random
import requests


load_dotenv()
# env_path = r'C:\py_proj\pairs_flask\.env'
# load_dotenv(dotenv_path=env_path)



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://postgres:{os.environ.get("POSTGRES_PASS")}@localhost/pairs_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

random.seed()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/boot')
def boot():
    return render_template('boot.html')

@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            # time.sleep(1)

    return Response(generate_random_data(), mimetype='text/event-stream')


def get_line_stream():
        api_key = os.environ.get('API_KEY_EXANTE_DEMO')
        token = os.environ.get('TOKEN_EXANTE_DEMO')
        headers={'Accept':'application/x-json-stream'}
        r = requests.get('https://api-demo.exante.eu/md/3.0/feed/trades/ETH.USD',stream=True, headers=headers, auth=(api_key,token))
        print(r)
        for chunk in r.iter_lines(chunk_size=1):
            if chunk:
                yield chunk.decode('utf8')

streamExante = get_line_stream() 

@app.route('/chart-data1')
def chart_data1():
    def generate_data():
        date_obj = datetime.now()
        for i in streamExante:
            i = json.loads(i)
            if "price" in i: 
                date_obj = datetime.fromtimestamp(i['timestamp']//1000)
                i['timestamp'] = str(datetime.fromtimestamp(i['timestamp']//1000))
                json_data = json.dumps({'time': i['timestamp'][-8:], 'value': float(i['price'])})
                print(json_data, 'jsondata')
                yield f"data:{json_data}\n\n"
            else:   
                continue

    return Response(generate_data(), mimetype='text/event-stream')

# class Role(db.Model): .
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

#     def __repr__(self):
#         return '<User %r>' % self.username

if __name__ == "__main__":
    app.run(debug=True, threaded = True)


