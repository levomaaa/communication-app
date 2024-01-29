from os import getenv
from flask import Flask


app = Flask(__name__)
app.secret_key = "Secret key1234"

import routes