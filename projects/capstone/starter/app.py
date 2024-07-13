import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Movie, Actor
from flask_moment import Moment
from flask_migrate import Migrate

def create_app(test_config=None):
  # create and configure the app
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

  
  return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
