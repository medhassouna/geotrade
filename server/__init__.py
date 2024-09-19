# /server/__init__.py

from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

# Initialize Flask app and SocketIO
app = Flask(__name__, static_folder='../app/static', template_folder='../app/templates')
socketio = SocketIO(app)

# Import routes
from . import routes

# Function to start the server
def run_server():
    print("Starting the Flask app...")
    socketio.run(app, port=8080, debug=True)
