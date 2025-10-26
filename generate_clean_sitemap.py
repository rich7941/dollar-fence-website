#!/usr/bin/env python3
import os
from datetime import datetime

def generate_clean_sitemap():
    # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Start with clean XML
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''
    
    # Add main pages
    main_pages = [
        ('https://dollarfence.com/', '1.0', 'weekly'),
        ('https://dollarfence.com/about/', '0.8', 'monthly'),
        ('https://dollarfence.com/contact/', '0.8', 'monthly'),
        ('https://dollarfence.com/reviews/', '0.8', 'monthly'),
        ('https://dollarfence.com/fence-types/', '0.8', 'monthly'),
        ('https://dollarfence.com/locations/', '0.9', 'weekly')
    ]
    
    for url, priority, changefreq in main_pages:
        sitemap_content += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{current_date}T00:00:00+00:00</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
'''
    
    # Add fence type pages
    fence_types = [
        'wood-fence', 'steel-fence', 'vinyl-fence', 'chain-link-fence',
        'aluminum-fence', 'dog-fence', 'pool-fence', 'agricultural-fence',
        'deer-fence', 'hardwood-fence', 'trex-fence', 'commercial-fence'
    ]
    
    for fence_type in fence_types:
        url = f'https://dollarfence.com/fence-types/{fence_type}/'
        sitemap_content += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{current_date}T00:00:00+00:00</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    
    # Add location pages by scanning the locations directory
    locations_dir = 'locations'
    if os.path.exists(locations_dir):
        for state in sorted(os.listdir(locations_dir)):
            state_path = os.path.join(locations_dir, state)
            if os.path.isdir(state_path) and not state.startswith('.'):
                for city in sorted(os.listdir(state_path)):
                    city_path = os.path.join(state_path, city)
                    if os.path.isdir(city_path) and not city.startswith('.'):
                        url = f'https://dollarfence.com/locations/{state}/{city}/'
                        sitemap_content += f'''  <url>
    <loc>{url}</loc>
    <lastmod>{current_date}T00:00:00+00:00</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
'''
    
    # Close the XML
    sitemap_content += '</urlset>\n'
    
    # Write the new sitemap
    with open('sitemap_new.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"Generated clean sitemap with {sitemap_content.count('<url>')} URLs")
    return sitemap_content.count('<url>')

if __name__ == '__main__':
    url_count = generate_clean_sitemap()
    print(f"Clean sitemap generated successfully with {url_count} URLs")

