#!/usr/bin/env python3
"""
Fix XML Sitemap Format Errors - Version 2
Properly handles namespace prefixes and creates clean XML format
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import re

def fix_sitemap_format():
    """Fix sitemap format issues by cleaning XML structure"""
    
    print("Starting sitemap format fix...")
    
    # Parse the current sitemap with namespace handling
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        
        # Define the namespace
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # Create new root element without namespace prefix
        new_root = ET.Element('urlset')
        new_root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        # Get current date for consistency
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Process each URL entry
        url_count = 0
        for url in root.findall('ns0:url', {'ns0': 'http://www.sitemaps.org/schemas/sitemap/0.9'}):
            new_url = ET.SubElement(new_root, 'url')
            
            # Extract and clean each element
            loc_elem = url.find('ns0:loc', {'ns0': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
            lastmod_elem = url.find('ns0:lastmod', {'ns0': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
            changefreq_elem = url.find('ns0:changefreq', {'ns0': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
            priority_elem = url.find('ns0:priority', {'ns0': 'http://www.sitemaps.org/schemas/sitemap/0.9'})
            
            # Add elements in correct order
            if loc_elem is not None and loc_elem.text:
                loc = ET.SubElement(new_url, 'loc')
                loc.text = loc_elem.text
                
                lastmod = ET.SubElement(new_url, 'lastmod')
                lastmod.text = current_date
                
                changefreq = ET.SubElement(new_url, 'changefreq')
                changefreq.text = changefreq_elem.text if changefreq_elem is not None else 'weekly'
                
                priority = ET.SubElement(new_url, 'priority')
                priority.text = priority_elem.text if priority_elem is not None else '0.8'
                
                url_count += 1
        
        # Create new tree and write clean XML
        new_tree = ET.ElementTree(new_root)
        ET.indent(new_tree, space="  ", level=0)
        
        # Write with proper XML declaration
        new_tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)
        
        print("✅ Sitemap format fixed successfully!")
        print(f"- Processed {url_count} URLs")
        print("- Removed namespace prefixes")
        print("- Standardized XML structure")
        print(f"- Updated all dates to {current_date}")
        
        return True, url_count
        
    except Exception as e:
        print(f"❌ Error fixing sitemap: {e}")
        return False, 0

def validate_sitemap():
    """Validate the cleaned sitemap"""
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        
        # Check root element and namespace
        if root.tag != 'urlset':
            print(f"❌ Incorrect root element: {root.tag}")
            return False
            
        expected_ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
        if root.get('xmlns') != expected_ns:
            print(f"❌ Incorrect namespace: {root.get('xmlns')}")
            return False
        
        # Count URLs and validate structure
        urls = root.findall('url')
        print(f"✅ Found {len(urls)} URLs in sitemap")
        
        # Validate first few URLs
        issues = 0
        for i, url in enumerate(urls[:5]):
            loc = url.find('loc')
            lastmod = url.find('lastmod')
            changefreq = url.find('changefreq')
            priority = url.find('priority')
            
            if loc is None or not loc.text:
                print(f"❌ URL {i+1}: Missing <loc> element")
                issues += 1
            elif not loc.text.startswith('https://dollarfence.com/'):
                print(f"❌ URL {i+1}: Invalid URL format")
                issues += 1
            
            if lastmod is None:
                print(f"❌ URL {i+1}: Missing <lastmod> element")
                issues += 1
        
        if issues == 0:
            print("✅ Sitemap validation passed!")
            return True
        else:
            print(f"❌ Found {issues} validation issues")
            return False
            
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

if __name__ == "__main__":
    print("=== SITEMAP FORMAT FIX V2 ===")
    
    # Backup original
    import shutil
    shutil.copy('sitemap.xml', 'sitemap_backup.xml')
    print("📋 Created backup: sitemap_backup.xml")
    
    # Fix format issues
    success, url_count = fix_sitemap_format()
    
    if success and url_count > 0:
        # Validate the result
        if validate_sitemap():
            print("🎉 Sitemap format fix completed successfully!")
        else:
            print("⚠️  Format fixed but validation warnings exist")
    else:
        print("❌ Failed to fix sitemap format")
        # Restore backup
        shutil.copy('sitemap_backup.xml', 'sitemap.xml')
        print("📋 Restored from backup")

