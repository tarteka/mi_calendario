import os
from dotenv import load_dotenv

"""Versionamiento de la aplicación."""
load_dotenv()
__version__ = os.environ.get("VERSION", "0.0.0")


