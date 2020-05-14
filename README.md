# Drive_Services
This is the project made to use all kind of basic drive services like uploading, downloading, or searching of files or folders usng Google Drive APIs.

## Tools
basic tools in this pakage includes:
<ul style="list-style-type:disc;">
  <li> Uploading file in Drive's root directory </li>
  <li> Uploading file in particular folder by it's Drive folder ID </li>
  <li> Uploading of folder by maintaing it's hierarchy </li>
  <li> Creating Empty folder in root directory of Drive </li>
  <li> Downloading files using ID to a particlar path </li>
  <li> Searching of file by it's size and query </li>
  <li> Getting list of files or folder by their size </li>
  <li> Downloading any file or folder inly by it's name to your local path </li>
</ul>

## Instruction

-> First enable the Drive API to use the API function in your acoount. <br>
-> Head over to <a href="https://developers.google.com/drive/api/v3/quickstart/python">Python Quickstart</a> and enable the
   Drive API by instructions given overthere.<br>
-> Download the `credentials.json` in your working directory.<br><br>

<b>Now start using the tools by running `main.py`.</b><br><br>

For the first time you run the script it wil ask for permission of using Drive features. Just grant all the needed
permission.<br><br>

Doing this will create a `.credentials` folder in your working directory. This contains all the information associated with your current working acoount of which you have given the permission after running `main.py`.<br>
<br><i>

If you want to change the current Google ID to another just delete this `.credentials` folder and `credentials.json` file. and paste the `credentials.json` file of another Google ID which you want.
</i><br>

<ul style="list-style-type:disc;">
  <li> if using linux then press `ctrl + H` this will unhide the hidden `.credentials` folder which is hidden by default as 
       it contains .before it's name</li> 
</ul>


