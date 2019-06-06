import sys
import os

work_dir = os.path.dirname(os.path.abspath(sys.executable))
sys.path.insert(0, os.path.join(work_dir, "lib"))  # External modules
