from flask import Flask
from flask_bootstrap import Bootstrap
from urllib.request import urlopen
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import socket


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

root_url = 'http://10.132.106.207:8000'


def get_host_ip():
    """ 
    this method return the correct host ip address 
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ipaddr = s.getsockname()[0]
    finally:
        s.close()
    return ipaddr


