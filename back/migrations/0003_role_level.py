# Generated by Django 4.2.7 on 2024-04-15 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0002_remove_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
