#FSND FINAL PROJECT


Endpoints:
GET '/movies'
GET '/acotrs'
DELETE '/movies/<int:movie_id>'
DELETE '/actors/<int:actor_id>'
POST '/movies'
POST '/actors'
PATCH '/movies/<int:movie_id>'
PATCH '/actors/<int:actor_id>'

GET '/movies'
-Fetches movies data as json you should have a specific authorization.
-You can test it in https://fsndfinal.herokuapp.com/ when you login press movies.

GET '/actors'
-Fetches actors data as json you should have a specific authorization.
-You can test it in https://fsndfinal.herokuapp.com/ when you login press actors.

DELETE '/movies/<int:movie_id>'
-Delete a movie by id.
-You can test it by POSTMAN you should have a specific authorization: 
```
DELETE https://fsndfinal.herokuapp.com/movies/<movie_id>
```
-Return: 
{
    'success': True,
    'movie': movie_id,
    'total_movies': total number of movies
}

DELETE '/actors/<int:actor_id>'
-Delete a actor by id.
-You can test it by POSTMAN you should have a specific authorization: 
```
DELETE https://fsndfinal.herokuapp.com/actors/<actor_id>
```
-Return: 
{
    'success': True,
    'actor': actor_id,
    'total_actors': total number of actors
}

POST '/actors'
-Add new actor and you should have a specific authorization.
-You can test it by POSTMAN:
```
POST https://fsndfinal.herokuapp.com/actors
```
{
    "name": "Jerry Seinfeld ",
    "age": 66,
    "gender": "M"
}
-Return object:
{
    "actor": {
      "age": 80,
      "gender": "M",
      "id": 5,
      "name": "Frank "
    },
    "success": true,
    "total_actors": 5
  },
  200

POST '/movies'
-Add new movie and you should have a specific authorization.
-You can test it by POSTMAN:
```
POST https://fsndfinal.herokuapp.com/movies
```
{
    "title": "The Blacklist ",
    "release_date": "2020-02-16"
}
-Return object:
{
    "movie": {
      "id": 5,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "The Blacklist "
    },
    "success": true,
    "total_movies": 5
  },
  200

PATCH '/movies/<int:movie_id>'
-Edit the title or release date and you should have a specific authorization.
-You can test it by POSTMAN:
```
PATCH https://fsndfinal.herokuapp.com/movies/1
```
{
    "title": "new jersy",
    "release_date": "2020-02-16"
}
-Return:
{
    "movie": {
      "id": 1,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "new jersy"
    },
    "success": true
  },
  200

PATCH '/actors/<int:actor_id>'
-Edit the name, age or gender and you should have a specific authorization.
-You can test it by POSTMAN:
```
PATCH https://fsndfinal.herokuapp.com/actors/1
```
{
    "name": "new jersy",
    "age": 10,
    "gender": "M"
}
-Return:
{
    "actor": {
      "age": 10,
      "gender": "M",
      "id": 1,
      "name": "new jersy"
    },
    "success": true
  },
  200


Users to test the endpoints:

-Executive Producer:
Description: All permissions a Casting Director has and… Add or delete a movie from the database.

Email:
executive.producer@fsndfinal.com
password:
Fsndfinal123456

-Casting Director:
Description: All permissions a Casting Assistant has and… Add or delete an actor from the database Modify actors or movies.

Email:
casting.director@fsndfinal.com
password:
Fsndfinal123456

-Casting Assistant:
Description: Can view actors and movies.

Email:
casting.assistant@fsndfinal.com
password:
Fsndfinal123456