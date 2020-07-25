# Generated by Django 3.0.5 on 2020-07-10 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0002_auto_20200705_1551'),
        ('blog', '0006_post_bookmark'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0002_auto_20200705_1051'),
        ('proect', '0002_auto_20200710_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proect',
            name='announcement',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='announcement', to='chats.Chat'),
        ),
        migrations.AlterField(
            model_name='proect',
            name='curator',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='proect',
            name='post',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
        migrations.AlterField(
            model_name='proect',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='announcement.Announcement'),
        ),
    ]