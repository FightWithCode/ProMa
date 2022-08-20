from django.contrib import admin
from .models import Server, Project, AssignedFile, Log


admin.site.register(Server)
admin.site.register(Project)
admin.site.register(AssignedFile)
admin.site.register(Log)
