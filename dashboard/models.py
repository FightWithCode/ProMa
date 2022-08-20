from django.db import models
from django.contrib.auth.models import User

ACCESS_TYPES = (
    ('edit', 'edit'),
    ('view', 'view'),
)


class Profile(models.Model):
    last_logout = models.DateTimeField(auto_now_add=True)


class Server(models.Model):
    ip = models.CharField(max_length=24)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)

    def __str__(self):
        return self.ip


class Project(models.Model):
    name = models.CharField(max_length=255)
    full_path = models.TextField()
    server = models.ForeignKey(Server, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.server.ip)


class AssignedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.TextField()
    project = models.ForeignKey(Project, models.CASCADE)
    # provided_access_on = models.DateTimeField(auto_now=True)
    access_given_on = models.DateTimeField()
    # access_given_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_opened = models.DateTimeField(null=True, blank=True)
    last_saved = models.DateTimeField(null=True, blank=True)
    access_type = models.CharField(choices=ACCESS_TYPES, default='view', max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.file_path)


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
