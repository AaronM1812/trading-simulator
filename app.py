"""
Trading Strategy Simulator - Streamlit Cloud Entry Point
This file serves as the entry point for Streamlit Cloud deployment.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import and run the main application
from main import main

if __name__ == "__main__":
    main() 