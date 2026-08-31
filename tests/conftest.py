import os
import tempfile
from pathlib import Path

TEST_HOME = Path(tempfile.mkdtemp(prefix="gca-tests-"))
os.environ["GCA_HOME"] = str(TEST_HOME)
