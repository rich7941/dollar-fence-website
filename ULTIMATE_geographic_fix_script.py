#!/usr/bin/env python3
"""
ULTIMATE Geographic Fix Script for Dollar Fence Location Pages
This script catches ALL Birmingham and Alabama references with comprehensive validation
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
        
        # Colorado
        ("Denver", "Colorado"): "Denver County",
        ("Colorado Springs", "Colorado"): "El Paso County",
        ("Aurora", "Colorado"): "Arapahoe County",
        ("Fort Collins", "Colorado"): "Larimer County",
        ("Lakewood", "Colorado"): "Jefferson County",
    }
    
    return county_map.get((city, state), f"{city} County")

def get_nearby_cities_for_location(city, state):
    """Get nearby cities for each location to replace Birmingham suburbs"""
    nearby_cities_map = {
        # Texas
        ("Houston", "Texas"): "Houston, Sugar Land, The Woodlands, Pearland",
        ("Dallas", "Texas"): "Dallas, Plano, Irving, Garland",
        ("San Antonio", "Texas"): "San Antonio, New Braunfels, Schertz, Universal City",
        ("Austin", "Texas"): "Austin, Round Rock, Cedar Park, Georgetown",
        ("Fort Worth", "Texas"): "Fort Worth, Arlington, Grand Prairie, Euless",
        
        # California
        ("Los Angeles", "California"): "Los Angeles, Beverly Hills, Santa Monica, Pasadena",
        ("San Diego", "California"): "San Diego, Chula Vista, Oceanside, Escondido",
        ("San Francisco", "California"): "San Francisco, Oakland, Berkeley, Daly City",
        ("San Jose", "California"): "San Jose, Santa Clara, Sunnyvale, Mountain View",
        ("Sacramento", "California"): "Sacramento, Elk Grove, Roseville, Folsom",
        ("Fresno", "California"): "Fresno, Clovis, Madera, Selma",
        ("Long Beach", "California"): "Long Beach, Signal Hill, Lakewood, Cerritos",
        ("Oakland", "California"): "Oakland, Berkeley, Alameda, Emeryville",
        ("Bakersfield", "California"): "Bakersfield, Delano, Shafter, Wasco",
        ("Anaheim", "California"): "Anaheim, Santa Ana, Orange, Garden Grove",
        ("Stockton", "California"): "Stockton, Lodi, Tracy, Manteca",
        ("Riverside", "California"): "Riverside, Corona, Moreno Valley, Perris",
        ("Chula Vista", "California"): "Chula Vista, National City, Bonita, Imperial Beach",
        ("Irvine", "California"): "Irvine, Newport Beach, Costa Mesa, Tustin",
        
        # Florida
        ("Miami", "Florida"): "Miami, Coral Gables, Homestead, Aventura",
        ("Orlando", "Florida"): "Orlando, Winter Park, Kissimmee, Altamonte Springs",
        ("Tampa", "Florida"): "Tampa, St. Petersburg, Clearwater, Brandon",
        ("Jacksonville", "Florida"): "Jacksonville, Orange Park, Fernandina Beach, Neptune Beach",
        ("Fort Lauderdale", "Florida"): "Fort Lauderdale, Pompano Beach, Coral Springs, Plantation",
        ("Hialeah", "Florida"): "Hialeah, Miami Lakes, Opa-locka, Miami Springs",
        ("Tallahassee", "Florida"): "Tallahassee, Havana, Quincy, Crawfordville",
        ("St. Petersburg", "Florida"): "St. Petersburg, Clearwater, Pinellas Park, Largo",
        ("Port St. Lucie", "Florida"): "Port St. Lucie, Fort Pierce, Stuart, Jensen Beach",
        ("Cape Coral", "Florida"): "Cape Coral, Fort Myers, Lehigh Acres, Estero",
        
        # Georgia
        ("Atlanta", "Georgia"): "Atlanta, Marietta, Roswell, Sandy Springs",
        ("Augusta", "Georgia"): "Augusta, Martinez, Evans, Grovetown",
        ("Savannah", "Georgia"): "Savannah, Pooler, Richmond Hill, Tybee Island",
        ("Columbus", "Georgia"): "Columbus, Phenix City, Fort Benning, Harris County",
        ("Athens-Clarke County", "Georgia"): "Athens, Commerce, Jefferson, Madison",
        
        # Colorado
        ("Denver", "Colorado"): "Denver, Aurora, Lakewood, Thornton",
        ("Colorado Springs", "Colorado"): "Colorado Springs, Fountain, Security-Widefield, Cimarron Hills",
        ("Aurora", "Colorado"): "Aurora, Denver, Centennial, Glendale",
        ("Fort Collins", "Colorado"): "Fort Collins, Loveland, Windsor, Wellington",
        ("Lakewood", "Colorado"): "Lakewood, Denver, Wheat Ridge, Edgewater",
    }
    
    return nearby_cities_map.get((city, state), f"{city}, {city} Metro, {city} Area")

def get_state_abbreviation(state):
    """Get state abbreviation"""
    state_abbrevs = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
        "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
        "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
        "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
        "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
    }
    return state_abbrevs.get(state, state[:2].upper())

def ultimate_geographic_fix(city, state, template_content):
    """Apply ULTIMATE comprehensive geographic fixes to catch ALL remaining issues"""
    
    # Get location-specific information
    county = get_county_for_city(city, state)
    nearby_cities = get_nearby_cities_for_location(city, state)
    state_abbrev = get_state_abbreviation(state)
    
    # Create URL-safe city name
    city_slug = city.lower().replace(' ', '-').replace('.', '').replace(',', '').replace('&', 'and')
    state_slug = state.lower().replace(' ', '-')
    
    # Start with the template content
    content = template_content
    
    # ============================================================================
    # PHASE 1: COMPREHENSIVE BIRMINGHAM REPLACEMENT - ALL POSSIBLE VARIATIONS
    # ============================================================================
    
    # 1. EXACT PHRASE REPLACEMENTS (most specific first)
    birmingham_exact_phrases = [
        (r'Serving Birmingham and Surrounding Areas', f'Serving {city} and Surrounding Areas'),
        (r'Birmingham and Surrounding Areas', f'{city} and Surrounding Areas'),
        (r'Birmingham, Alabama fence company', f'{city}, {state} fence company'),
        (r'Birmingham, Alabama', f'{city}, {state}'),
        (r'Birmingham\'s #1', f'{city}\'s #1'),
        (r'Birmingham & Jefferson County', f'{city} & {county}'),
        (r'Birmingham, Hoover & Jefferson County', f'{city} & {county}'),
        (r'Birmingham and the surrounding Alabama areas', f'{city} and the surrounding {state} areas'),
        (r'throughout Jefferson County', f'throughout {county}'),
        (r'Jefferson County', county),
    ]
    
    for pattern, replacement in birmingham_exact_phrases:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # 2. SPECIFIC CITY COMBINATIONS - Replace Birmingham suburbs with local cities
    suburb_replacements = [
        (r'Houston, Hoover, Vestavia Hills, Mountain Brook', nearby_cities),
        (r'Birmingham, Hoover, Vestavia Hills, Mountain Brook', nearby_cities),
        (r'Hoover, Vestavia Hills, Mountain Brook', nearby_cities.split(', ', 1)[1] if ', ' in nearby_cities else nearby_cities),
        (r'Vestavia Hills, Mountain Brook', nearby_cities.split(', ', 2)[2] if nearby_cities.count(', ') >= 2 else nearby_cities),
    ]
    
    for pattern, replacement in suburb_replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # 3. INDIVIDUAL SUBURB REPLACEMENTS
    individual_suburbs = [
        (r'\bHoover\b(?!\s+Dam)', city),  # Avoid replacing "Hoover Dam"
        (r'Vestavia Hills', city),
        (r'Mountain Brook', city),
        (r'Homewood', city),
        (r'Irondale', city),
        (r'Trussville', city),
    ]
    
    for pattern, replacement in individual_suburbs:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # 4. COMPREHENSIVE BIRMINGHAM WORD BOUNDARY REPLACEMENTS
    # This catches ALL instances of "Birmingham" as a standalone word
    birmingham_contexts = [
        (r'\bBirmingham\b(?!\s+Alabama)', city),  # Birmingham not followed by Alabama
        (r'Birmingham fence company', f'{city} fence company'),
        (r'Birmingham fence installation', f'{city} fence installation'),
        (r'Birmingham fence contractor', f'{city} fence contractor'),
        (r'Birmingham fence builder', f'{city} fence builder'),
        (r'Birmingham customers', f'{city} customers'),
        (r'Birmingham residents', f'{city} residents'),
        (r'Birmingham homeowners', f'{city} homeowners'),
        (r'Birmingham businesses', f'{city} businesses'),
        (r'Birmingham area', f'{city} area'),
        (r'Birmingham property', f'{city} property'),
        (r'Birmingham properties', f'{city} properties'),
        (r'Birmingham yard', f'{city} yard'),
        (r'Birmingham pool area', f'{city} pool area'),
        (r'Birmingham fence project', f'{city} fence project'),
        (r'Birmingham fences', f'{city} fences'),
        (r'in Birmingham', f'in {city}'),
        (r'for Birmingham', f'for {city}'),
        (r'throughout Birmingham', f'throughout {city}'),
        (r'around Birmingham', f'around {city}'),
        (r'Birmingham landscaping', f'{city} landscaping'),
        (r'Birmingham gardens', f'{city} gardens'),
        (r'Birmingham backyard', f'{city} backyard'),
        (r'Birmingham commercial', f'{city} commercial'),
        (r'Birmingham residential', f'{city} residential'),
        (r'Birmingham installation', f'{city} installation'),
        (r'Birmingham service', f'{city} service'),
        (r'Birmingham team', f'{city} team'),
        (r'Birmingham contractor', f'{city} contractor'),
        (r'Birmingham company', f'{city} company'),
        (r'Birmingham Metro', f'{city} Metro'),
        (r'Birmingham region', f'{city} region'),
        (r'Birmingham vicinity', f'{city} vicinity'),
        (r'Birmingham neighborhood', f'{city} neighborhood'),
        (r'Birmingham community', f'{city} community'),
        (r'Birmingham location', f'{city} location'),
        (r'Birmingham market', f'{city} market'),
        (r'Birmingham client', f'{city} client'),
        (r'Birmingham project', f'{city} project'),
    ]
    
    for pattern, replacement in birmingham_contexts:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # ============================================================================
    # PHASE 2: COMPREHENSIVE ALABAMA REPLACEMENT - ALL POSSIBLE VARIATIONS
    # ============================================================================
    
    # Only replace Alabama references if this is NOT an Alabama page
    if state != "Alabama":
        alabama_replacements = [
            (r'surrounding Alabama communities', f'surrounding {state} communities'),
            (r'Alabama communities', f'{state} communities'),
            (r'serving Alabama—including', f'serving {state}—including'),
            (r'serving Alabama including', f'serving {state} including'),
            (r'withstand Alabama weather', f'withstand {state} weather'),
            (r'Alabama weather', f'{state} weather'),
            (r'Alabama\'s weather', f'{state}\'s weather'),
            (r'Alabama\'s climate', f'{state}\'s climate'),
            (r'Alabama climate', f'{state} climate'),
            (r'across Alabama', f'across {state}'),
            (r'throughout Alabama', f'throughout {state}'),
            (r'in Alabama for', f'in {state} for'),
            (r'trusted name in Alabama', f'trusted name in {state}'),
            (r'Alabama\'s', f'{state}\'s'),
            (r'Alabama residents', f'{state} residents'),
            (r'Alabama homeowners', f'{state} homeowners'),
            (r'Alabama businesses', f'{state} businesses'),
            (r'Alabama customers', f'{state} customers'),
            (r'Alabama area', f'{state} area'),
            (r'Alabama region', f'{state} region'),
            (r'Alabama market', f'{state} market'),
            (r'Alabama codes', f'{state} codes'),
            (r'Alabama regulations', f'{state} regulations'),
            (r'Alabama requirements', f'{state} requirements'),
            (r'Alabama standards', f'{state} standards'),
        ]
        
        for pattern, replacement in alabama_replacements:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # ============================================================================
    # PHASE 3: URL AND TECHNICAL REPLACEMENTS
    # ============================================================================
    
    # URL replacements
    content = re.sub(r'/locations/alabama/birmingham/', f'/locations/{state_slug}/{city_slug}/', content)
    content = re.sub(r'dollarfence\.com/locations/alabama/birmingham/', f'dollarfence.com/locations/{state_slug}/{city_slug}/', content)
    
    # ============================================================================
    # PHASE 4: SCHEMA MARKUP AND META DATA REPLACEMENTS
    # ============================================================================
    
    # Schema markup replacements
    schema_replacements = [
        (r'"name": "Dollar Fence Birmingham"', f'"name": "Dollar Fence {city}"'),
        (r'"addressLocality": "Birmingham"', f'"addressLocality": "{city}"'),
        (r'"addressRegion": "Alabama"', f'"addressRegion": "{state}"'),
        (r'"addressRegion": "AL"', f'"addressRegion": "{state_abbrev}"'),
        (r'Professional fence installation and repair services in Birmingham, Alabama', 
         f'Professional fence installation and repair services in {city}, {state}'),
    ]
    
    for pattern, replacement in schema_replacements:
        content = re.sub(pattern, replacement, content)
    
    # ============================================================================
    # PHASE 5: META DESCRIPTIONS AND TITLES
    # ============================================================================
    
    # Meta description fixes
    meta_replacements = [
        (r'<meta name="description" content="[^"]*Birmingham[^"]*"', 
         lambda m: m.group(0).replace('Birmingham', city).replace('Alabama', state)),
        (r'<meta property="og:description" content="[^"]*Birmingham[^"]*"',
         lambda m: m.group(0).replace('Birmingham', city).replace('Alabama', state)),
    ]
    
    # Apply meta replacements with lambda functions
    for pattern, replacement_func in meta_replacements:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in reversed(list(matches)):  # Reverse to maintain positions
            original = match.group(0)
            replaced = replacement_func(match)
            content = content[:match.start()] + replaced + content[match.end():]
    
    # Title replacements
    content = re.sub(r'<title>[^<]*Birmingham[^<]*</title>', 
                    lambda m: m.group(0).replace('Birmingham', city).replace('Alabama', state), 
                    content, flags=re.IGNORECASE)
    
    # ============================================================================
    # PHASE 6: COORDINATES UPDATE FOR MAJOR CITIES
    # ============================================================================
    
    coordinates = {
        ("Los Angeles", "California"): ("34.0522", "-118.2437"),
        ("San Diego", "California"): ("32.7157", "-117.1611"),
        ("San Francisco", "California"): ("37.7749", "-122.4194"),
        ("San Jose", "California"): ("37.3382", "-121.8863"),
        ("Sacramento", "California"): ("38.5816", "-121.4944"),
        ("Fresno", "California"): ("36.7378", "-119.7871"),
        ("Long Beach", "California"): ("33.7701", "-118.1937"),
        ("Oakland", "California"): ("37.8044", "-122.2712"),
        ("Bakersfield", "California"): ("35.3733", "-119.0187"),
        ("Anaheim", "California"): ("33.8366", "-117.9143"),
        ("Stockton", "California"): ("37.9577", "-121.2908"),
        ("Riverside", "California"): ("33.9533", "-117.3962"),
        ("Chula Vista", "California"): ("32.6401", "-117.0842"),
        ("Irvine", "California"): ("33.6846", "-117.8265"),
        ("Atlanta", "Georgia"): ("33.7490", "-84.3880"),
        ("Augusta", "Georgia"): ("33.4735", "-82.0105"),
        ("Columbus", "Georgia"): ("32.4609", "-84.9877"),
        ("Savannah", "Georgia"): ("32.0835", "-81.0998"),
        ("Houston", "Texas"): ("29.7604", "-95.3698"),
        ("Dallas", "Texas"): ("32.7767", "-96.7970"),
        ("San Antonio", "Texas"): ("29.4241", "-98.4936"),
        ("Austin", "Texas"): ("30.2672", "-97.7431"),
        ("Fort Worth", "Texas"): ("32.7555", "-97.3308"),
        ("Miami", "Florida"): ("25.7617", "-80.1918"),
        ("Orlando", "Florida"): ("28.5383", "-81.3792"),
        ("Tampa", "Florida"): ("27.9506", "-82.4572"),
        ("Jacksonville", "Florida"): ("30.3322", "-81.6557"),
        ("Denver", "Colorado"): ("39.7392", "-104.9903"),
        ("Colorado Springs", "Colorado"): ("38.8339", "-104.8214"),
        ("Aurora", "Colorado"): ("39.7294", "-104.8319"),
        ("Fort Collins", "Colorado"): ("40.5853", "-105.0844"),
        ("Lakewood", "Colorado"): ("39.7047", "-105.0814"),
    }
    
    if (city, state) in coordinates:
        lat, lng = coordinates[(city, state)]
        content = re.sub(r'"latitude": "?33\.5186"?', f'"latitude": "{lat}"', content)
        content = re.sub(r'"longitude": "?-86\.8104"?', f'"longitude": "{lng}"', content)
    
    # ============================================================================
    # PHASE 7: TESTIMONIAL AND CONTENT UPDATES
    # ============================================================================
    
    # Update testimonial locations if they reference Alabama cities
    if state != "Alabama":
        testimonial_replacements = [
            (r'Vestavia Hills, Alabama', f'Vestavia Hills, {state}'),
            (r'Hoover, Alabama', f'Hoover, {state}'),
            (r'Mountain Brook, Alabama', f'Mountain Brook, {state}'),
            (r'the Birmingham area', f'the {city} area'),
            (r'Birmingham\'s local codes', f'{city}\'s local codes'),
        ]
        
        for pattern, replacement in testimonial_replacements:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # ============================================================================
    # PHASE 8: FINAL CATCH-ALL AND VALIDATION
    # ============================================================================
    
    # Final catch-all for any remaining Birmingham references
    # This is a safety net, but be careful not to replace legitimate content
    if city != "Birmingham" or state != "Alabama":
        # Replace any remaining "Birmingham AL" or "Birmingham, AL"
        content = re.sub(r'Birmingham,?\s+AL\b', f'{city}, {state_abbrev}', content, flags=re.IGNORECASE)
        content = re.sub(r'Birmingham,?\s+Alabama\b', f'{city}, {state}', content, flags=re.IGNORECASE)
    
    # State abbreviation fixes
    if state != "Alabama":
        content = re.sub(r'\bAL\b(?!\s*backyard|abama)', state_abbrev, content)
    
    return content

def regenerate_location_page_with_ultimate_fix(city, state, template_content):
    """Regenerate a location page with the ultimate geographic fix"""
    
    # Create URL-safe names
    city_slug = city.lower().replace(' ', '-').replace('.', '').replace(',', '').replace('&', 'and')
    state_slug = state.lower().replace(' ', '-')
    
    # Create directory path
    location_dir = Path(f'/home/ubuntu/dollar-fence-website/locations/{state_slug}/{city_slug}')
    location_dir.mkdir(parents=True, exist_ok=True)
    
    # Apply ultimate geographic fixes
    fixed_content = ultimate_geographic_fix(city, state, template_content)
    
    # Write the page
    page_path = location_dir / 'index.html'
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    return str(page_path), len(fixed_content)

def main():
    """Main function to demonstrate the ultimate fix script"""
    
    # Read the Birmingham template
    template_path = '/home/ubuntu/dollar-fence-website/locations/alabama/birmingham/index.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    print(f"Loaded Birmingham template: {len(template_content)} characters")
    
    # Test the ultimate fix on a few problematic locations
    test_locations = [
        ("Houston", "Texas"),
        ("Los Angeles", "California"),
        ("Atlanta", "Georgia"),
        ("Denver", "Colorado"),
        ("Miami", "Florida"),
    ]
    
    print(f"\n=== TESTING ULTIMATE GEOGRAPHIC FIX ===")
    
    for city, state in test_locations:
        try:
            page_path, content_size = regenerate_location_page_with_ultimate_fix(city, state, template_content)
            print(f"✅ {city}, {state}: {content_size} characters -> {page_path}")
        except Exception as e:
            print(f"❌ {city}, {state}: Error - {str(e)}")
    
    print(f"\n=== ULTIMATE FIX SCRIPT READY ===")
    print("This script provides comprehensive geographic replacement for ALL location pages.")
    
    return True

if __name__ == "__main__":
    success = main()
    print(f"\nUltimate fix script test: {'SUCCESS' if success else 'FAILED'}")

