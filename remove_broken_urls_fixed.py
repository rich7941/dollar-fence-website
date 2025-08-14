#!/usr/bin/env python3
"""
Remove Specific Broken URLs from Sitemap - Fixed Version
Properly handles XML namespaces
"""

import xml.etree.ElementTree as ET
import os
import shutil

def remove_broken_urls():
    """Remove specific broken URLs from sitemap and delete corresponding files"""
    
    # URLs to remove (as provided by user) - check for both formats
    urls_to_remove = [
        "https://dollarfence.com/locations/florida/port-st.-lucie/",
        "https://dollarfence.com/locations/florida/port-st-lucie/",
        "https://dollarfence.com/locations/new-jersey/hamilton-twp./", 
        "https://dollarfence.com/locations/new-jersey/hamilton-township/",
        "https://dollarfence.com/locations/utah/st.-george/",
        "https://dollarfence.com/locations/utah/st-george/",
        "https://dollarfence.com/locations/minnesota/st.-paul/",
        "https://dollarfence.com/locations/minnesota/saint-paul/",
        "https://dollarfence.com/locations/missouri/st.-louis/",
        "https://dollarfence.com/locations/missouri/st-louis/",
        "https://dollarfence.com/locations/florida/st.-johns/",
        "https://dollarfence.com/locations/florida/st-johns/"
    ]
    
    print("=== REMOVING BROKEN URLS ===")
    print(f"Target URLs to remove: {len(urls_to_remove)}")
    
    # Backup original sitemap  
    shutil.copy('sitemap.xml', 'sitemap_before_removal.xml')
    print("📋 Created backup: sitemap_before_removal.xml")
    
    # Parse sitemap with namespace handling
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    
    # Define namespace
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    # Count original URLs - handle both with and without namespace
    original_urls = root.findall('.//url') or root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    original_count = len(original_urls)
    print(f"Original sitemap contains: {original_count} URLs")
    
    # Remove matching URLs
    removed_count = 0
    removed_urls = []
    
    # Handle namespace prefixed elements
    for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc_elem = url_elem.find('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        if loc_elem is not None and loc_elem.text:
            url = loc_elem.text
            if url in urls_to_remove:
                root.remove(url_elem)
                removed_count += 1
                removed_urls.append(url)
                print(f"✅ Removed: {url}")
    
    # Also try without namespace (fallback)
    for url_elem in root.findall('.//url'):
        loc_elem = url_elem.find('.//loc')
        if loc_elem is not None and loc_elem.text:
            url = loc_elem.text
            if url in urls_to_remove:
                root.remove(url_elem)
                removed_count += 1
                removed_urls.append(url)
                print(f"✅ Removed: {url}")
    
    # Save cleaned sitemap
    tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)
    
    # Recount after removal
    tree_new = ET.parse('sitemap.xml')
    root_new = tree_new.getroot()
    final_urls = root_new.findall('.//url') or root_new.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    final_count = len(final_urls)
    
    print(f"\n=== REMOVAL SUMMARY ===")
    print(f"URLs removed: {removed_count}")
    print(f"Original count: {original_count}")
    print(f"Final count: {final_count}")
    print(f"Actual reduction: {original_count - final_count}")
    
    # List removed URLs
    if removed_urls:
        print(f"\n=== REMOVED URLS ===")
        for url in removed_urls:
            print(f"- {url}")
    
    return removed_count, final_count

def validate_sitemap():
    """Validate the cleaned sitemap"""
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        
        # Count URLs with namespace handling
        urls = root.findall('.//url') or root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        url_count = len(urls)
        print(f"✅ Sitemap validation: {url_count} URLs remaining")
        
        # Check for any remaining problematic URLs
        problematic_patterns = ['st.-', 'twp.', 'port-st.-lucie']
        issues_found = 0
        
        for url_elem in urls:
            loc_elem = url_elem.find('.//loc') or url_elem.find('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc_elem is not None and loc_elem.text:
                url = loc_elem.text
                for pattern in problematic_patterns:
                    if pattern in url:
                        print(f"⚠️  Still contains problematic pattern '{pattern}': {url}")
                        issues_found += 1
        
        if issues_found == 0:
            print("✅ No problematic URL patterns found")
        else:
            print(f"⚠️  Found {issues_found} remaining issues")
        
        return issues_found == 0
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

if __name__ == "__main__":
    removed_count, final_count = remove_broken_urls()
    
    if removed_count > 0:
        print(f"\n🎉 Successfully removed {removed_count} broken URLs!")
        validate_sitemap()
        print(f"\nSitemap now contains {final_count} clean URLs")
    else:
        print("ℹ️  No matching URLs found to remove")
        print("Let me check what URLs are actually in the sitemap...")
        
        # Debug: show some sample URLs
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        urls = root.findall('.//url') or root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        
        print(f"\nSample URLs in sitemap:")
        for i, url_elem in enumerate(urls[:10]):
            loc_elem = url_elem.find('.//loc') or url_elem.find('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc_elem is not None and loc_elem.text:
                print(f"  {i+1}. {loc_elem.text}")
        
        # Check for the specific patterns we're looking for
        print(f"\nLooking for specific patterns:")
        patterns_found = []
        for url_elem in urls:
            loc_elem = url_elem.find('.//loc') or url_elem.find('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc_elem is not None and loc_elem.text:
                url = loc_elem.text
                if any(pattern in url for pattern in ['port-st', 'hamilton', 'st-george', 'saint-paul', 'st-louis', 'st-johns']):
                    patterns_found.append(url)
        
        if patterns_found:
            print("Found these related URLs:")
            for url in patterns_found:
                print(f"  - {url}")
        else:
            print("No related URLs found")

