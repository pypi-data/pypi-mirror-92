import os
from pathlib import Path

BIN_DIR = os.getenv('BIN_DIR', '/usr/local/bin/')
M2_HOME = os.getenv('M2_HOME', f"{str(Path.home())}/.m2")
