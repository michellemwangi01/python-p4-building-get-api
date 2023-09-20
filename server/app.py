#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Game, Review, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"


@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    game_dict = {
        "title": game.title,
        "genre": game.genre,
        "platform": game.platform,
        "price": game.price,
    }
    response = make_response(
        game_dict,
        200
    )
    return response


@app.route('/gamess/<int:id>')
def game_by_id_with_serializer(id):
    game = Game.query.filter(Game.id == id).first()
    game_dict = game.to_dict()
    response = make_response(game_dict,200)
    return response


@app.route('/games')
def games():
    games_sorted_by_genre = Game.query.order_by(Game.genre).all()
    hightest_priced_games = Game.query.order_by(Game.price.desc()).limit(10).all()
    games_from_database = Game.query.all()
    games = []
    for game in hightest_priced_games:
        game_dict = {
            "title": game.title,
            "genre:": game.genre,
            "platform": game.platform,
            "price": game.price
        }
        games.append(game_dict)
    response = make_response(jsonify(games), 200, {"Content-Type":"application/json"})
    # NOTE: jsonify() is now run automatically on all dictionaries returned by Flask views. We'll just pass in those dictionaries from now on, so we don't have to use jsonify, it happens in the backgroud for all dictionaries returned by Flask views
    #       Same applies to the header content-type, is unnecessary because it is done automatically by Jsonify

    return response

# game = Game.query.first()
# game.to_dict()

if __name__ == '__main__':
    app.run(debug=True, port=5555)




