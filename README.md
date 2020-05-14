# Drive_Services
This is the project made to use all kind of basic drive services like uploading, downloading, or searching of files or folders usng Google Drive APIs.

## Tools
basic tools in this pakage includes:
- Uploading file in Drive's root directory </li>
- Uploading file in particular folder by it's Drive folder ID </li>
- Uploading of folder by maintaing it's hierarchy </li>
- Creating Empty folder in root directory of Drive </li>
- Downloading files using ID to a particlar path </li>
- Searching of file by it's size and query </li>
- Getting list of files or folder by their size </li>
- Downloading any file or folder inly by it's name to your local path </li>


## Instruction

-> First enable the Drive API to use the API function in your acoount. <br>
-> Head over to <a href="https://developers.google.com/drive/api/v3/quickstart/python">Python Quickstart</a> and enable the
   Drive API by instructions given overthere.<br>
-> Download the `credentials.json` in your working directory.<br><br>

**Now start using the tools by running `main.py`.**<br><br>

For the first time you run the script it wil ask for permission of using Drive features. Just grant all the needed
permission.<br><br>

Doing this will create a `.credentials` folder in your working directory. This contains all the information associated with your current working acoount of which you have given the permission after running `main.py`.<br>
<br>

*If you want to change the current Google ID to another just delete this `.credentials` folder and `credentials.json` file. and paste the `credentials.json` file of another Google ID which you want.*<br>

> if working with linux systems then press `ctrl + H` this will unhide the hidden `.credentials` folder which is hidden by default as it contains "." before it's name.

### Using Script
You just need to run `main.py` file by using python-2. This will show all the further options.<br>

```
$ Python2.7 main.py
```
<br>

Here "google.png" image file is given for testing the script and it's working.


