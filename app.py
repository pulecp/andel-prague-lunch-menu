import json

from flask import Flask
from flask import render_template
import boto3
from datetime import datetime
app = Flask(__name__)

S3_BUCKET_NAME="lunch-for-heroes"
CACHE_FILENAME = "cache.json"

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

    s3_client = boto3.client('s3')

    menu = load_from_cache(name, s3_client)

    if not menu:
        menu = restaurants.process(name)
        save_to_cache(name, menu, s3_client)

    return render_template('index.html', restaurants=menu)


def save_to_cache(key, data, s3_client=None):
    """
    Stores data (string, bytes, or JSON object) to S3.
    :param key: The file path/name in the S3 bucket (e.g., 'user-data/1234.json')
    :param data: The data to store.
    """

    try:
        # Convert Python dict/list to JSON string, then encode to bytes
        body = {
            'date': datetime.now().isoformat(),
            'content': data
        }


        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=f"{key}_{CACHE_FILENAME}",
            Body=json.dumps(body).encode('utf-8'),
            ContentType='application/json'
        )

        return True
    except Exception as e:
        print(f"Error storing to S3: {e}")
        return False

def load_from_cache(key, s3_client=None):
    """
        Loads data from S3 and returns the content as a string or a Python object.
        :param key: The file path/name in the S3 bucket.
        :return: The data content or None on failure.
        """
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=f"{key}_{CACHE_FILENAME}")
        # S3 response body is a StreamingBody object, read it into memory
        data = json.loads(response['Body'].read().decode('utf-8'))

        date = datetime.fromisoformat(data.get('date'))
        today = datetime.today()

        # invalidate cache when its not from current day and its past 1100
        if date.date() < today.date() and today.strftime('%H:%M') > '10:45':
            return None

        return data['content']
    except s3_client.exceptions.NoSuchKey:
        print(f"File not found in S3: {key}")
        return None
    except Exception as e:
        print(f"Error loading {key} from S3: {e}")
        return None

if __name__ == '__main__':
    app.run()
