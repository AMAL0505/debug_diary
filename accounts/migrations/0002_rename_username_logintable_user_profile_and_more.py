# Generated by Django 4.2.18 on 2025-02-04 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logintable',
            old_name='username',
            new_name='user_profile',
        ),
        migrations.RemoveField(
            model_name='logintable',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='logintable',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
