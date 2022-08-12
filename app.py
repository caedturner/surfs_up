# import Flask
from flask import Flask

# Create new Flask app instance.
app = Flask(__name__)

# Create Flask Routes
@app.route('/')
def hello_world():
    return 'Hello world'
