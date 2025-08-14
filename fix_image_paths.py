#!/usr/bin/env python3
"""
Fix broken image paths in location pages
Replaces '..//assets/images/' with '/assets/images/'
"""

import os
import re
import glob

def fix_image_paths():
    """Fix broken image paths in all location pages"""
    
    # Find all location page HTML files
    location_pattern = "/home/ubuntu/dollar-fence-website/locations/**/index.html"
    html_files = glob.glob(location_pattern, recursive=True)
    
    print(f"Found {len(html_files)} location pages to fix")
    
    fixed_count = 0
    total_replacements = 0
    
    for html_file in html_files:
        try:
            # Read the file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count occurrences before fixing
            broken_paths = content.count('..//assets/images/')
            
            if broken_paths > 0:
                # Fix the broken paths
                # Replace '..//assets/images/' with '/assets/images/'
                fixed_content = content.replace('..//assets/images/', '/assets/images/')
                
                # Write back to file
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                fixed_count += 1
                total_replacements += broken_paths
                
                # Get location name for reporting
                location_name = html_file.replace('/home/ubuntu/dollar-fence-website/locations/', '').replace('/index.html', '')
                print(f"✅ Fixed {broken_paths} image paths in: {location_name}")
            
        except Exception as e:
            print(f"❌ Error processing {html_file}: {e}")
    
    print(f"\n🎯 SUMMARY:")
    print(f"✅ Files processed: {len(html_files)}")
    print(f"✅ Files with fixes: {fixed_count}")
    print(f"✅ Total image paths fixed: {total_replacements}")
    
    return fixed_count, total_replacements

if __name__ == "__main__":
    print("🔧 Starting image path fix...")
    fixed_files, total_fixes = fix_image_paths()
    print(f"\n🎉 Image path fix complete!")
    print(f"Fixed {total_fixes} broken image paths in {fixed_files} location pages")

