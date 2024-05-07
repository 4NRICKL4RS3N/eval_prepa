# Generated by Django 4.2.7 on 2024-03-27 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=256)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=150)),
                ('password', models.CharField(max_length=200)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.role')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=256)),
                ('date_end', models.DateField()),
                ('status', models.IntegerField(choices=[(0, 'in progress'), (1, 'complete'), (-1, 'late')], default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.project')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back.user')),
            ],
        ),
    ]