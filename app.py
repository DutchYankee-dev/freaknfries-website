#!/usr/bin/env python3
"""
Freak-n-Fries Flask Application - Fixed settings access
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'freaknfries_secret_key_2025'

# ========================================
# PRODUCTION CONFIGURATION
# ========================================

# Production vs Development configuration
if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    # Production settings for PythonAnywhere
    app.config['DEBUG'] = False
    DATABASE = '/home/yourusername/freaknfries/data/site.db'  # Update 'yourusername' with your PythonAnywhere username
else:
    # Development settings (your current setup)
    app.config['DEBUG'] = True
    DATABASE = os.path.join('data', 'site.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_site_settings():
    """Get site settings - fixed to handle different database structures"""
    conn = get_db_connection()
    
    try:
        # Method 1: Try the settings table with id=1 (your current structure)
        try:
            settings_row = conn.execute('SELECT * FROM settings WHERE id = 1').fetchone()
            if settings_row:
                # Convert Row object to dictionary and return individual values
                site_settings = {
                    'company_name': settings_row['company_name'] if 'company_name' in settings_row.keys() else 'Freak-n-Fries',
                    'tagline': settings_row['tagline'] if 'tagline' in settings_row.keys() else 'Home of the Dutch frikandel in the US',
                    'phone': settings_row['phone'] if 'phone' in settings_row.keys() else '440 453 1877',
                    'email': settings_row['email'] if 'email' in settings_row.keys() else 'info@freaknfries.com',
                    'product_name': settings_row['product_name'] if 'product_name' in settings_row.keys() else 'Dutch Dawg®'
                }
                conn.close()
                return site_settings
        except sqlite3.Error as e1:
            print(f"Method 1 failed: {e1}")
        
        # Method 2: Try key-value pairs in settings table
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM settings")
            settings_rows = cursor.fetchall()
            if settings_rows:
                site_settings = {}
                for row in settings_rows:
                    site_settings[row['key']] = row['value']
                
                # Ensure all required keys exist
                defaults = {
                    'company_name': 'Freak-n-Fries',
                    'tagline': 'Home of the Dutch frikandel in the US',
                    'phone': '440 453 1877',
                    'email': 'info@freaknfries.com',
                    'product_name': 'Dutch Dawg®'
                }
                
                for key, default_value in defaults.items():
                    if key not in site_settings:
                        site_settings[key] = default_value
                
                conn.close()
                return site_settings
        except sqlite3.Error as e2:
            print(f"Method 2 failed: {e2}")
        
        # Method 3: Fallback to default values
        print("Using fallback default values")
        site_settings = {
            'company_name': 'Freak-n-Fries',
            'tagline': 'Home of the Dutch frikandel in the US',
            'phone': '440 453 1877',
            'email': 'info@freaknfries.com',
            'product_name': 'Dutch Dawg®'
        }
        
    except Exception as e:
        print(f"Database error in get_site_settings: {e}")
        # Return default values if all else fails
        site_settings = {
            'company_name': 'Freak-n-Fries',
            'tagline': 'Home of the Dutch frikandel in the US',
            'phone': '440 453 1877',
            'email': 'info@freaknfries.com',
            'product_name': 'Dutch Dawg®'
        }
    finally:
        if conn:
            conn.close()
    
    return site_settings

def get_page(slug):
    """Get page data from pages table"""
    conn = get_db_connection()
    try:
        page = conn.execute('SELECT * FROM pages WHERE slug = ?', (slug,)).fetchone()
        return page
    except sqlite3.Error as e:
        print(f"Error getting page {slug}: {e}")
        return None
    finally:
        conn.close()

def get_page_content(page_name):
    """Get page content from page_content table"""
    conn = get_db_connection()
    try:
        content = conn.execute('SELECT * FROM page_content WHERE page_name = ?', (page_name,)).fetchone()
        return content
    except sqlite3.Error as e:
        print(f"Error getting page content {page_name}: {e}")
        return None
    finally:
        conn.close()

def get_retailers_by_category(category):
    """Get retailers by category"""
    conn = get_db_connection()
    try:
        retailers = conn.execute('SELECT * FROM retailers WHERE category = ? ORDER BY name', (category,)).fetchall()
        return retailers
    except sqlite3.Error as e:
        print(f"Error getting retailers for category {category}: {e}")
        return []
    finally:
        conn.close()

def get_all_retailers():
    """Get all retailers"""
    conn = get_db_connection()
    try:
        retailers = conn.execute('SELECT * FROM retailers ORDER BY category, name').fetchall()
        return retailers
    except sqlite3.Error as e:
        print(f"Error getting all retailers: {e}")
        return []
    finally:
        conn.close()

def get_testimonials():
    """Get active testimonials"""
    conn = get_db_connection()
    try:
        testimonials = conn.execute('SELECT * FROM testimonials WHERE active = 1').fetchall()
        return testimonials
    except sqlite3.Error as e:
        print(f"Error getting testimonials: {e}")
        return []
    finally:
        conn.close()

@app.template_filter('strftime')
def strftime_filter(date, fmt='%Y-%m-%d'):
    if date:
        return date.strftime(fmt)
    return ''

@app.context_processor
def inject_global_vars():
    """Make site_settings and settings available to all templates"""
    site_settings = get_site_settings()
    return {
        'site_settings': site_settings,
        'settings': site_settings  # For base.html which uses 'settings'
    }

@app.route('/')
def index():
    """Home page"""
    try:
        site_settings = get_site_settings()
        home_content = get_page_content('home')
        testimonials = get_testimonials()
        testimonial = testimonials[0] if testimonials else None
        
        return render_template('index.html',
                             site_settings=site_settings,
                             settings=site_settings,
                             home_content=home_content,
                             testimonial=testimonial)
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"Error loading home page: {e}", 500

@app.route('/about')
def about():
    """About page"""
    try:
        site_settings = get_site_settings()
        page = get_page('about')
        about_content = get_page_content('about')
        
        print(f"About route - site_settings type: {type(site_settings)}")
        print(f"About route - site_settings: {site_settings}")
        
        return render_template('about.html',
                             site_settings=site_settings,
                             settings=site_settings,
                             page=page,
                             about_content=about_content)
    except Exception as e:
        print(f"Error in about route: {e}")
        return f"Error loading about page: {e}", 500

@app.route('/where-to-buy')
def where_to_buy():
    """Where to Buy page"""
    try:
        site_settings = get_site_settings()
        page = get_page('where-to-buy')
        where_content = get_page_content('where-to-buy')
        
        # Get retailers by category
        online_retailers = get_retailers_by_category('online')
        restaurants = get_retailers_by_category('restaurant')
        
        print(f"Where-to-buy route - site_settings type: {type(site_settings)}")
        print(f"Where-to-buy route - site_settings: {site_settings}")
        
        return render_template('where-to-buy.html',
                             site_settings=site_settings,
                             settings=site_settings,
                             page=page,
                             where_content=where_content,
                             online_retailers=online_retailers,
                             restaurants=restaurants,
                             retailer=online_retailers,  # For template loops
                             restaurant=restaurants)     # For template loops
    except Exception as e:
        print(f"Error in where_to_buy route: {e}")
        return f"Error loading where to buy page: {e}", 500

@app.route('/admin')
def admin():
    """Admin page"""
    try:
        site_settings = get_site_settings()
        retailers = get_all_retailers()
        testimonials = get_testimonials()
        
        # Get pages for admin interface
        conn = get_db_connection()
        try:
            pages = conn.execute('SELECT * FROM pages ORDER BY slug').fetchall()
        except sqlite3.Error as e:
            print(f"Error getting pages: {e}")
            pages = []
        finally:
            conn.close()
        
        return render_template('admin.html',
                             site_settings=site_settings,
                             settings=site_settings,
                             retailers=retailers,
                             testimonials=testimonials,
                             pages=pages)
    except Exception as e:
        print(f"Error in admin route: {e}")
        return f"Error loading admin page: {e}", 500

@app.errorhandler(404)
def not_found(error):
    site_settings = get_site_settings()
    return f"Page not found - {site_settings['company_name']}", 404

@app.errorhandler(500)
def internal_error(error):
    site_settings = get_site_settings()
    return f"Internal server error - {site_settings['company_name']}", 500

def get_local_ip():
    """Get the local IP address for network access"""
    import socket
    try:
        # Connect to a remote server to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "localhost"

if __name__ == '__main__':
    # Only run the development server when running directly
    # PythonAnywhere will use WSGI instead
    local_ip = get_local_ip()
    
    print("🚀 Starting Freak-n-Fries development server...")
    print(f"🏠 Local access: http://127.0.0.1:5000")
    print(f"🌐 Network access: http://{local_ip}:5000")
    print(f"⚙️  Admin (local): http://127.0.0.1:5000/admin")
    print(f"⚙️  Admin (network): http://{local_ip}:5000/admin")
    print("📱 Test on mobile devices using the network address!")
    print("🛑 Press Ctrl+C to stop")
    print(f"🗄️  Database: {DATABASE}")
    print(f"🐛 Debug mode: {app.config['DEBUG']}")
    
    # host='0.0.0.0' allows access from any device on the network
    app.run(debug=True, host='0.0.0.0', port=5000)