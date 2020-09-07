import os
import unittest
import json
from flask import template_rendered
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors
from dotenv import load_dotenv
from manage import seed

# Unpack the environment variables
load_dotenv()
# assigning env variables to contants
CASTING_ASSISTANT = os.environ.get('CASTING_ASSISTANT_JWT')
CASTING_DIRECTOR = os.environ.get('CASTING_DIRECTOR_JWT')
EXECUTIVE_PRODUCER = os.environ.get('EXECUTIVE_PRODUCER_JWT')


def _auth(token):
    return {'Authorization': f'Bearer {token}'}


class CastingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'finaltest'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        # Load initial data into database
        seed()

        self.new_movie = {
            'title': 'TEST TITLE',
            'release_date': '2020-04-20'
        }
        self.new_actor = {
            'name': 'TEST NAME',
            'age': 25,
            'gender': 'M'
        }
        self.update_movie = {
            'title': 'UPDATED TITLE',
            'release_date': '2015-04-20'
        }
        self.update_actor = {
            'name': 'UPDATED NAME',
            'age': 21,
            'gender': 'F'
        }
        self.bad_movie = {
            'bad-title': 'TEST TITLE',
            'release_date': '2020-04-20'
        }
        self.bad_actor = {
            'bad-name': 'TEST NAME',
            'age': 25,
            'gender': 'M'
        }
        self.unprocessable_movie = {
            'title': None,
            'release_date': '2020-04-20'
        }
        self.unprocessable_actor = {
            'name': None,
            'age': 25,
            'gender': 'M'
        }

    def tearDown(self):
        pass

    def test_add_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=_auth(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        movie = data['movie']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(movie['title'])
        self.assertTrue(movie['release_date'])

    def test_add_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=_auth(CASTING_DIRECTOR))
        data = json.loads(res.data)
        actor = data['actor']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actor['name'])
        self.assertTrue(actor['age'])
        self.assertTrue(actor['gender'])

    def test_get_movies(self):
        res = self.client().get('/movies', headers=_auth(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_get_actors(self):
        res = self.client().get('/actors', headers=_auth(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_get_one_movie(self):
        movie_id = Movies.query.first().id
        res = self.client().get(f'/movies/{movie_id}',
                                headers=_auth(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_get_one_actor(self):
        actor_id = Actors.query.first().id
        res = self.client().get(f'/actors/{actor_id}',
                                headers=_auth(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_patch_movie(self):
        movie_id = Movies.query.first().id
        res = self.client().patch(f'/movies/{movie_id}', json=self.update_movie,
                                  headers=_auth(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_patch_actor(self):
        actor_id = Actors.query.first().id
        res = self.client().patch(f'/actors/{actor_id}', json=self.update_actor,
                                  headers=_auth(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_movie(self):
        movie_id = Movies.query.first().id
        res = self.client().delete(f'/movies/{movie_id}',
                                   headers=_auth(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie'], movie_id)
        self.assertTrue(type(data['total_movies']) is int)
        self.assertEqual(movie, None)

    def test_delete_actor(self):
        actor_id = Actors.query.first().id
        res = self.client().delete(f'/actors/{actor_id}',
                                   headers=_auth(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'], actor_id)
        self.assertTrue(type(data['total_actors']) is int)
        self.assertEqual(actor, None)

    # # BAD REQUEST

    def test_400_movies_create_bad_request(self):
        res = self.client().post('/movies', json=self.bad_movie,
                                 headers=_auth(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_400_actors_create_bad_request(self):
        res = self.client().post('/actors', json=self.bad_actor,
                                 headers=_auth(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # # UNAUTHORIZED

    def test_401_actors_create_unauthorized(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=_auth(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_actors_delete_unauthorized(self):
        res = self.client().delete('/actors/3',
                                   headers=_auth(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_movies_create_unauthorized(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=_auth(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_401_movies_delete_unauthorized(self):
        res = self.client().delete('/movies/3',
                                   headers=_auth(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    # # NOT FOUND

    def test_404_movie_not_found(self):
        res = self.client().get('/movies/11100',
                                headers=_auth(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_404_actor_not_found(self):
        res = self.client().get('/actors/10000',
                                headers=_auth(CASTING_ASSISTANT))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_404_movie_not_found_to_update(self):
        res = self.client().patch('/movie/1000000', json=self.update_movie,
                                  headers=_auth(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_404_actor_not_found_to_update(self):
        res = self.client().patch('/actor/1000000', json=self.update_actor,
                                  headers=_auth(CASTING_DIRECTOR))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_404_movie_not_found_to_delete(self):
        res = self.client().delete('/movie/1000',
                                   headers=_auth(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_404_actor_not_found_to_delete(self):
        res = self.client().delete('/actor/1000',
                                   headers=_auth(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # UNPROCESSABLE

    def test_422_movies_create_unprocessable(self):
        res = self.client().post('/movies', json=self.unprocessable_movie,
                                 headers=_auth(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_422_actors_create_unprocessable(self):
        res = self.client().post('/actors', json=self.unprocessable_actor,
                                 headers=_auth(EXECUTIVE_PRODUCER))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


if __name__ == "__main__":
    unittest.main()
