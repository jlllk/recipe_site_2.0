# Generated by Django 3.1.3 on 2020-11-26 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20201126_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='name',
            new_name='ingredient',
        ),
    ]
