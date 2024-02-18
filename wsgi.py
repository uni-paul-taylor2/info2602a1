import click
import csv
from tabulate import tabulate
from App import db, User, Pokemon, UserPokemon
from App import app

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  with open("pokemon.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
      pass
  print('database initialized')