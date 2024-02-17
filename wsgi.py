import click
import csv
from tabulate import tabulate
from App import db, User, Pokemon, UserPokemon
from App import app

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  print('database initialized')

@app.cli.command("getRoot", help="returns root of website")
def getRoot():
  return "<h1>Poke API v1.0</h1>"

#@app.cli.command("")