from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

# import datetime
import restaurants

pages = [
    'ata',
    'zbra'
]

default_page = 'ata'

@app.route('/', defaults={'name': default_page})
@app.route('/<name>')
def hello(name):

    if name not in pages:
        name = default_page

    menu = restaurants.process(name)
    return render_template('index.html', restaurants=menu)


if __name__ == '__main__':
    app.run()
