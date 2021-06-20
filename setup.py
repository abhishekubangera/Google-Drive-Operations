"""
Google Drive Operations setup file.
"""

from setuptools import setup, find_packages
from gdo.version import __version__, __build__

setup(
    name='Google Drive Operations',
    version="{0}.{1}".format(__version__, __build__),
    description='Minimal class for Google Drive Operations',
    author='Abhishek U Bangera',
    author_email='ubangera.abhishek89@gmail.com',
    url='https://github.com/abhishekubangera/Google-Drive-Operations',
    entry_points={
        "console_scripts": ["gdd = gdo.gdd:main"],
    },
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
    ],
    packages=find_packages()
)
