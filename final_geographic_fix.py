#!/usr/bin/env python3
"""
Final Geographic Fix Script for Dollar Fence Website
Targets remaining Alabama/Birmingham references with comprehensive patterns
"""

import os
import re
import csv
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

def fix_remaining_errors(file_path):
    """Fix remaining geographic errors in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        state, city = extract_location_from_path(file_path)
        
        if not state or not city:
            return False
        
        # Get proper state and city names
        state_name = state.replace('-', ' ').title()
        city_name = city.replace('-', ' ').title()
        
        # Fix remaining Alabama references in text
        patterns_to_fix = [
            # Geographic references
            (r'\bAlabama\'s unique climate\b', f'{state_name}\'s unique climate'),
            (r'\bAlabama\'s climate\b', f'{state_name}\'s climate'),
            (r'\bAlabama\'s weather\b', f'{state_name}\'s weather'),
            (r'\bAlabama\'s\b', f'{state_name}\'s'),
            (r'\bAlabama\b(?=\s+(?:weather|storms|heat|humidity|climate|rain|sun))', state_name),
            
            # City, State references
            (rf'\b{city_name}, Alabama\b', f'{city_name}, {state_name}'),
            (rf'\b{city.replace("-", " ").title()}, Alabama\b', f'{city_name}, {state_name}'),
            
            # Service area references
            (r'\bin Alabama\b', f'in {state_name}'),
            (r'\bserving Alabama\b', f'serving {state_name}'),
            (r'\bacross Alabama\b', f'across {state_name}'),
            (r'\bthroughout Alabama\b', f'throughout {state_name}'),
            
            # Image alt text
            (r'Alabama service', f'{state_name} service'),
            (r'and Alabama', f'and {state_name}'),
            
            # General Alabama mentions
            (r'\bAlabama—', f'{state_name}—'),
            (r'\bAlabama,', f'{state_name},'),
            (r'\bAlabama\.', f'{state_name}.'),
            (r'\bAlabama\s+', f'{state_name} '),
        ]
        
        # Apply all patterns
        for pattern, replacement in patterns_to_fix:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # Fix any remaining Birmingham coordinates
        content = content.replace('"latitude": 33.5186', f'"latitude": 35.3733')  # Bakersfield coords
        content = content.replace('"longitude": -86.8104', f'"longitude": -119.0187')
        
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
    """Main function to fix remaining geographic errors"""
    print("Starting final geographic fix...")
    
    # Read the list of files that had errors
    files_to_fix = []
    try:
        with open('/home/ubuntu/files_to_fix.txt', 'r') as f:
            files_to_fix = [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Error reading files list: {e}")
        return
    
    print(f"Processing {len(files_to_fix)} files...")
    
    fixed_count = 0
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_remaining_errors(file_path):
                fixed_count += 1
                print(f"✓ Fixed remaining errors in: {file_path}")
    
    print(f"\nFinal Fix Summary:")
    print(f"Files processed: {len(files_to_fix)}")
    print(f"Files with additional fixes: {fixed_count}")

if __name__ == "__main__":
    main()

