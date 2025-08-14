#!/usr/bin/env python3
"""
Remove Specific Broken URLs from Sitemap
Removes the URLs that are causing 404 errors
"""

import xml.etree.ElementTree as ET
import os
import shutil

def remove_broken_urls():
    """Remove specific broken URLs from sitemap and delete corresponding files"""
    
    # URLs to remove (as provided by user)
    urls_to_remove = [
        "https://dollarfence.com/locations/florida/port-st.-lucie/",
        "https://dollarfence.com/locations/new-jersey/hamilton-twp./", 
        "https://dollarfence.com/locations/utah/st.-george/",
        "https://dollarfence.com/locations/minnesota/st.-paul/",
        "https://dollarfence.com/locations/missouri/st.-louis/",
        "https://dollarfence.com/locations/florida/st.-johns/"
    ]
    
    # Also check for variations without periods
    url_variations = [
        "https://dollarfence.com/locations/florida/port-st-lucie/",
        "https://dollarfence.com/locations/new-jersey/hamilton-township/",
        "https://dollarfence.com/locations/utah/st-george/", 
        "https://dollarfence.com/locations/minnesota/saint-paul/",
        "https://dollarfence.com/locations/missouri/st-louis/",
        "https://dollarfence.com/locations/florida/st-johns/"
    ]
    
    all_urls_to_remove = urls_to_remove + url_variations
    
    print("=== REMOVING BROKEN URLS ===")
    print(f"Target URLs to remove: {len(urls_to_remove)}")
    
    # Backup original sitemap
    shutil.copy('sitemap.xml', 'sitemap_before_removal.xml')
    print("📋 Created backup: sitemap_before_removal.xml")
    
    # Parse sitemap
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    
    # Count original URLs
    original_count = len(root.findall('url'))
    print(f"Original sitemap contains: {original_count} URLs")
    
    # Remove matching URLs
    removed_count = 0
    removed_urls = []
    
    for url_elem in root.findall('url'):
        loc_elem = url_elem.find('loc')
        if loc_elem is not None and loc_elem.text:
            url = loc_elem.text
            if url in all_urls_to_remove:
                root.remove(url_elem)
                removed_count += 1
                removed_urls.append(url)
                print(f"✅ Removed: {url}")
    
    # Save cleaned sitemap
    tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)
    
    final_count = len(root.findall('url'))
    print(f"\n=== REMOVAL SUMMARY ===")
    print(f"URLs removed: {removed_count}")
    print(f"Original count: {original_count}")
    print(f"Final count: {final_count}")
    print(f"Expected reduction: {original_count - final_count}")
    
    # List removed URLs
    if removed_urls:
        print(f"\n=== REMOVED URLS ===")
        for url in removed_urls:
            print(f"- {url}")
    
    # Check for corresponding directories to remove
    print(f"\n=== CHECKING FOR FILES TO DELETE ===")
    directories_to_check = [
        "locations/florida/port-st-lucie",
        "locations/new-jersey/hamilton-township", 
        "locations/utah/st-george",
        "locations/minnesota/saint-paul",
        "locations/missouri/st-louis",
        "locations/florida/st-johns"
    ]
    
    deleted_dirs = 0
    for dir_path in directories_to_check:
        full_path = os.path.join('.', dir_path)
        if os.path.exists(full_path):
            try:
                shutil.rmtree(full_path)
                print(f"🗑️  Deleted directory: {dir_path}")
                deleted_dirs += 1
            except Exception as e:
                print(f"❌ Failed to delete {dir_path}: {e}")
        else:
            print(f"ℹ️  Directory not found: {dir_path}")
    
    print(f"\n=== CLEANUP SUMMARY ===")
    print(f"Directories deleted: {deleted_dirs}")
    print(f"Sitemap URLs removed: {removed_count}")
    
    return removed_count, final_count

def validate_sitemap():
    """Validate the cleaned sitemap"""
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        
        url_count = len(root.findall('url'))
        print(f"✅ Sitemap validation: {url_count} URLs remaining")
        
        # Check for any remaining problematic URLs
        problematic_patterns = ['st.-', 'twp.', 'port-st.-lucie']
        issues_found = 0
        
        for url_elem in root.findall('url'):
            loc_elem = url_elem.find('loc')
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
        print("This might mean the URLs have different formatting in the sitemap")

