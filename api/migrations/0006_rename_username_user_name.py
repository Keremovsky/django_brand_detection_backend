# Generated by Django 5.0.1 on 2024-01-04 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_user_name_alter_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='name',
        ),
    ]
