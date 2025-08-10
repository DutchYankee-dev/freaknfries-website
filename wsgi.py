#!/usr/bin/python3

"""
WSGI configuration for Freak-n-Fries Flask application on PythonAnywhere

This file contains the WSGI configuration required to serve your Flask app
on PythonAnywhere. It sets up the proper Python path and environment variables.

Instructions:
1. Replace 'yourusername' with your actual PythonAnywhere username
2. Upload this file to your project root directory
3. Configure PythonAnywhere to use this file as your WSGI configuration
"""

import sys
import os

# Add your project directory to the Python path
# Replace 'yourusername' with your actual PythonAnywhere username
username = 'DutchYankee'  # CHANGE THIS!
project_path = f'/home/DutchYankee/freaknfries'

if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Set environment variable to indicate we're running on PythonAnywhere
os.environ['PYTHONANYWHERE_DOMAIN'] = f'{username}.pythonanywhere.com'

# Import your Flask application
from app import app as application

# Optional: Add some debugging info (remove in production if desired)
if __name__ == "__main__":
    print(f"WSGI starting for user: {username}")
    print(f"Project path: {project_path}")
    print(f"Python path: {sys.path}")
    application.run()