# Generated by Django 3.2.1 on 2021-11-02 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20211102_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choose',
            old_name='user',
            new_name='user_id',
        ),
    ]
