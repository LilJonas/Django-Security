# Generated by Django 4.2.2 on 2023-06-14 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]