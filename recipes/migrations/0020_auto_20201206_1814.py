# Generated by Django 3.1.3 on 2020-12-06 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0019_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='tag',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.CharField(choices=[('orange', 'Завтрак'), ('green', 'Обед'), ('purple', 'Ужин')], default='orange', max_length=10),
        ),
    ]