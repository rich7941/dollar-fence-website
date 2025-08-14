#!/usr/bin/env python3
"""
Enhanced Location Page Generator with Integrated Review System
Generates complete location pages with unique, location-specific customer reviews
"""

import os
import re
import json
import random
from pathlib import Path

# Import the review generation functions
def generate_location_reviews(city, state):
    """Generate unique reviews for a specific location"""
    
    # Pool of realistic customer names
    first_names = [
        "Michael", "Sarah", "Robert", "Jennifer", "David", "Lisa", "James", "Maria",
        "John", "Patricia", "Christopher", "Linda", "Matthew", "Elizabeth", "Anthony",
        "Barbara", "Mark", "Susan", "Donald", "Jessica", "Steven", "Karen", "Paul",
        "Nancy", "Andrew", "Betty", "Joshua", "Helen", "Kenneth", "Sandra", "Kevin",
        "Donna", "Brian", "Carol", "George", "Ruth", "Timothy", "Sharon", "Ronald",
        "Michelle", "Jason", "Laura", "Edward", "Sarah", "Jeffrey", "Kimberly",
        "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry",
        "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Gregory", "Alexander",
        "Patrick", "Frank", "Raymond", "Jack", "Dennis", "Jerry", "Tyler", "Aaron"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
        "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
        "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner",
        "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
        "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper"
    ]
    
    # Pool of fence types and features
    fence_types = [
        "vinyl fence", "wood fence", "composite fence", "aluminum fence", 
        "chain link fence", "privacy fence", "pool fence", "decorative fence",
        "security fence", "garden fence", "picket fence", "ranch fence"
    ]
    
    # Pool of positive descriptors
    descriptors = [
        "outstanding", "excellent", "amazing", "fantastic", "superb", "exceptional",
        "professional", "high-quality", "beautiful", "perfect", "impressive",
        "top-notch", "wonderful", "incredible", "remarkable", "superior"
    ]
    
    # Pool of service aspects
    service_aspects = [
        "installation", "workmanship", "customer service", "communication", 
        "attention to detail", "professionalism", "quality", "craftsmanship",
        "project management", "cleanup", "efficiency", "expertise"
    ]
    
    # Pool of positive outcomes
    outcomes = [
        "exceeded our expectations", "looks fantastic", "transformed our yard",
        "added great value to our home", "provides perfect privacy", 
        "enhanced our property", "solved our needs perfectly", "looks amazing",
        "completed efficiently", "finished beautifully", "works perfectly",
        "improved our outdoor space", "gave us peace of mind"
    ]
    
    # Generate 3 unique reviews
    reviews = []
    used_names = set()
    
    for i in range(3):
        # Generate unique name
        while True:
            first = random.choice(first_names)
            last = random.choice(last_names)
            full_name = f"{first} {last}"
            if full_name not in used_names:
                used_names.add(full_name)
                break
        
        # Select random elements for variety
        fence_type = random.choice(fence_types)
        descriptor = random.choice(descriptors)
        service_aspect = random.choice(service_aspects)
        outcome = random.choice(outcomes)
        
        # Generate review templates with variety
        review_templates = [
            f"{descriptor.title()} results! The {fence_type} installation {outcome}. The crew was respectful of our {city} property and completed the work efficiently. Very satisfied with Dollar Fence.",
            
            f"Dollar Fence transformed our {city} backyard with a beautiful {fence_type}. The installation was quick and clean, and the final result {outcome}. Highly recommend their services in the {city} area.",
            
            f"Excellent {service_aspect} and superior craftsmanship. The new {fence_type} around our {city} home {outcome}. Dollar Fence made the entire process smooth and stress-free.",
            
            f"We needed a {fence_type} quickly for our {city} property, and Dollar Fence delivered perfectly. Fast installation, great communication, and the fence {outcome}. Highly recommend for any {city} residents!",
            
            f"{descriptor.title()} experience from start to finish! The {fence_type} they installed has completely {outcome}. Fair pricing, excellent workmanship, and they cleaned up perfectly. Five stars!",
            
            f"Dollar Fence provided {descriptor} {service_aspect} for our {fence_type} project in {city}. The team was professional, punctual, and the quality is outstanding. Our neighbors have been asking for their contact information!",
            
            f"Amazing {service_aspect} and {descriptor} results! The {fence_type} installation {outcome}. The crew was respectful and completed the work efficiently. Very satisfied with Dollar Fence in {city}.",
            
            f"We're thrilled with our new {fence_type} from Dollar Fence! The installation in {city} was seamless, and the final result {outcome}. Professional team and {descriptor} quality throughout.",
            
            f"Outstanding {service_aspect}! Dollar Fence installed our {fence_type} with precision and care. The project in {city} {outcome} and added great value to our property. Highly recommended!",
            
            f"Excellent choice for {fence_type} installation in {city}! The team's {service_aspect} was {descriptor}, and the finished product {outcome}. Clean, professional, and reliable service."
        ]
        
        # Select random template and create review
        review_text = random.choice(review_templates)
        
        # Create nearby cities for location variety
        nearby_locations = [
            f"{city}, {state}",
            f"Near {city}, {state}",
            f"{city} area, {state}",
            f"Greater {city}, {state}"
        ]
        
        review = {
            "name": full_name,
            "location": random.choice(nearby_locations),
            "review": review_text
        }
        
        reviews.append(review)
    
    return reviews

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
        "St. Johns": "St. Johns County",
        
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
        "St. Louis": "St. Louis County",
        
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
        
        # New Jersey
        "Newark": "Essex County",
        "Jersey City": "Hudson County",
        "Paterson": "Passaic County",
        "Elizabeth": "Union County",
        "Edison": "Middlesex County",
        "Woodbridge": "Middlesex County",
        "Lakewood": "Ocean County",
        "Toms River": "Ocean County",
        "Hamilton Township": "Mercer County",
        "Trenton": "Mercer County",
        
        # Utah
        "Salt Lake City": "Salt Lake County",
        "West Valley City": "Salt Lake County",
        "Provo": "Utah County",
        "West Jordan": "Salt Lake County",
        "Orem": "Utah County",
        "Sandy": "Salt Lake County",
        "Ogden": "Weber County",
        "St. George": "Washington County",
        "Layton": "Davis County",
        "Taylorsville": "Salt Lake County",
        
        # Minnesota
        "Minneapolis": "Hennepin County",
        "Saint Paul": "Ramsey County",
        "Rochester": "Olmsted County",
        "Duluth": "St. Louis County",
        "Bloomington": "Hennepin County",
        "Brooklyn Park": "Hennepin County",
        "Plymouth": "Hennepin County",
        "St. Cloud": "Stearns County",
        "Eagan": "Dakota County",
        "Woodbury": "Washington County",
        
        # Add more as needed
    }
    
    return county_map.get(city, f"{city} County")

def apply_reviews_to_content(content, reviews):
    """Apply generated reviews to the HTML content"""
    
    # Replace reviews in JSON-LD schema
    for i, review in enumerate(reviews, 1):
        # Replace author name in JSON-LD schema
        pattern = rf'"name": "Customer {i}"'
        replacement = f'"name": "{review["name"]}"'
        content = re.sub(pattern, replacement, content)
        
        # Replace review body in JSON-LD schema
        pattern = rf'"reviewBody": "[^"]*"'
        escaped_review = review["review"].replace('"', '\\"')
        
        if i == 1:
            replacement = f'"reviewBody": "{escaped_review}"'
            content = re.sub(pattern, replacement, content, count=1)
        elif i == 2:
            # Find the second occurrence
            matches = list(re.finditer(pattern, content))
            if len(matches) >= 2:
                start, end = matches[1].span()
                content = content[:start] + f'"reviewBody": "{escaped_review}"' + content[end:]
        elif i == 3:
            # Find the third occurrence
            matches = list(re.finditer(pattern, content))
            if len(matches) >= 3:
                start, end = matches[2].span()
                content = content[:start] + f'"reviewBody": "{escaped_review}"' + content[end:]
    
    return content

def generate_location_page_with_reviews(location_input, output_base_dir=None):
    """Generate a complete HTML page for a specific location with unique reviews"""
    
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
    
    # Read the Birmingham template
    template_path = "/home/ubuntu/dollar-fence-website/locations/alabama/birmingham/index.html"
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        return {"error": f"Template file not found: {template_path}"}
    
    # Generate unique reviews for this location
    reviews = generate_location_reviews(city, state)
    
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
    
    # Apply the generated reviews to the content
    content = apply_reviews_to_content(content, reviews)
    
    # Main content replacements
    content = content.replace("Birmingham", city)
    content = content.replace("Alabama", state)
    content = content.replace("Jefferson County", county)
    
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
    content = re.sub(r'\\bBirmingham fence company\\b', f'{city} fence company', content, flags=re.IGNORECASE)
    content = re.sub(r'\\bBirmingham fence contractor\\b', f'{city} fence contractor', content, flags=re.IGNORECASE)
    content = re.sub(r'\\bBirmingham customers\\b', f'{city} customers', content, flags=re.IGNORECASE)
    content = re.sub(r'\\bBirmingham properties\\b', f'{city} properties', content, flags=re.IGNORECASE)
    content = re.sub(r'\\bBirmingham area\\b', f'{city} area', content, flags=re.IGNORECASE)
    content = re.sub(r'\\bBirmingham homes\\b', f'{city} homes', content, flags=re.IGNORECASE)
    content = re.sub(r'\\bBirmingham property\\b', f'{city} property', content, flags=re.IGNORECASE)
    content = re.sub(r'\\bin Birmingham\\b', f'in {city}', content, flags=re.IGNORECASE)
    content = re.sub(r'\\bthroughout Birmingham\\b', f'throughout {city}', content, flags=re.IGNORECASE)
    content = re.sub(r'\\baround Birmingham\\b', f'around {city}', content, flags=re.IGNORECASE)
    
    # FAQ section updates
    content = re.sub(
        r'How much does fence installation cost in Birmingham\\?',
        f'How much does fence installation cost in {city}?',
        content
    )
    
    content = re.sub(
        r'Fence installation costs in Birmingham vary by material',
        f'Fence installation costs in {city} vary by material',
        content
    )
    
    content = re.sub(
        r'What types of fences do you install in Birmingham\\?',
        f'What types of fences do you install in {city}?',
        content
    )
    
    content = re.sub(
        r'throughout Birmingham, Hoover, Vestavia Hills, Mountain Brook, and Jefferson County',
        f'throughout {city} and {county}',
        content
    )
    
    content = re.sub(
        r'How long does fence installation take in Birmingham\\?',
        f'How long does fence installation take in {city}?',
        content
    )
    
    content = re.sub(
        r'Most residential fence installations in Birmingham take',
        f'Most residential fence installations in {city} take',
        content
    )
    
    content = re.sub(
        r'Do you offer financing for fence installation in Birmingham\\?',
        f'Do you offer financing for fence installation in {city}?',
        content
    )
    
    # Determine output directory
    if output_base_dir is None:
        output_base_dir = "/home/ubuntu/dollar-fence-website"
    
    # Create the directory structure
    output_dir = f"{output_base_dir}/locations/{state_url}/{city_url}"
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
        "county": county,
        "reviews": [{"name": r["name"], "location": r["location"]} for r in reviews]
    }

def main():
    """Main function for testing"""
    import sys
    if len(sys.argv) > 1:
        location = sys.argv[1]
        result = generate_location_page_with_reviews(location)
        print(json.dumps(result, indent=2))
    else:
        # Test with a sample location
        result = generate_location_page_with_reviews("Miami, Florida")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

