# Generated by Django 2.2.16 on 2022-06-10 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220610_1516'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_title_author',
        ),
    ]
