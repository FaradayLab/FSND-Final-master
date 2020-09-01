import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors

class MoveisTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'finaltest'
        self.database_path = "postgresql://postgres:postgres@localhost:5432/"+self.database_name
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_movie = {
            'title': 'TEST',
            'release_date': '2020-04-20'
        }

        self.new_actor = {
            'name': 'TEST',
            'age': 25,
            'gender': 'M'
        }

        self.update_movie = {
            'title': 'UPDATED',
            'release_date': '2015-04-20'
        }
        self.update_actor = {
            'name': 'UPDATED',
            'age': 21,
            'gender': 'F'
        }

    def tearDown(self):
        pass

    def test_add_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['title'])
        self.assertTrue(data['release_date'])

    def test_add_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'])
        self.assertTrue(data['age'])
        self.assertTrue(data['gender'])

    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], 1)
        self.assertTrue(data['total_movies'])

    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        movie = Actors.query.filter(Actors.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], 1)
        self.assertTrue(data['total_actors'])

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.asserTrue(data['movies'])
        self.asserTrue(data['total_movies'])

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.asserTrue(data['actors'])
        self.asserTrue(data['total_actors'])

    def test_patch_movie(self):
        res = self.client().patch('/movies/1', json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_patch_movie(self):
        res = self.client().patch('/actors/1', json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_movie_not_found(self):
        res = self.client().get('/movies/111')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_404_actor_not_found(self):
        res = self.client().get('/actors/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_405_movies_creation_not_allowed(self):
        res = self.client().post('/movies/1', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_405_actors_creation_not_allowed(self):
        res = self.client().post('/actors/1', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_422_movie_does_not_exist_to_delete(self):
        res = self.client().delete('/movie/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_actor_does_not_exist_to_delete(self):
        res = self.client().delete('/actor/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_movie_does_not_exist_to_update(self):
        res = self.client().delete('/movie/1000000', json=self.update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_actor_does_not_exist_to_update(self):
        res = self.client().delete('/actor/1000000', json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == "__main__":
    unittest.main()
