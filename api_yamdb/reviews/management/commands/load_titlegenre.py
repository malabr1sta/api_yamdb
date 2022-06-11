from csv import DictReader
from django.core.management import BaseCommand
import codecs

from reviews.models import Genre, Title, TitleGenre


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from genre_title.csv"

    def handle(self, *args, **options):
        if TitleGenre.objects.exists():
            print('genre_title data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading genre_title data")
        pat = 'D:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\genre_title.csv'
        for row in DictReader(codecs.open((pat), encoding='utf-8')):
            child = TitleGenre(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                genre=Genre.objects.get(pk=row['genre_id'])
            )
            child.save()
