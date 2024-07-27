import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import create_app
from models import Actor, Movie
from config import SQLALCHEMY_DATABASE_URI

class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client.get('/movies')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_actors(self):
        res = self.client.get('/actors')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_movie(self):
        new_movie = {
            "title": "Some title",
            "release_date": datetime.now,
        }

        res = self.client().post('/movies', json=new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)