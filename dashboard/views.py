from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import paramiko
import pysftp
from stat import S_ISDIR, S_ISREG


ip='184.168.104.58'
port=22
username='s2b46pkx117j'
password='Xyz@1217'


@login_required
def IndexView(request):
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username, password=password)
    print('Connection done!')
    ftp_client=ssh_client.open_sftp()
    ftp_client.chdir('AAIENADashboard')
    project = 'AAIENADashboard'
    project_folders = []
    project_files = []
    res = ftp_client.listdir_attr()
    for i in res:
        temp_dict = {}
        temp_dict['name'] = i.filename
        temp_dict['size'] = i.st_size
        temp_dict['time'] = i.st_atime
        mode = i.st_mode
        
        if S_ISDIR(mode):
            temp_dict['type'] = 'folder'
            project_folders.append(temp_dict)
        elif S_ISREG(mode):
            temp_dict['type'] = 'file'
            project_files.append(temp_dict)
        else:
            print("Unknown!")
    context = {
        "project_name": project,
        "project_folders": project_folders,
        "project_files": project_files
    }
    ftp_client.close()
    ssh_client.close()
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
