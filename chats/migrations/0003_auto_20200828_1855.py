# Generated by Django 3.0.5 on 2020-08-28 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_auto_20200705_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='image',
        ),
        migrations.AddField(
            model_name='message',
            name='image0',
            field=models.ImageField(blank=True, upload_to='messages/image'),
        ),
        migrations.AddField(
            model_name='message',
            name='image1',
            field=models.ImageField(blank=True, upload_to='messages/image'),
        ),
        migrations.AddField(
            model_name='message',
            name='image2',
            field=models.ImageField(blank=True, upload_to='messages/image'),
        ),
        migrations.AddField(
            model_name='message',
            name='image3',
            field=models.ImageField(blank=True, upload_to='messages/image'),
        ),
        migrations.AddField(
            model_name='message',
            name='image4',
            field=models.ImageField(blank=True, upload_to='messages/image'),
        ),
        migrations.AlterField(
            model_name='message',
            name='file_message',
            field=models.FileField(blank=True, upload_to='messages/file'),
        ),
    ]