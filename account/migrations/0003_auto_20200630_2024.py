# Generated by Django 3.0.5 on 2020-06-30 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200630_1955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='category',
        ),
        migrations.AddField(
            model_name='profile',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='category', to='account.CategoryProfile'),
        ),
    ]