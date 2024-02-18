import click
import csv
from tabulate import tabulate
from App import db, User, Pokemon, UserPokemon
from App import app

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  #db.session.add_all([
    #User('bob', 'bob@mail.com', 'bobpass'),
    #User('rick', 'rick@mail.com', 'rickpass'),
    #User('sally', 'sally@mail.com', 'sallypass'),
  #])
  #db.session.commit()
  with open("pokemon.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
      db.session.add(Pokemon(
        row["attack"],row["defense"],row["height_m"],row["hp"],row["name"],row["pokedex_number"],
        row["sp_attack"],row["sp_defense"],row["speed"],row["type1"],row["type2"],row["weight_kg"]
      ))
    db.session.commit()
  print('database initialized')