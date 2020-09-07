import os
import babel
from flask import Flask, request, abort, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__,)
    app.debug = True
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ------------------------------------------------------------------------#
    # Filters
    # ------------------------------------------------------------------------#

    def paginate(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        return [data.format() for data in selection][start:end]

    # ------------------------------------------------------------------------#
    # Routes
    # ------------------------------------------------------------------------#

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Contorl-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return render_template('main.html')

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movies.query.order_by(Movies.id).all()
        current_movies = paginate(request, movies)

        if(len(current_movies) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'movies': current_movies,
            'total_movies': len(movies)
        }), 200

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actors.query.order_by(Actors.id).all()
        current_actors = paginate(request, actors)

        if(len(current_actors) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'actors': current_actors,
            'total_actors': len(actors)
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if(movie is None):
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
        if(actor is None):
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def new_movie(payload):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if 'title' not in body or 'release_date' not in body:
            abort(400)
        if not title or not release_date:
            abort(422)

        movie = Movies(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format(),
            'total_movies': len(Movies.query.all())
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def new_actor(payload):
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400)
        if not name or not age or not gender:
            abort(422)

        actor = Actors(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format(),
            'total_actors': len(Actors.query.all())
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(payload, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        body = request.get_json()
        movie.title = body.get('title', None)
        movie.release_date = body.get('release_date', None)

        if not (movie.title or movie.release_date):
            abort(422)

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        body = request.get_json()
        actor.name = body.get('name', None)
        actor.age = body.get('age', None)
        actor.gender = body.get('gender', None)

        if not (actor.name or actor.age or actor.gender):
            abort(422)

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'movie': movie_id,
            'total_movies': len(Movies.query.all())
        }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'actor': actor_id,
            'total_actors': len(Actors.query.all())
        }), 200

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    @app.errorhandler(400)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': "Unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal Server Error"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
