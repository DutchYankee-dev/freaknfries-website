#!/usr/bin/env python3
"""
Setup script for Freak 'n Fries website migration
Run this script to set up the project after creating the directory structure
"""

import os
import sys
import subprocess
import sqlite3

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def create_directory_structure():
    """Create the required directory structure"""
    directories = [
        'static/css',
        'static/js', 
        'static/images',
        'templates',
        'data',
        'build'
    ]
    
    print("📁 Creating directory structure...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  Created: {directory}/")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def initialize_database():
    """Initialize the SQLite database"""
    print("🗄️ Initializing database...")
    
    try:
        from app import init_db
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def create_env_file():
    """Create a .env file for environment variables"""
    env_content = """# Flask Environment Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True

# Secret key for Flask sessions (change this in production!)
SECRET_KEY=change-this-to-a-secure-random-key

# Database configuration
DATABASE_URL=sqlite:///data/site.db

# Site configuration
SITE_NAME=Freak-n-Fries Inc.
SITE_URL=https://www.freaknfries.com

# Contact information
CONTACT_EMAIL=info@freaknfries.com
CONTACT_PHONE=440 453 1877

# Social media
FACEBOOK_URL=www.facebook.com/freaknfries
"""
    
    env_file = '.env'
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_file}")
    else:
        print(f"⚠️ {env_file} already exists, skipping...")

def create_gitignore():
    """Create a .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Flask
instance/
.webassets-cache

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
data/site.db
*.log

# Don't ignore the build directory (needed for GitHub Pages)
# build/
"""
    
    gitignore_file = '.gitignore'
    if not os.path.exists(gitignore_file):
        with open(gitignore_file, 'w') as f:
            f.write(gitignore_content)
        print(f"✅ Created {gitignore_file}")
    else:
        print(f"⚠️ {gitignore_file} already exists, skipping...")

def test_flask_app():
    """Test if the Flask app can start"""
    print("🧪 Testing Flask application...")
    
    try:
        from app import app
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Flask app is working correctly")
                return True
            else:
                print(f"❌ Flask app returned status code: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Failed to test Flask app: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate your virtual environment:")
    print("   venv\\Scripts\\activate  (Windows)")
    print("   source venv/bin/activate  (macOS/Linux)")
    print("\n2. Start the development server:")
    print("   python app.py")
    print("\n3. Open your browser and visit:")
    print("   http://localhost:5000")
    print("\n4. Access the admin interface at:")
    print("   http://localhost:5000/admin")
    print("\n5. When ready to deploy, generate static files:")
    print("   python freeze.py")
    print("\n📚 Documentation:")
    print("   - Flask: https://flask.palletsprojects.com/")
    print("   - Frozen-Flask: https://frozen-flask.readthedocs.io/")
    print("   - GitHub Pages: https://pages.github.com/")

def main():
    """Main setup function"""
    print("🚀 Setting up Freak 'n Fries website migration project...")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Create directory structure
    if not create_directory_structure():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Create environment files
    create_env_file()
    create_gitignore()
    
    # Initialize database
    if not initialize_database():
        return 1
    
    # Test Flask app
    if not test_flask_app():
        return 1
    
    # Print next steps
    print_next_steps()
    
    return 0

if __name__ == '__main__':
    exit(main())