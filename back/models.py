from django.db import models


# must set :
#   - fields_to_show
class Role(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=0)
    fields_to_show = ['id', 'name', 'level']


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=200)
    fields_to_show = ['first_name', 'last_name', 'email']


class Project(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=256)
    date_start = models.DateField()
    date_end = models.DateField()
    fields_to_show = ['title', 'description', 'date_start', 'date_end']


class ProjectMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class Task(models.Model):
    STATUS_CHOICES = [
        (0, 'in progress'),
        (1, 'complete'),
        (-1, 'late'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=256)
    date_end = models.DateField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField()
