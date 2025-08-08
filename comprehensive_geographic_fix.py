#!/usr/bin/env python3
"""
Comprehensive Geographic Fix Script for Dollar Fence Website
Fixes all Alabama/Birmingham reference errors across location pages
"""

import os
import re
import csv
import json
from pathlib import Path

# Coordinate mapping for major cities (lat, lng)
CITY_COORDINATES = {
    # Alabama
    'birmingham': (33.5186, -86.8104),
    'huntsville': (34.7304, -86.5861),
    'montgomery': (32.3668, -86.3000),
    
    # Arkansas  
    'fayetteville': (36.0625, -94.1574),
    'little-rock': (34.7465, -92.2896),
    
    # California
    'anaheim': (33.8366, -117.9143),
    'bakersfield': (35.3733, -119.0187),
    'chula-vista': (32.6401, -117.0842),
    'fresno': (36.7378, -119.7871),
    'inland-empire': (34.0522, -117.7500),
    'irvine': (33.6846, -117.8265),
    'long-beach': (33.7701, -118.1937),
    'los-angeles': (34.0522, -118.2437),
    'north-san-diego': (32.8312, -117.1225),
    'northeastern-los-angeles': (34.1522, -118.1437),
    'oakland': (37.8044, -122.2712),
    'orange-county': (33.7175, -117.8311),
    'riverside-county': (33.7175, -116.2023),
    'riverside': (33.9533, -117.3962),
    'sacramento': (38.5816, -121.4944),
    'san-diego': (32.7157, -117.1611),
    'san-francisco-and-east-bay': (37.7749, -122.4194),
    'san-francisco': (37.7749, -122.4194),
    'san-jose': (37.3382, -121.8863),
    'santa-ana': (33.7455, -117.8677),
    'south-bay': (37.5630, -122.3255),
    'stockton': (37.9577, -121.2908),
    'ventura-county-and-santa-clarita-valley': (34.4208, -118.5739),
    'west-los-angeles': (34.0522, -118.4437),
    
    # Add more coordinates as needed - this is a sample
    # For now, we'll use a default calculation for missing cities
}

def get_coordinates_for_city(city_name, state_name):
    """Get coordinates for a city, with fallback to approximate calculation"""
    city_key = city_name.lower().replace(' ', '-')
    
    if city_key in CITY_COORDINATES:
        return CITY_COORDINATES[city_key]
    
    # For cities not in our mapping, we'll use state-based approximations
    # This is a simplified approach - in production you'd use a geocoding API
    state_defaults = {
        'alabama': (32.806671, -86.791130),
        'arkansas': (34.969704, -92.373123),
        'california': (36.116203, -119.681564),
        'colorado': (39.059811, -105.311104),
        'connecticut': (41.767, -72.677),
        'florida': (27.766279, -81.686783),
        'georgia': (33.76, -84.39),
        'idaho': (44.240459, -114.478828),
        'illinois': (40.349457, -88.986137),
        'indiana': (39.790942, -86.147685),
        'iowa': (42.011539, -93.210526),
        'kansas': (38.572954, -98.580480),
        'kentucky': (37.669789, -84.670067),
        'louisiana': (31.169546, -91.867805),
        'maryland': (39.063946, -76.802101),
        'massachusetts': (42.230171, -71.530106),
        'michigan': (43.326618, -84.536095),
        'minnesota': (45.694454, -93.900192),
        'mississippi': (32.741646, -89.678696),
        'missouri': (38.572954, -92.189283),
        'montana': (47.052952, -110.454353),
        'nebraska': (41.12537, -98.268082),
        'nevada': (39.161921, -117.327728),
        'new-hampshire': (43.452492, -71.563896),
        'new-jersey': (40.221741, -74.756138),
        'new-mexico': (34.97273, -105.032363),
        'new-york': (42.659829, -75.615137),
        'north-carolina': (35.771, -78.638),
        'north-dakota': (47.052952, -100.437012),
        'ohio': (40.367474, -82.996216),
        'oklahoma': (35.482309, -97.534994),
        'oregon': (44.931109, -123.029159),
        'pennsylvania': (40.269789, -76.875613),
        'rhode-island': (41.82355, -71.422132),
        'south-carolina': (33.836082, -81.163727),
        'south-dakota': (44.299782, -99.438828),
        'tennessee': (35.771, -86.25),
        'texas': (31.106, -97.6475),
        'utah': (40.150032, -111.862434),
        'vermont': (44.26639, -72.580536),
        'virginia': (37.54, -78.86),
        'washington': (47.042418, -120.61084),
        'west-virginia': (38.349497, -81.633294),
        'wisconsin': (44.268543, -89.616508),
        'wyoming': (42.755966, -107.302490)
    }
    
    return state_defaults.get(state_name.lower(), (39.8283, -98.5795))  # Center of US as fallback

def extract_location_from_path(file_path):
    """Extract state and city from file path"""
    # Path format: /locations/state/city/index.html
    parts = file_path.split('/')
    if len(parts) >= 4 and 'locations' in parts:
        locations_idx = parts.index('locations')
        if locations_idx + 2 < len(parts):
            state = parts[locations_idx + 1]
            city = parts[locations_idx + 2]
            return state, city
    return None, None

def fix_file_content(file_path, scan_result):
    """Fix all geographic errors in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        state, city = extract_location_from_path(file_path)
        
        if not state or not city:
            print(f"Could not extract location from path: {file_path}")
            return False
        
        # Get proper coordinates
        correct_lat, correct_lng = get_coordinates_for_city(city, state)
        
        # Fix canonical URL
        if scan_result.get('canonical_url_error'):
            # Replace /alabama/ with correct state
            content = re.sub(
                r'<link rel="canonical" href="https://dollarfence\.com/locations/alabama/([^"]+)"',
                f'<link rel="canonical" href="https://dollarfence.com/locations/{state}/\\1"',
                content,
                flags=re.IGNORECASE
            )
        
        # Fix Open Graph URL
        if scan_result.get('og_url_error'):
            content = re.sub(
                r'<meta property="og:url" content="https://dollarfence\.com/locations/alabama/([^"]+)"',
                f'<meta property="og:url" content="https://dollarfence.com/locations/{state}/\\1"',
                content,
                flags=re.IGNORECASE
            )
        
        # Fix Schema URL
        if scan_result.get('schema_url_error'):
            content = re.sub(
                r'"url": "https://dollarfence\.com/locations/alabama/([^"]+)"',
                f'"url": "https://dollarfence.com/locations/{state}/\\1"',
                content
            )
        
        # Fix coordinates (Birmingham coordinates: 33.5186, -86.8104)
        if scan_result.get('coordinates_error'):
            # Replace Birmingham coordinates with correct ones
            content = re.sub(
                r'"latitude": 33\.5186',
                f'"latitude": {correct_lat}',
                content
            )
            content = re.sub(
                r'"longitude": -86\.8104',
                f'"longitude": {correct_lng}',
                content
            )
        
        # Fix text content - replace "Alabama" with correct state name (capitalized)
        if scan_result.get('text_content_error'):
            state_name = state.replace('-', ' ').title()
            
            # Replace "Alabama" with correct state name, but be careful about context
            # Only replace when it's clearly referring to the state
            patterns_to_fix = [
                (r'\bAlabama\b(?=\s+(?:weather|storms|heat|humidity|climate))', state_name),
                (r'\bserving Alabama\b', f'serving {state_name}'),
                (r'\bin Alabama\b', f'in {state_name}'),
                (r'\bAlabama\s+(?:isn\'t|is|has|gets)', f'{state_name} \\1'),
                (r'\bAlabama—', f'{state_name}—'),
                (r'\bAlabama,', f'{state_name},'),
                (r'\bAlabama\.', f'{state_name}.'),
            ]
            
            for pattern, replacement in patterns_to_fix:
                content = re.sub(pattern, replacement, content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all geographic errors"""
    print("Starting comprehensive geographic fix...")
    
    # Read scan results
    scan_results = {}
    try:
        with open('/home/ubuntu/scan_geographic_errors.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Has Geographic Errors'] == 'True':
                    scan_results[row['File Path']] = {
                        'canonical_url_error': row['Canonical URL Error'] == 'True',
                        'og_url_error': row['Open Graph URL Error'] == 'True', 
                        'schema_url_error': row['Schema URL Error'] == 'True',
                        'coordinates_error': row['Coordinates Error'] == 'True',
                        'text_content_error': row['Text Content Error'] == 'True',
                        'error_count': int(row['Error Count']) if row['Error Count'].isdigit() else 0
                    }
    except Exception as e:
        print(f"Error reading scan results: {e}")
        return
    
    print(f"Found {len(scan_results)} files to fix")
    
    # Fix each file
    fixed_count = 0
    failed_count = 0
    
    for file_path, scan_result in scan_results.items():
        print(f"Fixing: {file_path}")
        if fix_file_content(file_path, scan_result):
            fixed_count += 1
            print(f"  ✓ Fixed {scan_result['error_count']} errors")
        else:
            failed_count += 1
            print(f"  ✗ Failed to fix")
    
    print(f"\nFix Summary:")
    print(f"Files fixed: {fixed_count}")
    print(f"Files failed: {failed_count}")
    print(f"Total processed: {len(scan_results)}")

if __name__ == "__main__":
    main()

