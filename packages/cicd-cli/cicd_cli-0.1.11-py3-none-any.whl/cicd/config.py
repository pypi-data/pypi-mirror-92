import os
from pathlib import Path

BIN_DIR = os.getenv('BIN_DIR', '/usr/local/bin/')
MAVEN_HOME = os.getenv('MAVEN_HOME', f"{str(Path.home())}/.m2")
MAVEN_SETTINGS = os.getenv('MAVEN_SETTINGS', None)
