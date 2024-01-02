# Generated by Django 5.0.1 on 2024-01-02 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackmodel',
            name='image',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='registrationType',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='historymodel',
            name='image',
            field=models.ImageField(upload_to='history/'),
        ),
        migrations.AlterField(
            model_name='requestmodel',
            name='image',
            field=models.ImageField(upload_to='request/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
