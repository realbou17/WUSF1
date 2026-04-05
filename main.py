import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui import create_interface

if __name__ == "__main__":
    create_interface()