# Generated by Django 4.2.2 on 2023-06-14 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_user_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Guestbook',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]
