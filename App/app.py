import os, csv
from json import dumps
from flask import Flask, jsonify, request, Response
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
def stringifiedArr(someCollection):
  string=""
  firstTime=True
  for item in someCollection:
    if firstTime:
      firstTime=False
      string+= item.__repr__()
    else:
      string+= ","+item.__repr__()
  return "["+string+"]"
def jsonHeader(text,code):
  resp=Response(text,code)
  resp.headers['Content-Type']="application/json"
  return resp
from .models import db, User, UserPokemon, Pokemon

# Configure Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'MySecretKey'
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
app.config['JWT_HEADER_TYPE'] = ""
app.config['JWT_HEADER_NAME'] = "Cookie"


# Initialize App 
db.init_app(app)
app.app_context().push()
CORS(app)
jwt = JWTManager(app)

# ********** Routes START **************
@app.route('/', methods=['GET'])
def index():
  return "<h1>Poke API v1.0</h1>", 200

@app.route('/init', methods=['GET'])
def initialize_db():
  db.drop_all()
  db.create_all()
  with open("pokemon.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
      db.session.add(Pokemon(
        row["attack"],row["defense"],row["height_m"],row["hp"],row["name"],row["pokedex_number"],
        row["sp_attack"],row["sp_defense"],row["speed"],row["type1"],row["type2"],row["weight_kg"]
      ))
    db.session.commit()
  return jsonHeader(dumps({"message":"Database Initialized!"}, indent=4), 200)

@app.route('/pokemon', methods=['GET'])
def listPokemon():
  return stringifiedArr(Pokemon.query.all()), 200

@app.route('/signup', methods=['POST'])
def sign_up():
  existingUser = User.query.filter_by(username=request.json["username"]).first()
  existingEmail = User.query.filter_by(email=request.json["email"]).first()
  if existingUser or existingEmail:
    return jsonHeader(dumps({"error":"username or email already exists"}, indent=4), 400)
  if not request.json["username"] or not request.json["email"] or not request.json["password"]:
    return jsonHeader(untested_exception, 406)
  db.session.add(
    User(request.json["username"], request.json["email"], request.json["password"])
  )
  db.session.commit()
  return jsonHeader(dumps({"message":request.json["username"]+" created"}, indent=4), 201)

@app.route('/login', methods=['POST'])
def login():
  if not request.json["username"] or not request.json["password"]:
    return untested_exception, 406
  user = User.query.filter_by(username=request.json["username"]).first()
  if not user or not user.authenticate(request.json["password"]):
    return dumps({"error":'bad username/password given'}), 401
  token = create_access_token(identity=user.id)
  response = jsonify(access_token=token)
  set_access_cookies(response, token)
  return response, 200

@app.route('/logout', methods=['GET']) #not even tested but yo it was just copy paste so yeah
def logout():
  response = jsonify(message='Logged out')
  unset_jwt_cookies(response)
  return response

@app.route('/mypokemon', methods=['GET','POST'])
@jwt_required()
def show_or_save_user_pokemon():
  if request.method == "POST":
    if not request.json["pokemon_id"] or not request.json["name"]:
      return jsonHeader(untested_exception, 406)
    pokemon = Pokemon.query.filter_by(id=request.json["pokemon_id"]).first()
    if not pokemon:
      return jsonHeader(dumps({"error":str(request.json["pokemon_id"])+" is not a valid pokemon id"}, indent=4), 400)
    userpokemon = UserPokemon.query.filter_by(pokemon_id=request.json["pokemon_id"]).first()
    if userpokemon:
      return jsonHeader(dumps({"error":"pokemon of id "+userpokemon.pokemon_id+" is already owned"}), 406) #another untested exception
    user_id=get_jwt_identity()
    user=User.query.filter_by(id=user_id).first()
    userpokemon=UserPokemon(user_id,request.json["pokemon_id"],request.json["name"])
    db.session.add(userpokemon)
    db.session.commit()
    return jsonHeader(dumps({"message":request.json["name"]+" captured with id: "+str(userpokemon.id)}, indent=4), 201)
  else:
    user_id=get_jwt_identity()
    return jsonHeader(stringifiedArr(UserPokemon.query.filter_by(user_id=user_id)), 200)
  
@app.route('/mypokemon/<int:id>', methods=['GET','PUT','DELETE']) #this line and below with "id" had "pokemon_id"
@jwt_required()
def get_set_or_remove_my_pokemon(id):
  user_id=get_jwt_identity()
  userpokemon=UserPokemon.query.filter_by(id=id).first()
  user=User.query.filter_by(id=user_id).first()
  if not userpokemon or userpokemon.user_id!=user_id:
    return jsonHeader(dumps({"error":f"Id {id} is invalid or does not belong to {user.username}"}, indent=4), 401)
  if request.method == "GET":
    return jsonHeader(userpokemon.__repr__(), 200)
  elif request.method == "PUT":
    if not request.json["name"]:
      return jsonHeader(untested_exception, 406)
    previousName=userpokemon.name
    userpokemon.name=request.json["name"]
    db.session.add(userpokemon)
    db.session.commit()
    return jsonHeader(dumps({"message":f"{previousName} renamed to {userpokemon.name}"}, indent=4), 200)
  else:
    previousName=userpokemon.name
    db.session.delete(userpokemon)
    db.session.commit()
    return jsonHeader(dumps({"message":previousName+" released"}, indent=4), 200)

# ********** Routes STOP **************

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
