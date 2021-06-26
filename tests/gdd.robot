*** Settings ***
Documentation       Google Drive File Dowload tests
...                 Usage:
...                 python -m robot.run -v CLIENT_SECRET:"C:/AUB/client_secret.json"
...                 -v FILE_ID:"xxxxxxxxHR0S2wxYWc" -v PATH:"C:/AUB/" gdd.robot
Library             gdo.gdo.GDO    ${CLIENT_SECRET}    WITH NAME    gdobject
Test Setup          Open Service
Test Teardown       Close Service

*** Variables ***
${CLIENT_SECRET}    ${NONE}  # Provide Client_secret.json file
${FILE_ID}          ${NONE}  # File ID of file to download
${PATH}             ${CURDIR}  # Path to save downloaded file; defaults to current working directory

*** Test Cases ***
Check whether Drive is Empty
  [Documentation]    Testcase to check if Google Drive contains no files
  ${resp} =    Is Drive Empty
  Should not be True    ${resp}    msg=No Files present in Google Drive

Check Whether File exists in Drive
  [Documentation]    Testcase to check if file exists in Google Drive
  ${resp} =    File Exists    ${FILE_ID}
  Should be True    ${resp[0]}    msg=Invalid File ID or no file with ID ${FILE_ID}

Download File And Verify
  [Documentation]    Testcase to download files (of different types) from Google Drive and verify (say filename and path)
  Download File    ${FILE_ID}    ${PATH}

Download same file twice and verify
  [Documentation]    Testcase to download file twice and verify they are replaced
  [Template]    Download File
  ${FILE_ID}    ${PATH}
  ${FILE_ID}    ${PATH}

*** Comments ***
Here are some test cases which are not yet covered

Parallel File Downloads
  pass
