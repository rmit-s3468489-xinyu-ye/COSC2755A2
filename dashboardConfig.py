from flask import Flask
from flask_bootstrap import Bootstrap
from urllib.request import urlopen
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

USER = 'root'
PASS = 's3468489'
HOST = '35.189.55.205'
DBNAME = 'Project'


app.config.update(
    DEBUG=True,
    SECRET_KEY='I LOVE HACKING!',
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

bootstrap  = Bootstrap(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

root_url = 'http://http://10.132.105.95:8000'
