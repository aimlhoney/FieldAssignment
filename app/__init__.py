import os
from flask import Flask
from flask_cors import CORS


project_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)

from app.module.controller import *
