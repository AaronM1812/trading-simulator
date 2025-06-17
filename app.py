"""
Trading Strategy Simulator - Streamlit Cloud Entry Point
Redirects to the main application in the app directory.
"""

import streamlit as st
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import the main function from app/main.py
from main import main

# Run the main application
main() 