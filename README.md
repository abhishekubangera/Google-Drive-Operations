# Google Drive Operations (GDO)
The supported operations for now is:
  * Downloading files from Google Drive

Prerequisites
  * Python 3.6 and above.
  * Google account with Google Drive enabled 
  * A Google Cloud Platform project with the API enabled. For creation refer: https://developers.google.com/workspace/guides/create-project
      - Here you need to enable "Drive API"
      - Add Scope ".../auth/drive"
  *  Create credentials for a desktop application, refer: https://developers.google.com/workspace/guides/create-credentials 
  

Installation Instructions
  * Install by running,
  
     ```pip install git+https://github.com/abhishekubangera/Google-Drive-Operations.git```


Execution Instructions
  
  * Commmand line execution
    
    > gdd -i "\<FILE ID\>" -c "\<CLIENT SECRET JSON FILE PATH\>" -f "\<DOWNLOAD PATH\>"

    * Terms:
      - FILE ID: Google Drive File ID
        * To get the File ID, go to Google Drive, right click on the file and get the link.
          > https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing&resourcekey=1234567890  
	  - CLIENT SECRET JSON FILE PATH: OAuth JSON file path
      - DOWNLOAD PATH: Folder path to save downloaded files; defaults to current working directory.
    
	*Example:
        
		> gdd -i "xxxxxxxxHR0S2wxYWc" -c "C:\AUB\client_secret.json" -f "C:\AUB\"
