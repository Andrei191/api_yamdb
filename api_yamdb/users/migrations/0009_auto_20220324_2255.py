# Generated by Django 2.2.16 on 2022-03-24 19:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220324_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='incorrect username', regex='^[\\w.@+-]+$')]),
        ),
    ]
