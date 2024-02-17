import os 
from json import dumps
from flask import Flask, jsonify, request
from functools import wraps
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)
untested_exception=dumps({"error":"improper request parameters"}, indent=4)
from .models import db, User, UserPokemon, Pokemon

# Configure Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MySecretKey'
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False


# Initialize App 
db.init_app(app)
app.app_context().push()
CORS(app)
jwt = JWTManager(app)

# ********** Routes START **************
@app.route('/', methods=['GET'])
def index():
  return "<h1>Poke API v1.0</h1>"

@app.route('/pokemon', methods=['GET'])
def listPokemon():
  return Pokemon.query.all()

@app.route('/signup', methods=['POST'])
def sign_up():
  existingUser = User.query.filter_by(username=request.json.username).first()
  existingEmail = User.query.filter_by(email=request.json.email).first()
  if existingUser or existingEmail:
    return dumps({"error":"username or email already exists"}, indent=4)
  if not request.json.username or not request.json.email or not request.json.password:
    return untested_exception
  User(request.json.username, request.json.email, request.json.password)
  return dumps({"message":request.username+" created"}, indent=4)

@app.route('/login', methods=['POST'])
def login():
  if not request.json.username or not request.json.password:
    return untested_exception
  user = User.query.filter_by(username=request.json.username).first()
  if not user:
    return 'bad username/password given'
  return user.authenticate(request.json.password)

@app.route('/mypokemon', methods=['POST'])
def save_pokemon():
  if not request.json.pokemon_id or not request.json.name:
    return untested_exception
  pokemon = Pokemon.query.filter_by(id=request.json.pokemon_id).first()
  if not pokemon:
    return dumps({"error":request.json.pokemon_id+" is not a valid pokemon id"}, indent=4)
  userpokemon = UserPokemon.query.filter_by(pokemon_id=request.json.pokemon_id).first()
  if userpokemon:
    return dumps({"error":"pokemon of id "+userpokemon.pokemon_id+" is already owned"}) #another untested exception
  user_id=1 #replace with session variable or something? python weird
  user=User.query.filter_by(id=user_id).first()
  userpokemon=UserPokemon(user_id,request.json.pokemon_id,request.json.name)
  return dumps({"message":user.username+" captured with id: "+userpokemon.id}, indent=4)

# ********** Routes STOP **************

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
