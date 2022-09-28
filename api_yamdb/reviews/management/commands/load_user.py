from csv import DictReader
from django.core.management import BaseCommand
import codecs

from reviews.models import User


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from users.csv"

    def handle(self, *args, **options):
        if User.objects.exists():
            print('user data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading user data")
        path_file = 'D:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\users.csv'
        for row in DictReader(codecs.open((path_file), encoding='utf-8')):
            child = User(id=row['id'], username=row['username'],
                         email=row['email'], role=row['role'], bio=row['bio'],
                         first_name=row['first_name'],
                         last_name=row['last_name'])
            child.save()
