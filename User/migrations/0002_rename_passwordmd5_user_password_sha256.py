# Generated by Django 4.0.2 on 2022-02-07 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='passwordMd5',
            new_name='password_SHA256',
        ),
    ]
