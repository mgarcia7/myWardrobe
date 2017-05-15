from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku


import json
from bson import json_util
from bson.json_util import dumps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mywardrobe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#heroku = Heroku(app)
db = SQLAlchemy(app)

from models import *



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_outfit',methods = ['POST'])
def add_outfit():
   if request.method == 'POST':
      result = request.form

      date = result.pop('date_outfit_worn')
      rating = result.pop('rating')
      notes = result.pop('notes')

      # Try to find outfit in database

      # If not in database, put outfit into database

      # Create log in database using form data

      return render_template("success.html")

@app.route("/items_info")
def items_info():
    results = Item.query.all()
    json_results = []

    for x in results:
        json_results.append({"itemID":x.id, "itemDesc":x.desc})

    return json.dumps(json_results, default=json_util.default)


if __name__ == '__main__':
    app.debug = True
    app.run()