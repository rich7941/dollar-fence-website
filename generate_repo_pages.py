#!/usr/bin/env python3
"""
Script to generate location pages directly in the repository structure
This will create pages in the locations/ directory for deployment
"""

import os
import re
import json
from pathlib import Path

def get_county_info(city, state):
    """Get county information for major cities"""
    county_map = {
        # Alabama
        "Birmingham": "Jefferson County",
        "Huntsville": "Madison County", 
        "Montgomery": "Montgomery County",
        "Mobile": "Mobile County",
        
        # California
        "Los Angeles": "Los Angeles County",
        "San Diego": "San Diego County",
        "San Francisco": "San Francisco County",
        "Sacramento": "Sacramento County",
        "Oakland": "Alameda County",
        "Fresno": "Fresno County",
        "Long Beach": "Los Angeles County",
        "Anaheim": "Orange County",
        "Santa Ana": "Orange County",
        "Riverside": "Riverside County",
        "Stockton": "San Joaquin County",
        "Irvine": "Orange County",
        "Chula Vista": "San Diego County",
        "Bakersfield": "Kern County",
        "San Jose": "Santa Clara County",
        
        # Florida
        "Jacksonville": "Duval County",
        "Miami": "Miami-Dade County",
        "Tampa": "Hillsborough County",
        "Orlando": "Orange County",
        "St. Petersburg": "Pinellas County",
        "Hialeah": "Miami-Dade County",
        "Tallahassee": "Leon County",
        "Fort Lauderdale": "Broward County",
        "Port St. Lucie": "St. Lucie County",
        "Cape Coral": "Lee County",
        "Hollywood": "Broward County",
        "Gainesville": "Alachua County",
        "Miramar": "Broward County",
        "Coral Springs": "Broward County",
        "Clearwater": "Pinellas County",
        "Palm Bay": "Brevard County",
        "West Palm Beach": "Palm Beach County",
        "Lakeland": "Polk County",
        "Pompano Beach": "Broward County",
        "Davie": "Broward County",
        
        # Texas
        "Houston": "Harris County",
        "San Antonio": "Bexar County", 
        "Dallas": "Dallas County",
        "Austin": "Travis County",
        "Fort Worth": "Tarrant County",
        "El Paso": "El Paso County",
        "Arlington": "Tarrant County",
        "Corpus Christi": "Nueces County",
        "Plano": "Collin County",
        "Lubbock": "Lubbock County",
        "Laredo": "Webb County",
        "Irving": "Dallas County",
        "Garland": "Dallas County",
        "Frisco": "Collin County",
        "McKinney": "Collin County",
        "Grand Prairie": "Dallas County",
        "Mesquite": "Dallas County",
        "Killeen": "Bell County",
        "Denton": "Denton County",
        "Midland": "Midland County",
        "Abilene": "Taylor County",
        "Beaumont": "Jefferson County",
        "Round Rock": "Williamson County",
        "Richardson": "Dallas County",
        "Pearland": "Brazoria County",
        "League City": "Galveston County",
        "Sugar Land": "Fort Bend County",
        "Tyler": "Smith County",
        "College Station": "Brazos County",
        "Waco": "McLennan County",
        "Brownsville": "Cameron County",
        "Odessa": "Ector County",
        "Pasadena": "Harris County",
        "Lewisville": "Denton County",
        "Allen": "Collin County",
        "Carrollton": "Dallas County",
        "Amarillo": "Potter County",
        "Wichita Falls": "Wichita County",
        
        # Georgia
        "Atlanta": "Fulton County",
        "Augusta": "Richmond County",
        "Columbus": "Muscogee County",
        "Savannah": "Chatham County",
        "Athens-Clarke County": "Clarke County",
        "Sandy Springs": "Fulton County",
        "Roswell": "Fulton County",
        "Johns Creek": "Fulton County",
        "Albany": "Dougherty County",
        "Warner Robins": "Houston County",
        "Alpharetta": "Fulton County",
        "Marietta": "Cobb County",
        "Valdosta": "Lowndes County",
        "Smyrna": "Cobb County",
        "Dunwoody": "DeKalb County",
        
        "Lakewood": "Ocean County",
        # Add more as needed - this covers major cities
    }
    
    return county_map.get(city, f"{city} County")

def generate_location_page(location_input):
    """Generate a complete HTML page for a specific location in the repository"""
    
    # Parse the location input (format: "City, State")
    try:
        city, state = location_input.strip().split(', ')
    except ValueError:
        return {"error": f"Invalid location format: {location_input}"}
    
    # Create URL-friendly versions
    state_url = state.lower().replace(' ', '-').replace('&', 'and')
    city_url = city.lower().replace(' ', '-').replace('&', 'and').replace('.', '').replace("'", '').replace('(', '').replace(')', '')
    
    # Get county information
    county = get_county_info(city, state)
    
    # Read the Birmingham template from the repository
    template_path = "locations/alabama/birmingham/index.html"
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        return {"error": f"Template file not found: {template_path}"}
    
    # Replace all Birmingham-specific content with the new location
    content = template_content
    
    # Title and meta descriptions
    content = content.replace(
        "Fence Company Birmingham, Alabama | Vinyl, Wood & Aluminum Fencing | Dollar Fence",
        f"Fence Company {city}, {state} | Vinyl, Wood & Aluminum Fencing | Dollar Fence"
    )
    
    content = content.replace(
        "Birmingham's #1 fence company. Professional vinyl, wood & aluminum fence installation. Free quotes, 96% satisfaction rate. Serving Birmingham, Hoover & Jefferson County.",
        f"{city}'s #1 fence company. Professional vinyl, wood & aluminum fence installation. Free quotes, 96% satisfaction rate. Serving {city} and {county}."
    )
    
    # Canonical URL
    content = content.replace(
        "https://dollarfence.com/locations/alabama/birmingham/",
        f"https://dollarfence.com/locations/{state_url}/{city_url}/"
    )
    
    # Schema markup - Local Business
    content = content.replace('"name": "Dollar Fence Birmingham"', f'"name": "Dollar Fence {city}"')
    content = content.replace('"addressLocality": "Birmingham"', f'"addressLocality": "{city}"')
    content = content.replace('"addressRegion": "Alabama"', f'"addressRegion": "{state}"')
    content = content.replace('"url": "https://dollarfence.com/locations/alabama/birmingham/"', f'"url": "https://dollarfence.com/locations/{state_url}/{city_url}/"')
    
    # Update coordinates (approximate - in real implementation you'd use a geocoding service)
    # For now, we'll use generic coordinates
    content = content.replace('"latitude": 33.5186', '"latitude": 39.8283')
    content = content.replace('"longitude": -86.8104', '"longitude": -98.5795')
    
    # Main content replacements
    content = content.replace("Birmingham", city)
    content = content.replace("Alabama", state)
    content = content.replace("Jefferson County", county)
    
    # Handle specific cases where we don't want to replace state names in certain contexts
    # This is a simplified approach - in production you'd want more sophisticated text processing
    
    # Hero section
    content = re.sub(
        r'<h1[^>]*>Fence Company Birmingham, Alabama</h1>',
        f'<h1>Fence Company {city}, {state}</h1>',
        content
    )
    
    content = re.sub(
        r'Professional fence installation and repair services for residential and commercial properties in Birmingham, Alabama\.',
        f'Professional fence installation and repair services for residential and commercial properties in {city}, {state}.',
        content
    )
    
    # Update all instances of "Birmingham fence company" to "{city} fence company"
    content = re.sub(r'\bBirmingham fence company\b', f'{city} fence company', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham fence contractor\b', f'{city} fence contractor', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham customers\b', f'{city} customers', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham properties\b', f'{city} properties', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham area\b', f'{city} area', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham homes\b', f'{city} homes', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham property\b', f'{city} property', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham pool area\b', f'{city} pool area', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham yard\b', f'{city} yard', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham gardens\b', f'{city} gardens', content, flags=re.IGNORECASE)
    content = re.sub(r'\bBirmingham fence project\b', f'{city} fence project', content, flags=re.IGNORECASE)
    content = re.sub(r'\bin Birmingham\b', f'in {city}', content, flags=re.IGNORECASE)
    content = re.sub(r'\bthroughout Birmingham\b', f'throughout {city}', content, flags=re.IGNORECASE)
    content = re.sub(r'\baround Birmingham\b', f'around {city}', content, flags=re.IGNORECASE)
    
    # FAQ section updates
    content = re.sub(
        r'How much does fence installation cost in Birmingham\?',
        f'How much does fence installation cost in {city}?',
        content
    )
    
    content = re.sub(
        r'Fence installation costs in Birmingham vary by material',
        f'Fence installation costs in {city} vary by material',
        content
    )
    
    content = re.sub(
        r'What types of fences do you install in Birmingham\?',
        f'What types of fences do you install in {city}?',
        content
    )
    
    content = re.sub(
        r'throughout Birmingham, Hoover, Vestavia Hills, Mountain Brook, and Jefferson County',
        f'throughout {city} and {county}',
        content
    )
    
    content = re.sub(
        r'How long does fence installation take in Birmingham\?',
        f'How long does fence installation take in {city}?',
        content
    )
    
    content = re.sub(
        r'Most residential fence installations in Birmingham take',
        f'Most residential fence installations in {city} take',
        content
    )
    
    content = re.sub(
        r'Do you offer financing for fence installation in Birmingham\?',
        f'Do you offer financing for fence installation in {city}?',
        content
    )
    
    # Create the directory structure in the repository
    output_dir = f"locations/{state_url}/{city_url}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Write the HTML file
    output_file = os.path.join(output_dir, "index.html")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        return {"error": f"Failed to write file {output_file}: {str(e)}"}
    
    return {
        "success": True,
        "location": f"{city}, {state}",
        "file_path": output_file,
        "url_path": f"/locations/{state_url}/{city_url}/",
        "county": county
    }

def main():
    """Main function for testing"""
    import sys
    if len(sys.argv) > 1:
        location = sys.argv[1]
        result = generate_location_page(location)
        print(json.dumps(result, indent=2))
    else:
        # Test with a sample location
        result = generate_location_page("Atlanta, Georgia")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

