from flask import Flask
from flask import render_template
app = Flask(__name__)

import restaurants
restaurants = restaurants.run("1")

@app.route("/")
def hello():
    return render_template('index.html', restaurants=restaurants)

if __name__ == "__main__":
    app.run()
