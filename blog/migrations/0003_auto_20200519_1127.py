# Generated by Django 3.0.5 on 2020-05-19 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
        migrations.AddField(
            model_name='comment',
            name='author_comment',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='comment_created', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, upload_to='comment/%Y/%m/%d'),
        ),
    ]
