# Generated by Django 5.0.1 on 2024-01-04 19:41

import api.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_user_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', api.models.UserManager()),
            ],
        ),
    ]
