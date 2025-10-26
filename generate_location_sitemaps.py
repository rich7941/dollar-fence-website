#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
from datetime import datetime

def generate_location_sitemaps():
    """Generate comprehensive location sitemaps"""
    
    base_url = "https://dollarfence.com"
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    
    # Find all location HTML files
    location_urls = []
    for root, dirs, files in os.walk('locations'):
        for file in files:
            if file == 'index.html':
                # Convert file path to URL
                url_path = root.replace('\\', '/')  # Handle Windows paths
                url = f"{base_url}/{url_path}/"
                location_urls.append(url)
    
    # Sort URLs for better organization
    location_urls.sort()
    
    print(f"Found {len(location_urls)} location pages")
    
    # Split into two sitemaps for better organization
    mid_point = len(location_urls) // 2
    priority_locations = location_urls[:mid_point]
    secondary_locations = location_urls[mid_point:]
    
    # Generate priority sitemap
    generate_sitemap(priority_locations, 'sitemap-business-priority.xml', 0.8, current_time)
    
    # Generate secondary sitemap  
    generate_sitemap(secondary_locations, 'sitemap-business-secondary.xml', 0.6, current_time)
    
    print(f"Generated sitemap-business-priority.xml with {len(priority_locations)} URLs")
    print(f"Generated sitemap-business-secondary.xml with {len(secondary_locations)} URLs")
    
    return len(location_urls)

def generate_sitemap(urls, filename, priority, current_time):
    """Generate a sitemap file"""
    
    # Create root element
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Add URLs
    for url in urls:
        url_elem = ET.SubElement(urlset, 'url')
        
        loc_elem = ET.SubElement(url_elem, 'loc')
        loc_elem.text = url
        
        lastmod_elem = ET.SubElement(url_elem, 'lastmod')
        lastmod_elem.text = current_time
        
        changefreq_elem = ET.SubElement(url_elem, 'changefreq')
        changefreq_elem.text = 'monthly'
        
        priority_elem = ET.SubElement(url_elem, 'priority')
        priority_elem.text = str(priority)
    
    # Create tree and write to file
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    
    with open(filename, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
        tree.write(f, encoding='utf-8', xml_declaration=False)

if __name__ == "__main__":
    generate_location_sitemaps()

