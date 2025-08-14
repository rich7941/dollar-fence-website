#!/usr/bin/env python3
"""
Create Missing Location Pages
Uses the existing location page generation system to create the 6 missing pages
"""

import os
import json
import shutil
from generate_location_page import generate_location_page

def load_missing_pages():
    """Load the list of pages that need to be created"""
    
    with open('broken_link_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    return mapping['needs_creation']

def create_missing_location_pages(missing_pages):
    """Create the missing location pages using the automated system"""
    
    print("=== CREATING MISSING LOCATION PAGES ===")
    
    created_pages = []
    errors = []
    
    for page in missing_pages:
        display_name = page['display_name']
        state = page['state']
        city = page['city']
        
        print(f"\n🔧 Creating: {display_name}")
        print(f"   State: {state}")
        print(f"   City: {city}")
        
        # Convert to proper format for generation
        # Map state URL to proper state name
        state_name_map = {
            'florida': 'Florida',
            'new-jersey': 'New Jersey',
            'utah': 'Utah', 
            'minnesota': 'Minnesota',
            'missouri': 'Missouri'
        }
        
        # Map city URL to proper city name
        city_name_map = {
            'port-st-lucie': 'Port St. Lucie',
            'hamilton-township': 'Hamilton Township',
            'st-george': 'St. George',
            'saint-paul': 'St. Paul',
            'st-louis': 'St. Louis',
            'st-johns': 'St. Johns'
        }
        
        state_name = state_name_map.get(state, state.title())
        city_name = city_name_map.get(city, city.replace('-', ' ').title())
        
        location_string = f"{city_name}, {state_name}"
        
        try:
            # Generate the page using the existing system
            result = generate_location_page(location_string)
            
            if result.get('success'):
                # Move the generated page to the correct location in the website
                source_path = result['file_path']
                target_dir = f"locations/{state}/{city}"
                target_path = f"{target_dir}/index.html"
                
                # Create target directory
                os.makedirs(target_dir, exist_ok=True)
                
                # Copy the generated file
                shutil.copy2(source_path, target_path)
                
                created_pages.append({
                    'display_name': display_name,
                    'location_string': location_string,
                    'file_path': target_path,
                    'url_path': f"/locations/{state}/{city}/",
                    'full_url': f"https://dollarfence.com/locations/{state}/{city}/"
                })
                
                print(f"   ✅ Created: {target_path}")
                print(f"   🌐 URL: https://dollarfence.com/locations/{state}/{city}/")
                
            else:
                error_msg = result.get('error', 'Unknown error')
                errors.append({
                    'display_name': display_name,
                    'location_string': location_string,
                    'error': error_msg
                })
                print(f"   ❌ Failed: {error_msg}")
                
        except Exception as e:
            errors.append({
                'display_name': display_name,
                'location_string': location_string,
                'error': str(e)
            })
            print(f"   ❌ Exception: {str(e)}")
    
    return created_pages, errors

def update_sitemap_with_new_pages(created_pages):
    """Add the new pages to the sitemap"""
    
    print(f"\n=== UPDATING SITEMAP ===")
    
    if not created_pages:
        print("No new pages to add to sitemap")
        return
    
    try:
        # Read current sitemap
        with open('sitemap.xml', 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        
        # Find the closing </urlset> tag
        closing_tag = '</ns0:urlset>'
        if closing_tag not in sitemap_content:
            closing_tag = '</urlset>'
        
        if closing_tag in sitemap_content:
            # Create new URL entries
            new_entries = []
            for page in created_pages:
                url_entry = f"""  <ns0:url>
    <ns0:loc>{page['full_url']}</ns0:loc>
    <ns0:lastmod>2025-08-14</ns0:lastmod>
    <ns0:changefreq>weekly</ns0:changefreq>
    <ns0:priority>0.8</ns0:priority>
  </ns0:url>"""
                new_entries.append(url_entry)
            
            # Insert new entries before closing tag
            new_sitemap = sitemap_content.replace(
                closing_tag,
                '\n'.join(new_entries) + f'\n{closing_tag}'
            )
            
            # Write updated sitemap
            with open('sitemap.xml', 'w', encoding='utf-8') as f:
                f.write(new_sitemap)
            
            print(f"✅ Added {len(created_pages)} new URLs to sitemap")
            
        else:
            print("❌ Could not find closing tag in sitemap")
            
    except Exception as e:
        print(f"❌ Error updating sitemap: {str(e)}")

def generate_creation_report(created_pages, errors):
    """Generate a comprehensive creation report"""
    
    print(f"\n=== CREATION SUMMARY ===")
    print(f"Pages successfully created: {len(created_pages)}")
    print(f"Errors encountered: {len(errors)}")
    
    if created_pages:
        print(f"\n=== SUCCESSFULLY CREATED PAGES ===")
        for page in created_pages:
            print(f"✅ {page['display_name']}")
            print(f"   File: {page['file_path']}")
            print(f"   URL: {page['full_url']}")
    
    if errors:
        print(f"\n=== ERRORS ===")
        for error in errors:
            print(f"❌ {error['display_name']}")
            print(f"   Location: {error['location_string']}")
            print(f"   Error: {error['error']}")
    
    # Save report to JSON
    report = {
        'created_pages': created_pages,
        'errors': errors,
        'summary': {
            'total_requested': len(created_pages) + len(errors),
            'successful': len(created_pages),
            'failed': len(errors)
        }
    }
    
    with open('page_creation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: page_creation_report.json")
    
    return report

def main():
    print("Starting missing page creation process...")
    
    # Change to website directory
    os.chdir('/home/ubuntu/dollar-fence-website')
    
    # Load the list of missing pages
    missing_pages = load_missing_pages()
    print(f"Found {len(missing_pages)} pages to create")
    
    # Create the missing pages
    created_pages, errors = create_missing_location_pages(missing_pages)
    
    # Update sitemap with new pages
    if created_pages:
        update_sitemap_with_new_pages(created_pages)
    
    # Generate comprehensive report
    report = generate_creation_report(created_pages, errors)
    
    return report

if __name__ == "__main__":
    report = main()

