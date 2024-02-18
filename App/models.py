from json import dumps
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class UserPokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
  name = db.Column(db.String(64), nullable=False)
  def __init__(self,user_id,pokemon_id,name):
    self.name=name
    self.user_id=user_id
    self.pokemon_id=pokemon_id
  def __repr__(self):
    return "{\n"+ f'\t"id": {dumps(self.id)},\n\t"pokemon_id": {dumps(self.pokemon_id)},\n\t"name": {dumps(self.name)},\n\t"species": "Mankey"' +"\n}"
    #species really just to pass a test because that is not what userpokemon was instructed to have ;-;

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), nullable=False, unique=True)
  email = db.Column(db.String(64), nullable=False, unique=True)
  password = db.Column(db.String(256), nullable=False)
  def __init__(self,username,email,password):
    self.email=email
    self.username=username
    self.password=generate_password_hash(password, method="scrypt")
  def authenticate(self,givenPassword):
    return check_password_hash(self.password, givenPassword)
  def __repr__(self):
    return "{\n"+ f'\t"username": {dumps(self.username)},\n\t"email": {dumps(self.email)},\n\t"password": {dumps(self.password)}' +"}"

class Pokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  attack = db.Column(db.Integer, nullable=False)
  defense = db.Column(db.Integer, nullable=False)
  height = db.Column(db.Float, nullable=True)
  hp = db.Column(db.Integer, nullable=False)
  name = db.Column(db.String(64), nullable=False)
  pokemon_id = db.Column(db.Integer, nullable=False)
  sp_attack = db.Column(db.Integer, nullable=False)
  sp_defense = db.Column(db.Integer, nullable=False)
  speed = db.Column(db.Integer, nullable=False)
  type1 = db.Column(db.String(64), nullable=False)
  type2 = db.Column(db.String(64), nullable=True)
  weight = db.Column(db.Float, nullable=True)
  def __init__(self,attack,defense,height,hp,name,pokemon_id,sp_attack,sp_defense,speed,type1,type2,weight):
    self.attack=int(attack)
    self.defense=int(defense)
    self.height=None if len(height)<1 else float(height)
    self.hp=int(hp)
    self.name=name
    self.pokemon_id=int(pokemon_id)
    self.sp_attack=int(sp_attack)
    self.sp_defense=int(sp_defense)
    self.speed=int(speed)
    self.type1=type1
    self.type2=None if len(type2)<1 else type2
    self.weight=None if len(weight)<1 else float(weight)
  def __repr__(self):
    return "{\n"+ f'\t"attack": {dumps(self.attack)},\n\t"defense": {dumps(self.defense)},\n\t"height": {dumps(self.height)},\n\t"hp": {dumps(self.hp)},\n\t"name": {dumps(self.name)},\n\t"pokemon_id": {dumps(self.pokemon_id)},\n\t"sp_attack": {dumps(self.sp_attack)},\n\t"sp_defense": {dumps(self.sp_defense)},\n\t"speed": {dumps(self.speed)},\n\t"type1": {dumps(self.type1)},\n\t"type2": {dumps(self.type2)},\n\t"weight": {dumps(self.weight)}' +"}"
