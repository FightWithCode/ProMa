from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import paramiko
import pysftp
from stat import S_ISDIR, S_ISREG


ip='184.168.104.58'
port=22
username='s2b46pkx117j'
password='Xyz@1217'


class GetFolderData(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, root_folder, request_folder):
        response = {}
        try:
            ssh_client=paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip, username=username, password=password)
            print('Connection done!')
            ftp_client=ssh_client.open_sftp()
            ftp_client.chdir(root_folder)
            ftp_client.chdir(request_folder)
            res = ftp_client.listdir_attr()
            project_folders = []
            project_files = []
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
            ftp_client.close()
            ssh_client.close()
            response = {
                "project_name": root_folder,
                "project_folders": project_folders,
                "project_files": project_files
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response['msg'] = 'error'
            response['error'] = str(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
