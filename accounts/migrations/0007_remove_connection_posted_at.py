# Generated by Django 4.1.4 on 2023-01-06 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_connection_following_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connection',
            name='posted_at',
        ),
    ]