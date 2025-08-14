#!/usr/bin/env python3
"""
Generate complete location pages by properly duplicating the full Birmingham page
with all content, images, and functionality preserved.
"""

import os
import re
import json
from pathlib import Path

def load_location_data():
    """Load all location data from the JSON file"""
    with open('/home/ubuntu/all_locations.json', 'r') as f:
        return json.load(f)

def get_county_for_city(city, state):
    """Get county information for a city"""
    county_map = {
        # Alabama
        ("Birmingham", "Alabama"): "Jefferson County",
        ("Huntsville", "Alabama"): "Madison County", 
        ("Montgomery", "Alabama"): "Montgomery County",
        
        # California
        ("Los Angeles", "California"): "Los Angeles County",
        ("San Diego", "California"): "San Diego County",
        ("San Francisco", "California"): "San Francisco County",
        ("San Jose", "California"): "Santa Clara County",
        ("Fresno", "California"): "Fresno County",
        ("Sacramento", "California"): "Sacramento County",
        ("Long Beach", "California"): "Los Angeles County",
        ("Oakland", "California"): "Alameda County",
        ("Bakersfield", "California"): "Kern County",
        ("Anaheim", "California"): "Orange County",
        ("Santa Ana", "California"): "Orange County",
        ("Riverside", "California"): "Riverside County",
        ("Stockton", "California"): "San Joaquin County",
        ("Irvine", "California"): "Orange County",
        ("Chula Vista", "California"): "San Diego County",
        
        # Florida
        ("Jacksonville", "Florida"): "Duval County",
        ("Miami", "Florida"): "Miami-Dade County",
        ("Tampa", "Florida"): "Hillsborough County",
        ("Orlando", "Florida"): "Orange County",
        ("St. Petersburg", "Florida"): "Pinellas County",
        ("Hialeah", "Florida"): "Miami-Dade County",
        ("Tallahassee", "Florida"): "Leon County",
        ("Fort Lauderdale", "Florida"): "Broward County",
        ("Port St. Lucie", "Florida"): "St. Lucie County",
        ("Cape Coral", "Florida"): "Lee County",
        
        # Georgia
        ("Atlanta", "Georgia"): "Fulton County",
        ("Augusta", "Georgia"): "Richmond County",
        ("Columbus", "Georgia"): "Muscogee County",
        ("Savannah", "Georgia"): "Chatham County",
        ("Athens-Clarke County", "Georgia"): "Clarke County",
        ("Macon-Bibb County", "Georgia"): "Bibb County",
        ("Roswell", "Georgia"): "Fulton County",
        ("Albany", "Georgia"): "Dougherty County",
        ("Marietta", "Georgia"): "Cobb County",
        ("Warner Robins", "Georgia"): "Houston County",
        
        # Texas
        ("Houston", "Texas"): "Harris County",
        ("San Antonio", "Texas"): "Bexar County",
        ("Dallas", "Texas"): "Dallas County",
        ("Austin", "Texas"): "Travis County",
        ("Fort Worth", "Texas"): "Tarrant County",
        ("El Paso", "Texas"): "El Paso County",
        ("Arlington", "Texas"): "Tarrant County",
        ("Corpus Christi", "Texas"): "Nueces County",
        ("Plano", "Texas"): "Collin County",
        ("Lubbock", "Texas"): "Lubbock County",
    }
    
    return county_map.get((city, state), f"{city} County")

def generate_location_page(city, state, template_content):
    """Generate a complete location page by properly replacing Birmingham content"""
    
    # Get county information
    county = get_county_for_city(city, state)
    
    # Create URL-safe city name
    city_slug = city.lower().replace(' ', '-').replace('.', '').replace(',', '').replace('&', 'and')
    state_slug = state.lower().replace(' ', '-')
    
    # Replace all Birmingham references with the new city
    content = template_content
    
    # Title and meta description replacements
    content = re.sub(r'Birmingham, Alabama', f'{city}, {state}', content)
    content = re.sub(r'Birmingham\'s #1', f'{city}\'s #1', content)
    content = re.sub(r'Birmingham, Hoover & Jefferson County', f'{city} & {county}', content)
    content = re.sub(r'Birmingham and the surrounding Alabama areas', f'{city} and the surrounding {state} areas', content)
    content = re.sub(r'throughout Jefferson County', f'throughout {county}', content)
    
    # URL replacements
    content = re.sub(r'/locations/alabama/birmingham/', f'/locations/{state_slug}/{city_slug}/', content)
    
    # Content body replacements
    content = re.sub(r'Birmingham fence company', f'{city} fence company', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham fence installation', f'{city} fence installation', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham fence contractor', f'{city} fence contractor', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham fence builder', f'{city} fence builder', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham customers', f'{city} customers', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham residents', f'{city} residents', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham homeowners', f'{city} homeowners', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham businesses', f'{city} businesses', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham area', f'{city} area', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham property', f'{city} property', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham properties', f'{city} properties', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham yard', f'{city} yard', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham pool area', f'{city} pool area', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham fence project', f'{city} fence project', content, flags=re.IGNORECASE)
    content = re.sub(r'Birmingham fences', f'{city} fences', content, flags=re.IGNORECASE)
    content = re.sub(r'in Birmingham', f'in {city}', content, flags=re.IGNORECASE)
    content = re.sub(r'for Birmingham', f'for {city}', content, flags=re.IGNORECASE)
    content = re.sub(r'throughout Birmingham', f'throughout {city}', content, flags=re.IGNORECASE)
    content = re.sub(r'around Birmingham', f'around {city}', content, flags=re.IGNORECASE)
    
    # State-specific replacements
    content = re.sub(r'Alabama\'s weather', f'{state}\'s weather', content, flags=re.IGNORECASE)
    content = re.sub(r'Alabama\'s climate', f'{state}\'s climate', content, flags=re.IGNORECASE)
    content = re.sub(r'across Alabama', f'across {state}', content, flags=re.IGNORECASE)
    content = re.sub(r'throughout Alabama', f'throughout {state}', content, flags=re.IGNORECASE)
    
    # Schema markup replacements
    content = re.sub(r'"name": "Dollar Fence Birmingham"', f'"name": "Dollar Fence {city}"', content)
    content = re.sub(r'"addressLocality": "Birmingham"', f'"addressLocality": "{city}"', content)
    content = re.sub(r'"addressRegion": "Alabama"', f'"addressRegion": "{state}"', content)
    content = re.sub(r'Professional fence installation and repair services in Birmingham, Alabama', 
                    f'Professional fence installation and repair services in {city}, {state}', content)
    
    # Update coordinates for major cities (simplified - you could expand this)
    coordinates = {
        ("Los Angeles", "California"): ("34.0522", "-118.2437"),
        ("San Diego", "California"): ("32.7157", "-117.1611"),
        ("San Francisco", "California"): ("37.7749", "-122.4194"),
        ("Atlanta", "Georgia"): ("33.7490", "-84.3880"),
        ("Houston", "Texas"): ("29.7604", "-95.3698"),
        ("Dallas", "Texas"): ("32.7767", "-96.7970"),
        ("Miami", "Florida"): ("25.7617", "-80.1918"),
        ("Orlando", "Florida"): ("28.5383", "-81.3792"),
    }
    
    if (city, state) in coordinates:
        lat, lng = coordinates[(city, state)]
        content = re.sub(r'"latitude": 33\.5186', f'"latitude": {lat}', content)
        content = re.sub(r'"longitude": -86\.8104', f'"longitude": {lng}', content)
    
    # Update testimonial locations (keep the testimonials but update the location references)
    content = re.sub(r'Vestavia Hills, Alabama', f'Vestavia Hills, {state}', content)
    content = re.sub(r'Hoover, Alabama', f'Hoover, {state}', content)
    content = re.sub(r'Mountain Brook, Alabama', f'Mountain Brook, {state}', content)
    content = re.sub(r'Alabama\'s weather', f'{state}\'s weather', content)
    content = re.sub(r'the Birmingham area', f'the {city} area', content)
    
    # Update local codes reference
    content = re.sub(r'Birmingham\'s local codes', f'{city}\'s local codes', content)
    
    return content

def create_location_page(city, state, template_content):
    """Create directory structure and write the location page"""
    
    # Create URL-safe names
    city_slug = city.lower().replace(' ', '-').replace('.', '').replace(',', '').replace('&', 'and')
    state_slug = state.lower().replace(' ', '-')
    
    # Create directory path
    location_dir = Path(f'/home/ubuntu/dollar-fence-website/locations/{state_slug}/{city_slug}')
    location_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate the page content
    page_content = generate_location_page(city, state, template_content)
    
    # Write the page
    page_path = location_dir / 'index.html'
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(page_content)
    
    return str(page_path)

def main():
    """Main function to generate all location pages"""
    
    # Read the Birmingham template
    template_path = '/home/ubuntu/dollar-fence-website/locations/alabama/birmingham/index.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    print(f"Loaded Birmingham template: {len(template_content)} characters")
    
    # Load location data
    locations = load_location_data()
    print(f"Loaded {len(locations)} locations")
    
    # Generate pages for all locations
    generated_count = 0
    failed_locations = []
    
    for location in locations:
        try:
            city = location['city']
            state = location['state']
            
            # Skip Birmingham since it's already the template
            if city == "Birmingham" and state == "Alabama":
                print(f"Skipping Birmingham, Alabama (template)")
                continue
            
            # Generate the page
            page_path = create_location_page(city, state, template_content)
            generated_count += 1
            
            if generated_count % 50 == 0:
                print(f"Generated {generated_count} pages...")
            
        except Exception as e:
            print(f"Failed to generate page for {city}, {state}: {str(e)}")
            failed_locations.append(f"{city}, {state}")
    
    print(f"\n=== GENERATION COMPLETE ===")
    print(f"Successfully generated: {generated_count} pages")
    print(f"Failed: {len(failed_locations)} pages")
    
    if failed_locations:
        print(f"Failed locations: {failed_locations}")
    
    return generated_count, failed_locations

if __name__ == "__main__":
    generated, failed = main()
    print(f"\nFinal result: {generated} pages generated, {len(failed)} failed")

