from flask import render_template
from . import app, socketio
from .performance_evaluation import start_background_performance_saving
from .data_request import handle_data_request

# Initialization variable
initialized = False

def initialize():
    global initialized
    if not initialized:
        print("Initializing background tasks...")
        start_background_performance_saving()
        initialized = True

# Ensure initialization happens only once
@app.before_request
def before_request():
    initialize()

# Serve the index.html
@app.route('/')
def index():
    print("Serving index.html")
    return render_template('index.html')

# Handle data requests for chart updates
@socketio.on('request_data')
def request_data():
    handle_data_request()
