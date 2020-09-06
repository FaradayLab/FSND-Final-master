# Capstone Project - Casting Agency

This is the capstone project for the Udacity Full Stack Nanodegree program. 
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. The agency employs a casting assistant, casting director and an executive producer who all have different roles / permissions in the agency.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once the virtual environment is setup and running, install dependencies by navigating to the working project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension used to handle cross origin requests. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to application `app.py`. 


### URLs

Casting Agency URL: https://alex-fsnd-capstone.herokuapp.com/ 
Heroku GitHub repository: https://git.heroku.com/alex-fsnd-capstone.git

## Authentication
#### JTW TOKENS FOR EACH ROLE ARE PROVIDED IN THE ENVIRONMENT FILES AND ARE VALID, SIMPLY RUN TESTS

### Casting Assistant
A casting assistant is only permitted to view actors and movies.

#### Permissions:
```bash
get:actors | get:movies
```

### Casting Director
A casting director is permitted the same as casting assistant plus adding/deleting an actor and modifying actors and movies.

#### Permissions:
```bash
get:actors    | get:movies 
patch:actors  | patch:movies
delete:actors | post:actors
```

### Executive Producer
The executive producer is permitted all operations, including adding/deleting movies

#### Permissions:
```bash
get:actors    | get:movies 
post:actors   | post:movies
patch:actors  | patch:movies
delete:actors | delete:movies 
```

## Endpoints

GET '/movies'
- Returns a dictionary of movies.
- Request Arguments: token
- Returns: Each object in the movies dictionary and an object showing the total number of movies. 
```bash
{
    "movies": [
        {
            "id": 3,
            "release_date": "2004-09-24",
            "title": "Shaun of the Dead"
        },
        {
            "id": 2,
            "release_date": "1979-06-22",
            "title": "Alien"
        }
    ],
    "success": true,
    "total_movies": 2
}
```

GET '/actors'
- Returns a dictionary of actors.
- Request Arguments: token
- Returns: Each actor object in the actors dictionary and an object showing the total number of actors. 
```bash
{
    "actors": [
        {
            "id": 2,
            "name": "Simon Pegg"
            "age": 50,
            "gender": "Male",
        },
        {
            "id": 3,
            "name": "Nick Frost"
            "age": 48,
            "gender": "Female",
        },
        {
            "id": 4,
            "name": "Sigourney Weaver"
            "age": 70,
            "gender": "Female",
        },
    ],
    "success": true,
    "total_actors": 2
}
```

POST '/movies'
- Send key value pairs of title and release_date, for the new movie, to database to be added. 
- Request Arguments: token
- Returns: An object containing the newly created movie, and the total number of movies.
```bash
{
    "success": true,
    "movie": {
        "id": 2,
        "release_date": "2012-05-04",
        "title": "Shaun of the Dead"
      },
    "total_movies": 1
}
```

POST '/actors'
- Send key value pairs of name, age, and gender, for the new actor, to database to be added. 
- Request Arguments: token
- Returns: An object containing the newly created actor and the total number of actors.
```bash
{
    "actor":{
          "id": 2,
          "name": "Simon Pegg"
          "age": 50,
          "gender": "Male",
      },
    "success": true,
    "total_actors": 1
}

```
PATCH '/movies'
- Send key value pairs for the specified fields to be changed. 
- Request Arguments: token, movie_id
- Returns: An object containing the updated movie.
```bash
{
    "success": true,
    "movie": {
        "id": 2,
        "release_date": "2004-09-24",
        "title": "Shaun of the Dead"
    },
}
```

PATCH '/actors'
- Send key value pairs for the specified fields to be changed.
- Request Arguments: token, actor_id
- Returns: An object containing the updated actor.
```bash
{
    "success": true,
    "actor": {
        "age": 48,
        "gender": "Male",
        "id": 3,
        "name": "Nick Frost"
    },
}
```

DELETE '/movies/<int:movie_id>'
- Deletes specified movie from the database
- Request Arguments: token, movie_id 
- Returns: The ID of the deleted movie and the total number of movies.
```bash
{
    "success": true,
    "movie": 1,
    "total_movies": 2
}
```

DELETE '/actors/<int:actor_id>'
- Deletes specified actor from the database
- Request Arguments: token, actor_id 
- Returns: The ID of the deleted actor and total number of actors.
```bash
{
    "success": true,
    "deleted": 1,
    "total_actors": 2
}
```