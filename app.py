import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Movie, Actor
from flask_moment import Moment
from flask_migrate import Migrate
import sys
from auth import AuthError, requires_auth


def create_app(test_config=None):

  app = Flask(__name__)
  moment = Moment(app)
  app.config.from_object('config')
  db.init_app(app)
  migrate = Migrate(app, db)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/movies')
  @requires_auth('get:movies')
  def get_movies(self):
    movies = Movie.query.all()
    if len(movies) == 0:
      abort(404)
    current_movies = [movie.format() for movie in movies]

    return jsonify({
      'success': True,
      'movies': current_movies
    })

  @app.route('/actors')
  @requires_auth('get:actors')
  def get_actors(self):
    actors = Actor.query.all()
    if len(actors) == 0:
      abort(404)

    current_actors = [actor.format() for actor in actors]

    return jsonify({
      'success': True,
      'actors': current_actors
    })

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_new_movie(self):
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)
    new_actors = body.get('actors', None)

    try:
      movie = Movie(title=new_title, release_date=new_release_date, actors=new_actors)
      movie.insert()
      return jsonify({
        'success': True
      })
    except:
      db.session.rollback()
      print(sys.exc_info())
      abort(422)
    finally:
      db.session.close()

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_new_actor(self):
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)
    new_movie_id = body.get('movie_id', None)

    try:
      actor = Actor(name=new_name, age=new_age, gender=new_gender, movie_id=new_movie_id)
      actor.insert()
      return jsonify({
        'success': True
      })
    except:
      db.session.rollback()
      print(sys.exc_info())
      abort(422)
    finally:
      db.session.close()

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
      abort(404)
    body = request.get_json()
    movie.title = body.get('title', None)
    movie.release_date = body.get('release_date', None)
    movie.actors = body.get('actors', None)

    try:
      movie.update()
      return jsonify({
        'success': True
      })
    except:
      db.session.rollback()
      print(sys.exc_info())
      abort(422)
    finally:
      db.session.close()

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
      abort(404)
    body = request.get_json()
    actor.title = body.get('title', None)
    actor.release_date = body.get('release_date', None)
    actor.actors = body.get('actors', None)

    try:
      actor.update()
      return jsonify({
        'success': True
      })
    except:
      db.session.rollback()
      print(sys.exc_info())
      abort(422)
    finally:
      db.session.close()

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)

    try:
      movie.delete()
      return jsonify({
        'success': True
      })
    except:
      db.session.rollback()
      print(sys.exc_info())
      abort(422)
    finally:
      db.session.close()

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
      abort(404)

    try:
      actor.delete()
      return jsonify({
        'success': True
      })
    except:
      db.session.rollback()
      print(sys.exc_info())
      abort(422)
    finally:
      db.session.close()
  """
  Create error handlers for all expected errors
  including 404 and 422.
  """

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "resource not found"}), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({"success": False, "error": 500, "message": "internal server error"}), 500

  return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
