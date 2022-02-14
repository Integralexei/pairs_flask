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


def get_line_stream(ticker):
        api_key = os.environ.get('API_KEY_EXANTE_DEMO')
        token = os.environ.get('TOKEN_EXANTE_DEMO')
        headers={'Accept':'application/x-json-stream'}
        r = requests.get(f'https://api-demo.exante.eu/md/3.0/feed/trades/{ticker}',stream=True, headers=headers, auth=(api_key,token))
        print(f'{r}___{ticker}')
        for chunk in r.iter_lines(chunk_size=1):
            if chunk:
                yield chunk.decode('utf8')
                # yield chunk

streamExante1 = get_line_stream('BTC.USD') 
streamExante2 = get_line_stream('ETH.USD') 
# streamExante_second_paper = get_line_stream('ETH.USD') 

@app.route('/chart-data1')
def chart_data1():
    def generate_data():
        date_obj = datetime.now()
        for i in zip(streamExante1, streamExante2) :
            i = [json.loads(x) for x in i] # convert str to type json
            if "price" in i[0] and "price" in i[1]: 
                date_obj = [datetime.fromtimestamp(x['timestamp']//1000) for x in i]
                # if i[0]['timestamp'] == i[1]['timestamp']:
                i[0]['timestamp'] = str(date_obj[0])[-8:]
                i[1]['timestamp'] = str(date_obj[1])[-8:]
                print(f'{i}\n\n')
                json_data1 = i[0]
                json_data2 = i[1]
                json_data = json.dumps({'time1': json_data1['timestamp'], 'value1': float(json_data1['price']),
                                        'time2': json_data2['timestamp'], 'value2': float(json_data2['price'])})
                # print(f'{json_data1}\n{json_data2}')
                yield f"data:{json_data}\n\n"
      
                # else:
                #     continue
            else:   
                continue

    return Response(generate_data(), mimetype='text/event-stream')

# @app.route('/chart-data1')
# def chart_data1():
#     def generate_data():
#         date_obj = datetime.now()
#         for i in zip(streamExante1,streamExante2):
#             print(i)
#             i = json.loads(i)
#             if "price" in i: 
#                 date_obj = datetime.fromtimestamp(i['timestamp']//1000)
#                 i['timestamp'] = str(datetime.fromtimestamp(i['timestamp']//1000))
#                 json_data = json.dumps({'time': i['timestamp'][-8:], 'value': float(i['price'])})
#                 print(json_data, 'jsondata')
#                 yield f"data:{json_data}\n\n"
#             else:   
#                 continue

#     return Response(generate_data(), mimetype='text/event-stream')


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


