from csv import DictReader
from django.core.management import BaseCommand
import codecs

from reviews.models import Category, Title


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from titles.csv"

    def handle(self, *args, **options):
        if Title.objects.exists():
            print('title data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading title data")
        path_file = 'D:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\titles.csv'
        for row in DictReader(codecs.open((path_file), encoding='utf-8')):
            child = Title(id=row['id'], name=row['name'],
                          year=int(row['year']),
                          category=Category.objects.get(
                              pk=row['category']))
            child.save()
