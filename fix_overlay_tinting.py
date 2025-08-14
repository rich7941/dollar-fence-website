#!/usr/bin/env python3
"""
Fix heavy overlay tinting on all location pages
Reduces rgba(0,0,0,0.7) to rgba(0,0,0,0.2) for better image visibility
"""

import os
import re
import glob

def fix_overlay_tinting():
    """Fix heavy overlay tinting in all location pages"""
    
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
            heavy_overlays = content.count('rgba(0,0,0,0.7)')
            
            if heavy_overlays > 0:
                # Fix the heavy overlays
                # Replace rgba(0,0,0,0.7) with rgba(0,0,0,0.2) for lighter tinting
                fixed_content = content.replace('rgba(0,0,0,0.7)', 'rgba(0,0,0,0.2)')
                
                # Also fix any rgba(0,0,0,0.4) to be consistent
                fixed_content = fixed_content.replace('rgba(0,0,0,0.4)', 'rgba(0,0,0,0.2)')
                
                # Write back to file
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                fixed_count += 1
                total_replacements += heavy_overlays
                
                # Get location name for reporting
                location_name = html_file.replace('/home/ubuntu/dollar-fence-website/locations/', '').replace('/index.html', '')
                print(f"✅ Fixed {heavy_overlays} overlay tints in: {location_name}")
            
        except Exception as e:
            print(f"❌ Error processing {html_file}: {e}")
    
    print(f"\n🎯 SUMMARY:")
    print(f"✅ Files processed: {len(html_files)}")
    print(f"✅ Files with fixes: {fixed_count}")
    print(f"✅ Total overlay tints fixed: {total_replacements}")
    
    return fixed_count, total_replacements

def update_generation_scripts():
    """Update the generation scripts to use lighter overlays for future pages"""
    
    scripts_to_update = [
        "/home/ubuntu/dollar-fence-website/generate_location_page.py",
        "/home/ubuntu/dollar-fence-website/batch_generate_all.py",
        "/home/ubuntu/dollar-fence-website/generate_repo_pages.py"
    ]
    
    updated_scripts = 0
    
    for script_path in scripts_to_update:
        if os.path.exists(script_path):
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update any references to heavy overlays in the scripts
                original_content = content
                content = content.replace('rgba(0,0,0,0.7)', 'rgba(0,0,0,0.2)')
                content = content.replace('rgba(0,0,0,0.4)', 'rgba(0,0,0,0.2)')
                
                if content != original_content:
                    with open(script_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    script_name = os.path.basename(script_path)
                    print(f"✅ Updated generation script: {script_name}")
                    updated_scripts += 1
                
            except Exception as e:
                print(f"❌ Error updating {script_path}: {e}")
    
    return updated_scripts

if __name__ == "__main__":
    print("🔧 Starting overlay tinting fix...")
    
    # Fix existing pages
    fixed_files, total_fixes = fix_overlay_tinting()
    
    # Update generation scripts for future consistency
    print(f"\n🔧 Updating generation scripts...")
    updated_scripts = update_generation_scripts()
    
    print(f"\n🎉 Overlay tinting fix complete!")
    print(f"✅ Fixed {total_fixes} heavy overlays in {fixed_files} location pages")
    print(f"✅ Updated {updated_scripts} generation scripts for future consistency")
    print(f"📸 Images will now show with 20% overlay instead of 70% for much better visibility!")

