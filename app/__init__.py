from flask import Flask, render_template, request, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import LoginManager


import os
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_object(Config)
app.debug = True
login = LoginManager(app)
login.login_view = 'login'


from app import routes, models
user = {'username': 'Miguel'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
