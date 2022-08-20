from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import paramiko
import pysftp
from stat import S_ISDIR, S_ISREG
from .models import AssignedFile, ConnectionHistory
from django.shortcuts import redirect
from django.contrib.auth.models import User
from channels.db import database_sync_to_async


# @database_sync_to_async
# def update_user_status(self, user, device_id, status):
#     return ConnectionHistory.objects.get_or_create(
#         user=user, device_id=device_id,
#     ).update(status=status)


ip='184.168.104.58'
port=22
username='s2b46pkx117j'
password='Xyz@1217'

# Old Index View for Developer
# @login_required
# def IndexView(request):
#     ssh_client=paramiko.SSHClient()
#     ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh_client.connect(hostname=ip, username=username, password=password)
#     print('Connection done!')
#     ftp_client=ssh_client.open_sftp()
#     ftp_client.chdir('AAIENADashboard')
#     project = 'AAIENADashboard'
#     project_folders = []
#     project_files = []
#     res = ftp_client.listdir_attr()
#     for i in res:
#         temp_dict = {}
#         temp_dict['name'] = i.filename
#         temp_dict['size'] = i.st_size
#         temp_dict['time'] = i.st_atime
#         mode = i.st_mode
        
#         if S_ISDIR(mode):
#             temp_dict['type'] = 'folder'
#             project_folders.append(temp_dict)
#         elif S_ISREG(mode):
#             temp_dict['type'] = 'file'
#             project_files.append(temp_dict)
#         else:
#             print("Unknown!")
#     context = {
#         "project_name": project,
#         "project_folders": project_folders,
#         "project_files": project_files
#     }
#     ftp_client.close()
#     ssh_client.close()
#     return render(request, 'index.html', context)

@login_required
def AdminIndexView(request):
    context = {}
    if request.user.is_superuser:
        dev_data = []
        for user in User.objects.filter(is_superuser=False):
            temp_dict = {}
            temp_dict['user'] = user
            temp_dict['assigned_files'] = AssignedFile.objects.filter(user=user)
            dev_data.append(temp_dict)
        context =  {
            'developers': dev_data
        }
        return render(request, 'admin-dashboard.html', context)
    else:
        return redirect('dashboard:index')


@login_required
def IndexView(request):
    context = {}
    if request.user.is_superuser:
        return redirect('dashboard:admin-dashboard')
    else:
        assigned_files = AssignedFile.objects.filter(user=request.user)
        # Code to read file content
        files = []
        for i in assigned_files:
            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=i.project.server.ip, username=i.project.server.username, password=i.project.server.password)
            print('Connection done!')
            ftp_client=ssh_client.open_sftp()
            temp_dict = {}
            try:
                temp_dict['file_name'] = i.file_path.split('/')[-1]
            except:
                temp_dict['file_name'] = i.file_path
            print('FTP Opened')
            file_obj = ftp_client.file(i.file_path, 'rt')
            attr_obj = ftp_client.lstat(i.file_path)
            temp_dict['size'] = attr_obj.st_size
            file_content = file_obj.read()
            temp_dict['content'] = file_content.decode('utf-8')
            ftp_client.close()
            ssh_client.close()
            files.append(temp_dict)
            print('Closed!')
        context['files'] = files
        print(files)
    return render(request, 'index.html', context)


def LoginView(request):
    if request.user.is_authenticated:
        redirect('/')
        
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:index')
        return render(request, 'login.html', {})
