from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name='Harry')

# @app.route('/')
# def index():
#     return '<h1>Чёкаво!!!</h1>'

# @app.route('/user/<name>')
# def user(name):
#     return '<h1>Hello, {}!</h1>'.format(name)