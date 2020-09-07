from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db, Movies, Actors

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    '''Load initial data into database.'''
    movies = [
        {'title': 'Title 1', 'release_date': '04-20-2020'},
        {'title': 'Title 2', 'release_date': '04-20-2020'},
        {'title': 'Title 3', 'release_date': '04-20-2020'},
        {'title': 'Title 4', 'release_date': '04-20-2020'},
        {'title': 'Title 5', 'release_date': '04-20-2020'}]
    actors = [
        {'name': 'Name 1', 'age': 21, 'gender': 'F'},
        {'name': 'Name 2', 'age': 21, 'gender': 'F'},
        {'name': 'Name 3', 'age': 21, 'gender': 'F'},
        {'name': 'Name 4', 'age': 21, 'gender': 'F'},
        {'name': 'Name 5', 'age': 21, 'gender': 'F'}]

    for movie in movies:
        Movies(title=movie['title'],
               release_date=movie['release_date']).insert()
    for actor in actors:
        Actors(name=actor['name'],
               age=actor['age'],
               gender=actor['gender']).insert()


if __name__ == '__main__':
    manager.run()
