# Generated by Django 4.2.7 on 2024-05-09 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0003_role_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
