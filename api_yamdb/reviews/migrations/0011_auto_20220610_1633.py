# Generated by Django 2.2.16 on 2022-06-10 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20220610_1627'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_author_title',
        ),
    ]
