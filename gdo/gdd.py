from __future__ import print_function
import os
import sys
import argparse
import logging
from .config import Config
from .gdo import GDO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Google Drive File Downloader")


def create_parser():
    """
    Parse the command line arguments
    :return: an argparse object
    """
    parser = argparse.ArgumentParser(description='Download files from Google Drive',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-i',
                        '--file_id',
                        type=str,
                        required=True,
                        help='File ID of files to be downloaded')
    parser.add_argument('-c',
                        '--creds',
                        type=str,
                        required=True,
                        help='OAuth JSON file path; ex: /path/client_secret.json')
    parser.add_argument('-f',
                        '--folder',
                        type=str,
                        default=os.getcwd(),
                        help='Folder path to save downloaded files; defaults to current working directory')

    return parser


def log_version_info():
    """
    Log the GDD version info
    """
    print('\n')
    logger.info("GDD %s.%s %s (%s)", Config.version, Config.build,
                Config.date, Config.commit)
    logger.info("Python version: %s\n", sys.version)


def main():
    """
    the main entry point
    :return: None
    """
    parser = create_parser()
    args = parser.parse_args()

    # write the GDD version info to console
    log_version_info()

    gdd_object = GDO(args.creds)
    gdd_object.open_service()
    assert not gdd_object.is_drive_empty(), "No files present in Google Drive"
    gdd_object.download_file(args.file_id, args.folder)
