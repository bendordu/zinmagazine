# Generated by Django 3.0.5 on 2020-07-02 07:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20200701_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='donate_sum',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='product',
            name='file_product',
            field=models.FileField(blank=True, upload_to='products/file/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/image/%Y/%m/%d'),
        ),
    ]