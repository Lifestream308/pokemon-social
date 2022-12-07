from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# Below is elephant sql database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ikqcpqmt:XAjcIV0wn1AB2dZv3_QHr2U-RRgWzday@heffalump.db.elephantsql.com/ikqcpqmt'
# Below is Heroku database  
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vhrqoutdtfwqih:ee04557886db9b747029d2969d08daf410b0fc521a3325c982291cea8c12b8e6@ec2-52-205-98-159.compute-1.amazonaws.com:5432/d6mfch3vglar1o'
CORS(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from capstone import routes

# To create Database go into Python, >>>from capstone import db           >>>db.create_all()     
# To delete Database go into Python, >>>from capstone import db           >>>db.drop_all()