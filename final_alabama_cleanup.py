#!/usr/bin/env python3
"""
Final Alabama Cleanup Script - Target remaining specific patterns
"""

import os
import re
import glob

def extract_location_from_path(file_path):
    """Extract state and city from file path"""
    parts = file_path.split('/')
    if len(parts) >= 4 and 'locations' in parts:
        locations_idx = parts.index('locations')
        if locations_idx + 2 < len(parts):
            state = parts[locations_idx + 1]
            city = parts[locations_idx + 2]
            return state, city
    return None, None

def get_state_name(state_slug):
    """Convert state slug to proper state name"""
    state_names = {
        'california': 'California',
        'florida': 'Florida',
        'georgia': 'Georgia',
        'illinois': 'Illinois',
        'kentucky': 'Kentucky',
        'maryland': 'Maryland',
        'minnesota': 'Minnesota',
        'missouri': 'Missouri',
        'north-carolina': 'North Carolina',
        'north-dakota': 'North Dakota',
        'tennessee': 'Tennessee',
        'texas': 'Texas',
        'utah': 'Utah',
        'vermont': 'Vermont',
        'virginia': 'Virginia',
        'washington': 'Washington',
        'west-virginia': 'West Virginia',
        'wisconsin': 'Wisconsin',
        'wyoming': 'Wyoming'
    }
    return state_names.get(state_slug, state_slug.replace('-', ' ').title())

def final_cleanup(file_path):
    """Final aggressive cleanup of Alabama references"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        state_slug, city_slug = extract_location_from_path(file_path)
        
        # Skip actual Alabama pages
        if state_slug == 'alabama':
            return False
            
        if not state_slug or not city_slug:
            return False
            
        correct_state = get_state_name(state_slug)
        
        # Use regex to find and replace any pattern of "CITY, Alabama" with "CITY, CORRECT_STATE"
        # This will catch complex city names with special characters
        pattern = r'([^<>]+),\s*Alabama'
        replacement = rf'\1, {correct_state}'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # Additional specific patterns
        content = re.sub(r'\bAlabama\b', correct_state, content)
        
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
    """Main function for final cleanup"""
    print("🧹 FINAL ALABAMA CLEANUP - Targeting remaining patterns...")
    
    # Find files that still have Alabama references
    html_files = glob.glob('locations/**/*.html', recursive=True)
    files_with_alabama = []
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'alabama' in content.lower() and '/alabama/' not in file_path:
                    files_with_alabama.append(file_path)
        except Exception:
            continue
    
    print(f"Found {len(files_with_alabama)} files still containing Alabama references")
    
    # Fix each file
    fixed_count = 0
    for file_path in files_with_alabama:
        print(f"Final cleanup: {file_path}")
        if final_cleanup(file_path):
            fixed_count += 1
            print(f"  ✅ Cleaned")
        else:
            print(f"  ⏭️  No changes")
    
    print(f"\n🎯 FINAL CLEANUP SUMMARY:")
    print(f"Files processed: {len(files_with_alabama)}")
    print(f"Files cleaned: {fixed_count}")
    
    # Final verification
    remaining_count = 0
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'alabama' in content.lower() and '/alabama/' not in file_path:
                    remaining_count += 1
        except Exception:
            continue
    
    print(f"Files still containing Alabama references: {remaining_count}")

if __name__ == "__main__":
    main()

