from django.contrib import admin
from .models import Server, Project, AssignedFile, Log, ConnectionHistory, Profile, LoggedInUsers


admin.site.register(Server)
admin.site.register(Project)
admin.site.register(AssignedFile)
admin.site.register(Log)
admin.site.register(Profile)
admin.site.register(ConnectionHistory)
admin.site.register(LoggedInUsers)
