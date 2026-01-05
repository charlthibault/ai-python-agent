import sys
from pathlib import Path

# Add the parent directory to the Python path to allow imports from the main package
sys.path.insert(0, str(Path(__file__).parent.parent))
