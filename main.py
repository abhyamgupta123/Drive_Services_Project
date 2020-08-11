
from __future__ import print_function
import httplib2
import os, io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

import downloader as d
import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

file_size_counter = 0.0


def get_directory_size(Folder_path):
    total_size = 0
    for path, dirs, files in os.walk(Folder_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size


def listFiles(size):

    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def uploadFile(filename,filepath,mimetype):

    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID of {}: %s'.format(filename) % file.get('id'))
    print("")

def downloadFile(file_id,filepath):

    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def createFolder(name):

    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID of {}: %s'.format(name) % file.get('id'))
    print("")
    return file.get('id')

def upload_file_in_folder(drive_folder_id, local_file_name, local_file_path, percent_show):
    # drive_folder_id = folderid
    file_metadata = {
        'name': local_file_name,
        'parents': [drive_folder_id]
    }
    media = MediaFileUpload(local_file_path,
                            mimetype='application/octet-stream',
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print ('File ID of {}: {}  ({}% Completed...) '.format(local_file_name, file.get('id'), int(percent_show)))
    print("")

def creating_folder_in_parent_folder(local_folder_name,parent_folder_id):

    file_metadata = {
    'name' : local_folder_name,
    'parents' : [parent_folder_id],
    'mimeType' : 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID of {}: %s'.format(local_folder_name) % file.get('id'))
    print("")
    return file.get('id')

def upload_all_files_of_given_folder(local_folder_path, local_folder_name, drive_folder_id, folder_size_calculated):

    global file_size_counter

    for root, dirs, files in os.walk(local_folder_path):
        for single_file_name in files:
            current_size = os.path.getsize(os.path.join(root, single_file_name))
            file_size_counter = file_size_counter + current_size
            percent = (float(file_size_counter)/folder_size_calculated)*100
            upload_file_in_folder(drive_folder_id, single_file_name, os.path.join(root, single_file_name), percent)
        break

def recursive_upload(local_folder_path, local_folder_name, drive_folder_id, folder_size):

    upload_all_files_of_given_folder(local_folder_path, local_folder_name, drive_folder_id, folder_size)

    id_list={}
    for root, dirs, files in os.walk(local_folder_path):
        for single_dir_name in dirs:
            temp_id = creating_folder_in_parent_folder(single_dir_name, drive_folder_id)
            id_list[single_dir_name] = temp_id
        break

    for key, value in id_list.items():
        new_path = os.path.join(local_folder_path,key)
        recursive_upload(new_path, key, value, folder_size)

def whole_folder_upload(local_folder_path, local_folder_name):

    local_folder_whole_size = get_directory_size(local_folder_path)
    print("Total Folder size is {} Bytes.".format(local_folder_whole_size))
    print("")
    root_id = createFolder(local_folder_name)
    recursive_upload(local_folder_path, local_folder_name, root_id, local_folder_whole_size)

def searchFile(size,query):

    results = drive_service.files().list(
    pageSize=size,fields = "nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))




while True:
    print("")
    print("Choose a number to perform your action.")
    print("")
    print(" 1. To Upload a Single File.")
    print(" 2. To download a file using it's ID to a desired local location path.")
    print(" 3. To create a Empty Folder in Root Directory of Drive.")
    print(" 4. To upload a file in a given Folder by it's Drive Folder ID.")
    print(" 5. To Upload a whole folder by using it's complete path.")
    print(" 6. To Search a File by its size and Query.")
    print(" 7. To list all the files based on Size.")
    print(" 8. To download folder or file by it's name.")
    print("")
    print("PRESS 'q' TO QUIT")
    print("")
    num = raw_input("Enter Option Number:  ")

    if (num == "q"):
        break

    elif (int(num) == 1):
        f_name = raw_input("Enter name of file with it's format (like .pdf, .txt, .jpg etc.): ")
        f_path = raw_input("Enter the complete path of File: ")
        Mime = raw_input("Enter MIME Type of file if you know otherwise just press enter: ")
        if (Mime == ""):
            Mime ='application/octet-stream'
        print("")
        uploadFile(f_name, f_path,Mime)
        print("")
        print("UPLOADING DONE..!!")
        print("")

    elif (int(num) == 2):
        f_id = raw_input("Enter file ID of File present in Google drive: ")
        f_path = raw_input("Enter the local download path: ")
        downloadFile(f_id, f_path)
        print("")
        print("DOWNLOADING DONE..!!")
        print("")

    elif (int(num) == 3):
        f_name = raw_input("Enter the name of folder: ")
        print('')
        createFolder(f_name)
        print("Folder is Successfully Created.")
        print("")

    elif (int(num) == 4):
        d_f_id = raw_input("Enter ID of Google Drive Folder: ")
        l_f_path = raw_input("Enter path of that local file: ")
        l1=l_f_path.split('/')
        print("")
        if (os.path.isfile(l_f_path)):
            l_f_name = l1[-1]
            upload_file_in_folder(d_f_id, l_f_name, l_f_path, '100')
            print("")
            print("File created Successfully")
            print("")
        else:
            print("Enter the correct file path or Folder ID...")

    elif (int(num) == 5):
        local_f_path = raw_input("Enter path of your local folder: ")
        local_f_name = raw_input("Enter name for your folder to be created in Drive: ")
        print("")
        if (os.path.isdir(local_f_path)):
            whole_folder_upload(local_f_path, local_f_name)
            print("")
            print("UPLOADING DONE...!!")
            file_size_counter = 0
            print("")
        else:
            print("Enter the correcr folder name that is present at your given path.")

    elif (int(num) == 6):
        s=raw_input("Enter Size of file: ")
        q=raw_input("Enter Query for file: ")
        print("")
        searchFile(s, q)
        print("")

    elif (int(num) == 7):
        s=raw_input("Enter the Size of file: ")
        print("")
        listFiles(s)
        print("")

    elif (int(num)==8):
        inp1=raw_input("enter the folder name : ")
        inp2=raw_input("enter the location of path : ")
        print("")
        d.dwnld(inp1, inp2)
        print("")
        print('DOWNLOAD DONE...!!')

    else:
        print("")
        print("You entered a wrong option no. Please Enter the correct Task no. to procced further.")
        print("")


# uploadFile('google','google.jpg','application/octet-stream')
#downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg')
# folder_id=createFolder('new1')
# upload_file_in_folder(folder_id,"friends.jpg",'./upl/friends.jpg')
# creating_folder_in_parent_folder("folder_in_folder",folder_id)
# upload_all_files_of_given_folder("./upl","upl",folder_id)
# whole_folder_upload("/home/abhyam/Desktop/drive_API/google-drive-api-tutorial/google-drive-api-tutorial-project/upl","upl")
#searchFile(10,"name contains 'Getting'")
