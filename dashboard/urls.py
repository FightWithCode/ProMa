
from django.contrib import admin
from django.urls import path, include
from . import views
from . import apis

app_name = 'dashboard'

urlpatterns = [
    # Views
    path('', views.IndexView, name='index'),
    path('admin-dashboard', views.AdminIndexView, name='admin-dashboard'),
    path('login', views.LoginView, name='login'),

    # APIs
    path('folder-data/<str:root_folder>/<str:request_folder>', apis.GetFolderData.as_view(), name='folder-data'),
    path('save-file', apis.SaveFileView.as_view(), name='savee-file'),
]
