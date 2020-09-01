import os
from flask import Flask, request, abort, jsonify, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors
from auth.auth import AuthError, requires_auth
from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    formatted = [data.format() for data in selection]
    current = formatted[start:end]
    return current


def create_app(test_config=None):

    app = Flask(__name__,)
    app.debug = True
    setup_db(app)
    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Contorl-Allow-Headers',
                             'Content-Type, Athurization true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.order_by(Movies.id).all()
            movies_per_page = paginate(request, movies)
            if(len(movies_per_page) == 0):
                abort(404)

            return jsonify({
              'success': True,
              'movies': movies_per_page,
              'total_movies': len(movies)
            }, 200)

        except Exception as e:
            abort(404)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actors.query.order_by(Actors.id).all()
            actors_per_page = paginate(request, actors)
            if(len(actors_per_page) == 0):
                abort(404)

            return jsonify({
              'success': True,
              'actors': actors_per_page,
              'total_actors': len(actors)
            }, 200)

        except Exception as e:
            abort(404)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def new_movie(payload):
        try:
            body = request.get_json()
            newMovie = Movies(title = body.get('title', None), release_date = body.get('release_date', None))
            newMovie.insert()
            return jsonify({
              'success': True,
              'movie': newMovie.format(),
              'total_movies': len(Movies.query.all())
            }, 200)

        except Exception as e:
            abort(405)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def new_actor(payload):
        try:
            body = request.get_json()
            newActor = Actors(name = body.get('name'), age = body.get('age'), gender = body.get('gender'))
            newActor.insert()
            return jsonify({
              'success': True,
              'actor': newActor.format(),
              'total_actors': len(Actors.query.all())
            }, 200)

        except Exception as e:
            abort(405)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if(movie is None):
                abort(422)

            movie.delete()
            return jsonify({
              'success': True,
              'movie': movie_id,
              'total_movies': len(Movies.query.all())
            }, 200)

        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if(actor is None):
                abort(422)
            actor.delete()
            total_actors = len(Actors.query.all())
            return jsonify({
              'success': True,
              'actor': actor_id,
              'total_actors': total_actors
            }, 200)

        except Exception as e:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload, movie_id):
        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if(movie is None):
                abort(422)
            body = request.get_json()
            movie.title = body.get('title', None)
            movie.release_date = body.get('release_date', None)
            movie.update()
            return jsonify({
              'success': True,
              'movie': movie.format()
            }, 200)

        except Exception as e:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):
        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if(actor is None):
                abort(422)
            body = request.get_json()
            actor.name = body.get('name', None)
            actor.age = body.get('age', None)
            actor.gender = body.get('gender', None)
            actor.update()
            return jsonify({
              'success': True,
              'actor': actor.format()
            }, 200)

        except Exception as e:
            abort(422)

    @app.errorhandler(AuthError)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
      }, error.status_code)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
           }), 422

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
           })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unathorized'
        }, 401)
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }, 500)

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(debug=True)
    # APP.run(host='0.0.0.0', port=8080, debug=True)
