#!/usr/bin/env python3
"""
Map Broken Links to Working Alternatives
Identifies which broken links have working alternatives and which need new pages
"""

import os
import json
import glob
from pathlib import Path

def get_existing_location_pages():
    """Get all existing location pages"""
    existing_pages = []
    
    # Find all location HTML files
    location_files = glob.glob("locations/**/*.html", recursive=True)
    
    for file_path in location_files:
        # Convert file path to URL format
        url_path = file_path.replace('locations/', '/locations/')
        url_path = url_path.replace('/index.html', '/')
        url_path = url_path.replace('\\', '/')
        full_url = f"https://dollarfence.com{url_path}"
        
        # Extract state and city from path
        parts = file_path.split('/')
        if len(parts) >= 3:
            state = parts[1]
            city = parts[2]
            
            existing_pages.append({
                'state': state,
                'city': city,
                'url_path': url_path,
                'full_url': full_url,
                'file_path': file_path
            })
    
    return existing_pages

def identify_broken_links():
    """Identify the broken links from the audit"""
    
    # These are the broken links identified in the audit
    broken_links = [
        {
            'display_name': 'Port St. Lucie',
            'broken_url': 'https://dollarfence.com/locations/florida/port-st.-lucie/',
            'state': 'florida',
            'city': 'port-st-lucie',
            'variations': ['port-st-lucie', 'port-st.-lucie']
        },
        {
            'display_name': 'Hamilton Township',
            'broken_url': 'https://dollarfence.com/locations/new-jersey/hamilton-twp./',
            'state': 'new-jersey', 
            'city': 'hamilton-township',
            'variations': ['hamilton-twp', 'hamilton-township']
        },
        {
            'display_name': 'St. George',
            'broken_url': 'https://dollarfence.com/locations/utah/st.-george/',
            'state': 'utah',
            'city': 'st-george',
            'variations': ['st-george', 'st.-george']
        },
        {
            'display_name': 'St. Paul',
            'broken_url': 'https://dollarfence.com/locations/minnesota/st.-paul/',
            'state': 'minnesota',
            'city': 'saint-paul',
            'variations': ['st-paul', 'st.-paul', 'saint-paul']
        },
        {
            'display_name': 'St. Louis',
            'broken_url': 'https://dollarfence.com/locations/missouri/st.-louis/',
            'state': 'missouri',
            'city': 'st-louis',
            'variations': ['st-louis', 'st.-louis', 'saint-louis']
        },
        {
            'display_name': 'St. Johns',
            'broken_url': 'https://dollarfence.com/locations/florida/st.-johns/',
            'state': 'florida',
            'city': 'st-johns',
            'variations': ['st-johns', 'st.-johns']
        },
        {
            'display_name': 'St. Petersburg',
            'broken_url': 'https://dollarfence.com/locations/florida/st.-petersburg/',
            'state': 'florida',
            'city': 'st-petersburg',
            'variations': ['st-petersburg', 'st.-petersburg']
        },
        {
            'display_name': 'Sandy Springs',
            'broken_url': 'https://dollarfence.com/locations/georgia/Sandy Springs/',
            'state': 'georgia',
            'city': 'sandy-springs',
            'variations': ['sandy-springs', 'Sandy Springs']
        }
    ]
    
    return broken_links

def map_broken_to_existing(broken_links, existing_pages):
    """Map broken links to existing working alternatives"""
    
    mapping = {
        'has_alternative': [],
        'needs_creation': []
    }
    
    print("=== MAPPING BROKEN LINKS TO ALTERNATIVES ===")
    
    for broken in broken_links:
        found_alternative = False
        
        # Look for existing pages that match this location
        for existing in existing_pages:
            # Check if state matches and city matches any variation
            if (existing['state'] == broken['state'] and 
                existing['city'] in broken['variations']):
                
                mapping['has_alternative'].append({
                    'display_name': broken['display_name'],
                    'broken_url': broken['broken_url'],
                    'working_url': existing['full_url'],
                    'working_file': existing['file_path'],
                    'state': broken['state'],
                    'city': existing['city']
                })
                
                print(f"✅ FOUND ALTERNATIVE: {broken['display_name']}")
                print(f"   Broken: {broken['broken_url']}")
                print(f"   Working: {existing['full_url']}")
                print()
                
                found_alternative = True
                break
        
        if not found_alternative:
            mapping['needs_creation'].append({
                'display_name': broken['display_name'],
                'broken_url': broken['broken_url'],
                'state': broken['state'],
                'city': broken['city'],
                'variations': broken['variations']
            })
            
            print(f"❌ NEEDS CREATION: {broken['display_name']}")
            print(f"   Broken: {broken['broken_url']}")
            print(f"   State: {broken['state']}")
            print(f"   City: {broken['city']}")
            print()
    
    return mapping

def generate_mapping_report(mapping):
    """Generate a comprehensive mapping report"""
    
    print(f"\n=== MAPPING SUMMARY ===")
    print(f"Broken links with alternatives: {len(mapping['has_alternative'])}")
    print(f"Broken links needing creation: {len(mapping['needs_creation'])}")
    
    if mapping['has_alternative']:
        print(f"\n=== LINKS WITH WORKING ALTERNATIVES ===")
        for item in mapping['has_alternative']:
            print(f"• {item['display_name']} → {item['working_url']}")
    
    if mapping['needs_creation']:
        print(f"\n=== PAGES THAT NEED TO BE CREATED ===")
        for item in mapping['needs_creation']:
            print(f"• {item['display_name']} ({item['state']}/{item['city']})")
    
    # Save mapping to JSON for later use
    with open('broken_link_mapping.json', 'w') as f:
        json.dump(mapping, f, indent=2)
    
    print(f"\n📄 Mapping saved to: broken_link_mapping.json")
    
    return mapping

def main():
    print("Starting broken link mapping process...")
    
    # Change to website directory
    os.chdir('/home/ubuntu/dollar-fence-website')
    
    # Get existing location pages
    existing_pages = get_existing_location_pages()
    print(f"Found {len(existing_pages)} existing location pages")
    
    # Identify broken links
    broken_links = identify_broken_links()
    print(f"Identified {len(broken_links)} broken links to map")
    
    # Map broken links to existing alternatives
    mapping = map_broken_to_existing(broken_links, existing_pages)
    
    # Generate comprehensive report
    generate_mapping_report(mapping)
    
    return mapping

if __name__ == "__main__":
    mapping = main()

