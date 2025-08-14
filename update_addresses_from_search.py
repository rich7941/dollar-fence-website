#!/usr/bin/env python3
"""
Update Location Pages with Business Center Addresses
Updates Local Business schema markup with cheapest Regus/Servcorp addresses
"""

import os
import re
import json
import csv
from pathlib import Path

def load_address_data():
    """Load the business address search results"""
    address_data = {}
    
    try:
        with open('/home/ubuntu/find_cheapest_business_addresses.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                city = row['City'].strip()
                state = row['State'].strip()
                recommended_address = row['Recommended Address'].strip()
                
                # Skip if no valid address found
                if recommended_address and recommended_address not in ['Not Found', 'N/A', '']:
                    key = f"{city}, {state}"
                    address_data[key] = {
                        'address': recommended_address,
                        'provider': row['Recommended Provider'].strip(),
                        'price': row['Regus Price'] if row['Recommended Provider'] == 'Regus' else row['Servcorp Price']
                    }
    except Exception as e:
        print(f"Error loading address data: {e}")
        return {}
    
    return address_data

def normalize_city_name(city_name):
    """Normalize city names to match the search results"""
    # Handle special cases
    replacements = {
        'And': 'and',
        'Twp': 'Township',
        'St ': 'St. ',
        'Mt ': 'Mount ',
        'Ft ': 'Fort ',
        'N ': 'North ',
        'S ': 'South ',
        'E ': 'East ',
        'W ': 'West ',
        'Ne ': 'Northeast ',
        'Nw ': 'Northwest ',
        'Se ': 'Southeast ',
        'Sw ': 'Southwest '
    }
    
    normalized = city_name
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    
    return normalized

def update_location_addresses():
    """Update all location pages with business center addresses"""
    
    print("🔧 Updating Location Pages with Business Center Addresses...")
    print("Loading address search results...")
    
    address_data = load_address_data()
    
    if not address_data:
        print("❌ No address data loaded. Exiting.")
        return
    
    print(f"📊 Loaded {len(address_data)} business addresses")
    print("-" * 60)
    
    locations_dir = Path("locations")
    updated_count = 0
    not_found_count = 0
    error_count = 0
    
    # Walk through all location directories
    for root, dirs, files in os.walk(locations_dir):
        for file in files:
            if file == "index.html":
                file_path = Path(root) / file
                
                try:
                    # Extract city and state from path
                    path_parts = str(file_path).split('/')
                    if len(path_parts) >= 3:
                        state = path_parts[1].replace('-', ' ').title()
                        city = path_parts[2].replace('-', ' ').title()
                        
                        # Normalize city name
                        city = normalize_city_name(city)
                        
                        # Look up address
                        lookup_key = f"{city}, {state}"
                        
                        if lookup_key in address_data:
                            # Read the file
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            business_address = address_data[lookup_key]['address']
                            provider = address_data[lookup_key]['provider']
                            
                            # Extract just the street address (before first comma)
                            street_address = business_address.split(',')[0].strip()
                            
                            # Pattern to find and replace streetAddress in LocalBusiness schema
                            pattern = r'("streetAddress":\s*")[^"]*(")'
                            replacement = f'\\1{street_address}\\2'
                            
                            new_content = re.sub(pattern, replacement, content)
                            
                            # Write back if changed
                            if new_content != content:
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(new_content)
                                
                                updated_count += 1
                                print(f"✅ Updated: {city}, {state} → {provider} ({street_address})")
                            
                        else:
                            not_found_count += 1
                            print(f"⚠️  No address: {city}, {state}")
                        
                except Exception as e:
                    error_count += 1
                    print(f"❌ Error updating {file_path}: {str(e)}")
    
    print("-" * 60)
    print(f"🎉 Address Update Complete!")
    print(f"✅ Updated: {updated_count} location pages")
    print(f"⚠️  No address found: {not_found_count} pages")
    if error_count > 0:
        print(f"❌ Errors: {error_count} pages")
    print(f"📊 Total processed: {updated_count + not_found_count + error_count} pages")
    print()
    print("🎯 Result: Location pages now use legitimate business center addresses")
    print("📈 Expected: 1,089 structured data validation errors should be resolved")
    print("💰 Cost: Using cheapest available Regus/Servcorp options")

if __name__ == "__main__":
    update_location_addresses()

