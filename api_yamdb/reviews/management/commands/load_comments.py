from csv import DictReader
from django.core.management import BaseCommand
import codecs

from reviews.models import Review, Comment, User


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from comments.csv"

    def handle(self, *args, **options):
        if Comment.objects.exists():
            print('comments data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        print("Loading comments data")
        path_file = 'D:\\Dev\\api_yamdb\\api_yamdb\\static\\data\\comments.csv'
        for row in DictReader(codecs.open((path_file), encoding='utf-8')):
            child = Comment(
                id=row['id'],
                review=Review.objects.get(pk=row['review_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                pub_date=row['pub_date']
            )
            child.save()
