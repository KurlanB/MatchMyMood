from flask import Flask;
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'

from app import routes