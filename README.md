# Lunch menus on Andel in Prague
Website which shows lunch menus of your favorite restaurants

[https://andel-lunch.herokuapp.com/](https://andel-lunch.herokuapp.com/)

## how to run

```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ # python app.py
$ gunicorn app:app --log-file=-
```

Now go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
