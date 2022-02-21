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
                yield json.loads(chunk.decode('utf8'))   # convert str to type json




def synchronized_streams(paper1, paper2):
    lst = ['00:00:00']
    lst2 = ['00:00:00']
    first_paper = get_line_stream(paper1)
    second_paper = get_line_stream(paper2)
    for paper1 in first_paper:
        # print('1')
        if "price" in paper1:
            date_obj1 = datetime.fromtimestamp(paper1['timestamp']//1000)
            paper1['timestamp'] = date_obj1.strftime("%H:%M:%S")
            if paper1['timestamp'] == lst[0]:
                continue
            elif paper1['timestamp'] < lst2[0]:
                continue
            else:
                lst[0] = paper1['timestamp']
            for paper2 in second_paper:
                if "price" in paper2:
                    date_obj2 = datetime.fromtimestamp(paper2['timestamp']//1000)
                    paper2['timestamp'] = date_obj2.strftime("%H:%M:%S")
                    lst2[0] = paper2['timestamp']
                    if paper2['timestamp'] == lst[0]:
                        yield paper1, paper2
                        lst = ['00:00:00']
                        break
                    elif paper2['timestamp'] > lst[0]:
                        next(first_paper)
                        break
                else: 
                    continue
        else: 
            continue
                            
# synchronized_streams('ETH.USD', 'BTC.USD')
        

@app.route('/chart-data1')
def chart_data1():
    def generate_data():
        for i in synchronized_streams('ETH.USD', 'BTC.USD'):
            json_data1 = i[0]
            json_data2 = i[1]
            json_data = json.dumps({'time1': json_data1['timestamp'], 'value1': float(json_data1['price']),
                                    'time2': json_data2['timestamp'], 'value2': float(json_data2['price'])})
            yield f"data:{json_data}\n\n"
            

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


