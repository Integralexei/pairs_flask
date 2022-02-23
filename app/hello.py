from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from datetime import datetime
import requests


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://postgres:{os.environ.get("POSTGRES_PASS")}@localhost/pairs_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import *
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/boot')
def boot():
    return render_template('boot.html')


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


if __name__ == "__main__":
    app.run(debug=True, threaded = True)


