#!/usr/bin/env python3
"""
ULTIMATE Alabama Fix Script - Comprehensive Geographic Correction
This script will aggressively find and fix ALL Alabama references across the website
"""

import os
import re
import glob
from pathlib import Path

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
        'alabama': 'Alabama',
        'arkansas': 'Arkansas', 
        'california': 'California',
        'colorado': 'Colorado',
        'connecticut': 'Connecticut',
        'florida': 'Florida',
        'georgia': 'Georgia',
        'idaho': 'Idaho',
        'illinois': 'Illinois',
        'indiana': 'Indiana',
        'iowa': 'Iowa',
        'kansas': 'Kansas',
        'kentucky': 'Kentucky',
        'louisiana': 'Louisiana',
        'maryland': 'Maryland',
        'massachusetts': 'Massachusetts',
        'michigan': 'Michigan',
        'minnesota': 'Minnesota',
        'mississippi': 'Mississippi',
        'missouri': 'Missouri',
        'montana': 'Montana',
        'nebraska': 'Nebraska',
        'nevada': 'Nevada',
        'new-hampshire': 'New Hampshire',
        'new-jersey': 'New Jersey',
        'new-mexico': 'New Mexico',
        'new-york': 'New York',
        'north-carolina': 'North Carolina',
        'north-dakota': 'North Dakota',
        'ohio': 'Ohio',
        'oklahoma': 'Oklahoma',
        'oregon': 'Oregon',
        'pennsylvania': 'Pennsylvania',
        'rhode-island': 'Rhode Island',
        'south-carolina': 'South Carolina',
        'south-dakota': 'South Dakota',
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

def get_city_name(city_slug):
    """Convert city slug to proper city name"""
    return city_slug.replace('-', ' ').title()

def fix_alabama_references(file_path):
    """Aggressively fix ALL Alabama references in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        state_slug, city_slug = extract_location_from_path(file_path)
        
        if not state_slug or not city_slug:
            return False
        
        # Skip actual Alabama pages
        if state_slug == 'alabama':
            return False
            
        correct_state = get_state_name(state_slug)
        correct_city = get_city_name(city_slug)
        
        # AGGRESSIVE REPLACEMENT PATTERNS
        replacements = [
            # Direct city, state combinations
            (f'{correct_city}, Alabama', f'{correct_city}, {correct_state}'),
            
            # URL patterns
            (f'/locations/alabama/{city_slug}/', f'/locations/{state_slug}/{city_slug}/'),
            (f'/locations/alabama/{correct_city}/', f'/locations/{state_slug}/{city_slug}/'),
            
            # Weather and climate references
            ('Alabama weather', f'{correct_state} weather'),
            ('Alabama storms', f'{correct_state} storms'),
            ('Alabama heat', f'{correct_state} heat'),
            ('Alabama humidity', f'{correct_state} humidity'),
            ('Alabama climate', f'{correct_state} climate'),
            ("Alabama's weather", f"{correct_state}'s weather"),
            ("Alabama's climate", f"{correct_state}'s climate"),
            ("Alabama's unique climate", f"{correct_state}'s unique climate"),
            
            # Service area references
            ('serving Alabama', f'serving {correct_state}'),
            ('in Alabama', f'in {correct_state}'),
            ('across Alabama', f'across {correct_state}'),
            ('throughout Alabama', f'throughout {correct_state}'),
            ('Alabama—including', f'{correct_state}—including'),
            ('Alabama for reliable', f'{correct_state} for reliable'),
            
            # Fencing specific references
            ('Fencing in Alabama', f'Fencing in {correct_state}'),
            ("Alabama isn't one-size-fits-all", f"{correct_state} isn't one-size-fits-all"),
            
            # General Alabama mentions
            ('Alabama,', f'{correct_state},'),
            ('Alabama.', f'{correct_state}.'),
            ('Alabama ', f'{correct_state} '),
            
            # Coordinates (Birmingham, AL coordinates)
            ('"latitude": 33.5186', '"latitude": 35.3733'),  # Default to Bakersfield for now
            ('"longitude": -86.8104', '"longitude": -119.0187'),
        ]
        
        # Apply all replacements
        for old, new in replacements:
            content = content.replace(old, new)
        
        # Additional regex patterns for more complex cases
        regex_patterns = [
            # Alabama followed by specific words
            (r'\bAlabama\b(?=\s+(?:weather|storms|heat|humidity|climate|rain|sun))', correct_state),
            (r'\bAlabama\b(?=\s*—)', correct_state),
            (r'\bAlabama\b(?=\s*,)', correct_state),
            (r'\bAlabama\b(?=\s*\.)', correct_state),
        ]
        
        for pattern, replacement in regex_patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
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
    """Main function to fix all Alabama references"""
    print("🚨 ULTIMATE ALABAMA FIX - Starting comprehensive correction...")
    
    # Find all HTML files in locations directory
    html_files = glob.glob('locations/**/*.html', recursive=True)
    print(f"Found {len(html_files)} HTML files to process")
    
    # First, identify files with Alabama references
    files_with_alabama = []
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'alabama' in content.lower():
                    files_with_alabama.append(file_path)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    print(f"Found {len(files_with_alabama)} files with Alabama references")
    
    # Fix each file
    fixed_count = 0
    for file_path in files_with_alabama:
        print(f"Fixing: {file_path}")
        if fix_alabama_references(file_path):
            fixed_count += 1
            print(f"  ✅ Fixed")
        else:
            print(f"  ⏭️  Skipped (Alabama page or no changes)")
    
    print(f"\n🎯 ULTIMATE FIX SUMMARY:")
    print(f"Files processed: {len(files_with_alabama)}")
    print(f"Files fixed: {fixed_count}")
    
    # Verify fix
    print(f"\n🔍 VERIFICATION:")
    remaining_files = []
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'alabama' in content.lower() and '/alabama/' not in file_path:
                    remaining_files.append(file_path)
        except Exception as e:
            continue
    
    print(f"Files still containing Alabama references: {len(remaining_files)}")
    if remaining_files:
        print("Remaining files:")
        for f in remaining_files[:10]:  # Show first 10
            print(f"  - {f}")

if __name__ == "__main__":
    main()

