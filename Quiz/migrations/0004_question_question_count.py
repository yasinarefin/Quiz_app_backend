# Generated by Django 4.0.2 on 2022-02-24 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0003_remove_question_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
