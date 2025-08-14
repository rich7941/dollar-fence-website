#!/usr/bin/env python3
"""
Fix Final 4 Files - Target specific URL patterns
"""

import os
import re

def fix_file(file_path, state_slug, city_slug):
    """Fix Alabama URL references in a specific file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix URL patterns
        city_name = city_slug.replace('-', ' ').title()
        
        # Replace Alabama URLs with correct state URLs
        patterns = [
            (f'/locations/alabama/{city_name}/', f'/locations/{state_slug}/{city_slug}/'),
            (f'/locations/alabama/{city_slug}/', f'/locations/{state_slug}/{city_slug}/'),
        ]
        
        for old_pattern, new_pattern in patterns:
            content = content.replace(old_pattern, new_pattern)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Fix the final 4 files"""
    print("🎯 FIXING FINAL 4 FILES...")
    
    files_to_fix = [
        ('locations/utah/st-george/index.html', 'utah', 'st-george'),
        ('locations/missouri/st-louis/index.html', 'missouri', 'st-louis'),
        ('locations/georgia/athens-clarke-county/index.html', 'georgia', 'athens-clarke-county'),
        ('locations/index.html', None, None)  # Special case
    ]
    
    fixed_count = 0
    
    for file_path, state_slug, city_slug in files_to_fix:
        if os.path.exists(file_path):
            print(f"Fixing: {file_path}")
            
            if state_slug and city_slug:
                if fix_file(file_path, state_slug, city_slug):
                    fixed_count += 1
                    print(f"  ✅ Fixed")
                else:
                    print(f"  ⏭️  No changes needed")
            else:
                # Handle locations/index.html separately
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Remove any Alabama references from main locations page
                    content = re.sub(r'\balabama\b', 'state', content, flags=re.IGNORECASE)
                    
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        fixed_count += 1
                        print(f"  ✅ Fixed")
                    else:
                        print(f"  ⏭️  No changes needed")
                        
                except Exception as e:
                    print(f"  ❌ Error: {e}")
        else:
            print(f"File not found: {file_path}")
    
    print(f"\n🎯 FINAL 4 FILES SUMMARY:")
    print(f"Files fixed: {fixed_count}")
    
    # Final verification
    remaining_count = 0
    for file_path, _, _ in files_to_fix:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'alabama' in content.lower():
                        remaining_count += 1
                        print(f"Still contains Alabama: {file_path}")
            except Exception:
                continue
    
    print(f"Files still containing Alabama: {remaining_count}")
    
    if remaining_count == 0:
        print("🎉 100% COMPLETION ACHIEVED!")

if __name__ == "__main__":
    main()

