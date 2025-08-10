#!/usr/bin/env python3
"""
Static site generator for Freak 'n Fries website
Converts Flask app to static HTML files for GitHub Pages deployment
"""

import os
import shutil
from urllib.parse import urljoin
from flask_frozen import Freezer
from app import app

# Configure Freezer
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DESTINATION_IGNORE'] = ['.git*', 'CNAME', '.nojekyll']

freezer = Freezer(app)

@freezer.register_generator
def static_files():
    """Generate URLs for static files"""
    for filename in os.listdir(os.path.join(app.static_folder, 'css')):
        yield 'static', {'filename': f'css/{filename}'}
    
    for filename in os.listdir(os.path.join(app.static_folder, 'js')):
        yield 'static', {'filename': f'js/{filename}'}
    
    # Add image files if they exist
    images_dir = os.path.join(app.static_folder, 'images')
    if os.path.exists(images_dir):
        for filename in os.listdir(images_dir):
            yield 'static', {'filename': f'images/{filename}'}

@freezer.register_generator
def all_pages():
    """Generate URLs for all pages"""
    # Main pages
    yield 'home'
    yield 'about'
    yield 'where_to_buy'

def prepare_build_directory():
    """Prepare the build directory for deployment"""
    build_dir = app.config['FREEZER_DESTINATION']
    
    # Create .nojekyll file for GitHub Pages
    nojekyll_path = os.path.join(build_dir, '.nojekyll')
    with open(nojekyll_path, 'w') as f:
        f.write('')
    
    # Create CNAME file if custom domain is used
    # Uncomment and modify if you have a custom domain
    # cname_path = os.path.join(build_dir, 'CNAME')
    # with open(cname_path, 'w') as f:
    #     f.write('www.freaknfries.com')
    
    # Create robots.txt
    robots_path = os.path.join(build_dir, 'robots.txt')
    with open(robots_path, 'w') as f:
        f.write("""User-agent: *
Allow: /

Sitemap: https://www.freaknfries.com/sitemap.xml
""")
    
    # Create sitemap.xml
    sitemap_path = os.path.join(build_dir, 'sitemap.xml')
    with open(sitemap_path, 'w') as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://www.freaknfries.com/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://www.freaknfries.com/about</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://www.freaknfries.com/where-to-buy</loc>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
</urlset>
""")

def optimize_static_files():
    """Optimize static files for production"""
    build_dir = app.config['FREEZER_DESTINATION']
    
    print("Optimizing static files...")
    
    # Here you could add:
    # - CSS minification
    # - JavaScript minification
    # - Image optimization
    # - GZIP compression
    
    print("Static file optimization complete.")

def validate_build():
    """Validate the generated static site"""
    build_dir = app.config['FREEZER_DESTINATION']
    
    required_files = [
        'index.html',
        'about/index.html', 
        'where-to-buy/index.html',
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(build_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files in build:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("✅ All required files generated successfully!")
        return True

def clean_build_directory():
    """Clean the build directory before generating"""
    build_dir = app.config['FREEZER_DESTINATION']
    
    if os.path.exists(build_dir):
        print(f"Cleaning existing build directory: {build_dir}")
        shutil.rmtree(build_dir)
    
    os.makedirs(build_dir, exist_ok=True)

def generate_deployment_info():
    """Generate deployment information file"""
    build_dir = app.config['FREEZER_DESTINATION']
    
    deployment_info = {
        'generated_at': __import__('datetime').datetime.now().isoformat(),
        'python_version': __import__('sys').version,
        'flask_version': __import__('flask').__version__,
        'pages_generated': ['/', '/about', '/where-to-buy'],
        'deployment_target': 'GitHub Pages',
        'instructions': [
            '1. Commit all files in the build/ directory to your repository',
            '2. Push to the main branch',
            '3. Enable GitHub Pages in repository settings',
            '4. Set source to "Deploy from a branch" and select "main" branch',
            '5. Your site will be available at https://yourusername.github.io/repository-name/'
        ]
    }
    
    info_path = os.path.join(build_dir, 'deployment-info.json')
    with open(info_path, 'w') as f:
        __import__('json').dump(deployment_info, f, indent=2)

def main():
    """Main function to generate static site"""
    print("🚀 Starting static site generation for Freak 'n Fries...")
    
    # Initialize database if it doesn't exist
    from app import init_db
    init_db()
    
    # Clean build directory
    clean_build_directory()
    
    # Generate static files
    print("📄 Generating static HTML files...")
    with app.app_context():
        freezer.freeze()
    
    # Post-processing
    prepare_build_directory()
    optimize_static_files()
    generate_deployment_info()
    
    # Validate build
    if validate_build():
        print("\n🎉 Static site generation completed successfully!")
        print(f"📁 Files generated in: {app.config['FREEZER_DESTINATION']}/")
        print("\n📋 Next steps:")
        print("1. Review the generated files in the build/ directory")
        print("2. Test the site by opening build/index.html in a browser")
        print("3. Commit and push the build/ directory to GitHub")
        print("4. Configure GitHub Pages to serve from the main branch")
        print("\n🌐 Your site will be live at: https://yourusername.github.io/repository-name/")
    else:
        print("\n❌ Build validation failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())