from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

# import datetime
import restaurants

pages = dict()

DEFAULT_PAGE = 'andel'

for page in os.listdir('pages'):
    pages[page.replace('.json', '')] = restaurants.run(page)


@app.route('/', defaults={'name': DEFAULT_PAGE})
@app.route('/<name>')
def hello(name):
    if name not in pages:
        name = DEFAULT_PAGE
        # return render_template('404.html')
    return render_template('index.html', restaurants=pages[name])


if __name__ == '__main__':
    app.run()
