from csv import DictReader
from django.core.management import BaseCommand
import codecs

from reviews.models import Genre


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from genre.csv"

    def handle(self, *args, **options):
        if Genre.objects.exists():
            print('genre data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading genre data")
        path_file = 'D:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\genre.csv'
        for row in DictReader(codecs.open((path_file), encoding='utf-8')):
            child = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            child.save()
