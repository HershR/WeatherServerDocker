from flaskr import db, create_app
from flaskr.models import *

db.create_all(app=create_app())