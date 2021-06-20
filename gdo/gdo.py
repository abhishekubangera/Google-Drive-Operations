"""
This module contain methods related to Google Drive operations (GDO).
"""
from __future__ import print_function
import os
import io
import logging
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests_oauthlib
from googleapiclient.http import MediaIoBaseDownload

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
logger = logging.getLogger("Google Drive operations")


class GDO(object):
    """
    Google Drive operations (GDO)
    This class contains methods related to Google Drive operations.
    """
    def __init__(self, client_secret):
        """
        :param str client_secret: File name with path to OAuth details
        """
        self.creds = None
        self.service = None
        self.scopes = ["https://www.googleapis.com/auth/drive"]
        self.client_secret = client_secret
        self.service_name = "drive"
        self.version = "v3"
        self.get_client_credential()

    def __del__(self):
        """
        Make sure the session objects are deleted.
        """
        if self.creds or self.service:
            self.close_service()

    def get_client_credential(self):
        """
        Get Client Access details.
        If you are executing for first time, make sure you follow the steps displayed on console
        to authorize.
        :raises AssertionError if,
        1. Client Secret file not found.
        2. Client Secret file format is not JSON.
        3. Error occurs during Authorization or Refreshing Token.
        """
        _flag1 = True
        if not os.path.exists(self.client_secret):
            raise AssertionError("Client Secret file not found")
        if not self.client_secret.endswith(".json"):
            raise AssertionError("Invalid Client Secret file format. Should be a JSON file")
        try:
            self.creds = Credentials.from_authorized_user_file(self.client_secret, self.scopes)
        except Exception as e:
            _flag1 = False
            _error1 = e

        try:
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.client_secret, self.scopes)
                    self.creds = flow.run_local_server(port=0)

                with open(self.client_secret, 'w') as secret:
                    secret.write(self.creds.to_json())
        except Exception as e:
            e = str(e) + str(_error1) if not _flag1 else str(e)
            raise AssertionError(e)

    def open_service(self):
        """
        Creates service for communicating with API.
        :raises Exception on Failure
        """
        try:
            self.service = build(self.service_name, self.version, credentials=self.creds)
        except Exception as e:
            raise AssertionError(e)

    def close_service(self):
        """
        Closes if services are open.
        """
        self.creds = None
        self.service = None

    def is_drive_empty(self):
        """
        Checks if Drive is empty.
        :return: bool: True if empty, else False
        """
        files = self.service.files().list().execute().get('files', [])
        return True if not files else False

    def file_exists(self, file_id):
        """
        Checks if requested file ID is present in Drive.
        :param str: file ID
        :return: tuple: (True, response) if file exists, else (False, None)
        """
        try:
            response = self.service.files().get(fileId=file_id).execute()
        except Exception as e:
            logger.error(e)
            response = None
        return (True, response) if response else (False, response)

    def _create_local_folder_path_if_not_present(self, folder):
        """
        Checks if folder path exists, else creates folder path.
        If exception occurs during creation, current working directory will be considered.
        :param str: folder
        :return: str: folder path
        """
        if not os.path.isdir(folder):
            logger.warning('Folder path to save downloaded files not found %s' % folder)
            try:
                logger.info('Creating %s' % folder)
                os.makedirs(folder)
                logger.info('Folder path to save downloaded files set to %s' % folder)
            except OSError as ex:
                logger.error(ex)
                folder = str(os.getcwd())
                logger.warning('Folder path to save downloaded files set to %s' % os.getcwd())
        else:
            logger.info('Folder path to save downloaded files set to %s' % folder)
        return folder

    def download_file(self, file_id, folder):
        """
        Downloads file from Google Drive and saves to local path.
        :param str: file_id; id of file to download
        :param str: folder; path to save downloaded files
        :raises AssertionError if,
        1. File not found in Drive.
        2. Error occurs during downloading.
        3. Downloaded file not found in path.
        """
        folder = self._create_local_folder_path_if_not_present(folder)

        status, response = self.file_exists(file_id)
        if not status:
            raise AssertionError("File with ID %s not found" % file_id)

        logger.info("Downloading file: %s" % response["name"])
        resp = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        try:
            downloader = MediaIoBaseDownload(fh, resp)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download progress: %d%%." % int(status.progress() * 100))

            _file_name = response["name"]
            logger.info("Saving file as %s" % _file_name)

            with open(os.path.join(folder, _file_name), 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
        except Exception as e:
            raise AssertionError(e)

        if not os.path.exists(os.path.join(folder, _file_name)):
            raise AssertionError("File: %s not found in Path: %s" % (_file_name, folder))
        logger.info("File downloaded successfully. Path: %s" % os.path.join(folder, _file_name))
