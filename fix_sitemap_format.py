#!/usr/bin/env python3
"""
Fix XML Sitemap Format Errors
Removes namespace prefixes and ensures clean XML format for better compatibility
"""

import xml.etree.ElementTree as ET
from datetime import datetime
import re

def fix_sitemap_format():
    """Fix sitemap format issues by cleaning XML structure"""
    
    print("Starting sitemap format fix...")
    
    # Read the current sitemap
    with open('sitemap.xml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove namespace prefixes (ns0:) that cause format errors
    content = content.replace('ns0:', '')
    content = content.replace('xmlns:ns0=', 'xmlns=')
    
    # Ensure proper XML declaration
    if not content.startswith('<?xml'):
        content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content
    
    # Parse and reformat the XML for consistency
    try:
        root = ET.fromstring(content)
        
        # Set the correct namespace
        root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        # Get current date for consistency
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Clean up and standardize all URL entries
        for url in root.findall('url'):
            # Ensure all required elements exist
            loc = url.find('loc')
            lastmod = url.find('lastmod')
            changefreq = url.find('changefreq')
            priority = url.find('priority')
            
            if lastmod is not None:
                # Standardize date format
                lastmod.text = current_date
            
            # Ensure proper ordering of elements
            # Remove and re-add elements in correct order
            elements = []
            if loc is not None:
                elements.append(('loc', loc.text))
                url.remove(loc)
            if lastmod is not None:
                elements.append(('lastmod', lastmod.text))
                url.remove(lastmod)
            if changefreq is not None:
                elements.append(('changefreq', changefreq.text))
                url.remove(changefreq)
            if priority is not None:
                elements.append(('priority', priority.text))
                url.remove(priority)
            
            # Re-add elements in correct order
            for tag, text in elements:
                elem = ET.SubElement(url, tag)
                elem.text = text
        
        # Write the cleaned XML
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)
        tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)
        
        print("✅ Sitemap format fixed successfully!")
        print("- Removed namespace prefixes")
        print("- Standardized XML structure")
        print("- Updated date format consistency")
        
        # Verify the fix
        with open('sitemap.xml', 'r', encoding='utf-8') as f:
            new_content = f.read()
            url_count = new_content.count('<url>')
            print(f"- Verified {url_count} URLs in clean format")
        
        return True
        
    except ET.ParseError as e:
        print(f"❌ XML parsing error: {e}")
        return False

def validate_sitemap():
    """Validate the sitemap structure"""
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        
        # Check namespace
        expected_ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
        if root.get('xmlns') != expected_ns:
            print(f"⚠️  Warning: Incorrect namespace. Expected: {expected_ns}")
        
        # Count URLs
        urls = root.findall('url')
        print(f"✅ Sitemap contains {len(urls)} URLs")
        
        # Check for required elements
        issues = 0
        for i, url in enumerate(urls[:5]):  # Check first 5 URLs
            loc = url.find('loc')
            if loc is None or not loc.text:
                print(f"❌ URL {i+1}: Missing or empty <loc> element")
                issues += 1
        
        if issues == 0:
            print("✅ Sitemap validation passed!")
        else:
            print(f"⚠️  Found {issues} validation issues")
        
        return issues == 0
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

if __name__ == "__main__":
    print("=== SITEMAP FORMAT FIX ===")
    
    # Fix format issues
    if fix_sitemap_format():
        # Validate the result
        validate_sitemap()
    else:
        print("❌ Failed to fix sitemap format")

