from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# def create_app():
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://lukas:lukas@mysql:3306/scraper?charset=utf8'

db = SQLAlchemy(app)

#Register blueprint
from .userendpoints import blueprint
from .models import User

app.register_blueprint(blueprint)

db.create_all()
db.session.commit()

# test_user = User(1, "asd", "omg")
# db.session.add(test_user)
# db.session.commit()