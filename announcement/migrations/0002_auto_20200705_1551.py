# Generated by Django 3.0.5 on 2020-07-05 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='announcement',
        ),
    ]
