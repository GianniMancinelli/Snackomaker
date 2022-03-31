from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
import random


app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True, port=5000)