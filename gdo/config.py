"""
Configuration file.  All constants should go here.
"""
from .version import __version__, __build__, __date__, __commit__


class Config:
    """
    This class contains the application configuration values
    """
    version = __version__
    build = __build__
    date = __date__
    commit = __commit__
