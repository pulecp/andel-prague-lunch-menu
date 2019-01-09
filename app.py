from flask import Flask
from flask import render_template

app = Flask(__name__)

# import datetime
import restaurants

# day_of_week = datetime.datetime.today().isoweekday()
# restaurants = restaurants.run(str(day_of_week))
restaurants = restaurants.run()


@app.route("/")
def hello():
    return render_template('index.html', restaurants=restaurants)


if __name__ == "__main__":
    app.run()
