#!/usr/bin/env python3
"""
Script to update meta title and description tags for all location pages
with the optimized format that achieved 9.5/10 SEO scores
"""

import os
import re
import json
from pathlib import Path

def get_county_or_parish_info(city, state):
    """Get county/parish information for cities, handling Louisiana parishes"""
    
    # Louisiana uses parishes instead of counties
    if state.lower() == "louisiana":
        parish_map = {
            "New Orleans": "Orleans Parish",
            "Baton Rouge": "East Baton Rouge Parish", 
            "Shreveport": "Caddo Parish",
            "Lafayette": "Lafayette Parish",
            "Lake Charles": "Calcasieu Parish",
            "Kenner": "Jefferson Parish",
            "Bossier City": "Bossier Parish",
            "Monroe": "Ouachita Parish",
            "Alexandria": "Rapides Parish",
            "Houma": "Terrebonne Parish",
            "Marrero": "Jefferson Parish",
            "Laplace": "St. John the Baptist Parish",
            "Harvey": "Jefferson Parish",
            "Slidell": "St. Tammany Parish",
            "Chalmette": "St. Bernard Parish"
        }
        return parish_map.get(city, f"{city} Parish")
    
    # Standard county mapping for other states
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
        "Port St. Lucie": "St. Lucie County",
        "Cape Coral": "Lee County",
        "Hollywood": "Broward County",
        "Gainesville": "Alachua County",
        "Clearwater": "Pinellas County",
        "Palm Bay": "Brevard County",
        "West Palm Beach": "Palm Beach County",
        "Lakeland": "Polk County",
        
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
        "Sugar Land": "Fort Bend County",
        "Tyler": "Smith County",
        "Amarillo": "Potter County",
        
        # Georgia
        "Atlanta": "Fulton County",
        "Augusta": "Richmond County",
        "Columbus": "Muscogee County",
        "Savannah": "Chatham County",
        "Sandy Springs": "Fulton County",
        "Roswell": "Fulton County",
        "Albany": "Dougherty County",
        "Warner Robins": "Houston County",
        "Marietta": "Cobb County",
        "Valdosta": "Lowndes County",
        
        # Add more major cities as needed
    }
    
    return county_map.get(city, f"{city} County")

def get_nearby_cities(city, state):
    """Get nearby cities for better geographic targeting in meta descriptions"""
    
    nearby_cities_map = {
        # Louisiana
        ("Lafayette", "Louisiana"): ["Broussard", "Scott", "Carencro"],
        ("New Orleans", "Louisiana"): ["Metairie", "Kenner", "Gretna"],
        ("Baton Rouge", "Louisiana"): ["Zachary", "Baker", "Central"],
        ("Shreveport", "Louisiana"): ["Bossier City", "Minden", "Marshall"],
        
        # Texas
        ("Houston", "Texas"): ["Sugar Land", "Katy", "The Woodlands"],
        ("Dallas", "Texas"): ["Plano", "Irving", "Garland"],
        ("Austin", "Texas"): ["Round Rock", "Cedar Park", "Pflugerville"],
        ("San Antonio", "Texas"): ["New Braunfels", "Schertz", "Universal City"],
        
        # California
        ("Los Angeles", "California"): ["Beverly Hills", "Santa Monica", "Pasadena"],
        ("San Diego", "California"): ["Chula Vista", "Oceanside", "Escondido"],
        ("San Francisco", "California"): ["Oakland", "Berkeley", "Daly City"],
        
        # Florida
        ("Miami", "Florida"): ["Coral Gables", "Hialeah", "Homestead"],
        ("Tampa", "Florida"): ["St. Petersburg", "Clearwater", "Brandon"],
        ("Orlando", "Florida"): ["Winter Park", "Kissimmee", "Altamonte Springs"],
        
        # Georgia
        ("Atlanta", "Georgia"): ["Sandy Springs", "Roswell", "Alpharetta"],
        ("Augusta", "Georgia"): ["Martinez", "Evans", "Grovetown"],
        
        # Add more as needed
    }
    
    return nearby_cities_map.get((city, state), [])

def create_optimized_meta_tags(city, state):
    """Create optimized meta title and description following the proven format"""
    
    # Get county/parish info
    county_or_parish = get_county_or_parish_info(city, state)
    
    # Get nearby cities for description
    nearby_cities = get_nearby_cities(city, state)
    
    # Create optimized title (following the proven format)
    title = f"Fence Company {city}, {state} | Vinyl, Wood & Aluminum Fencing | Dollar Fence"
    
    # Create optimized description
    if nearby_cities:
        # Include nearby cities if available
        nearby_text = f", {nearby_cities[0]}"
        if len(nearby_cities) > 1:
            nearby_text += f" & {nearby_cities[1]}"
    else:
        nearby_text = ""
    
    description = f"{city}'s #1 fence company. Professional vinyl, wood & aluminum fence installation. Free quotes, 96% satisfaction rate. Serving {city}{nearby_text} & {county_or_parish}."
    
    # Ensure description is under 160 characters
    if len(description) > 160:
        # Fallback to simpler format if too long
        description = f"{city}'s #1 fence company. Professional vinyl, wood & aluminum fence installation. Free quotes, 96% satisfaction rate. Serving {city} & {county_or_parish}."
    
    return title, description

def update_location_page_meta(file_path, city, state):
    """Update meta tags in a specific location page file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}
    
    # Generate optimized meta tags
    new_title, new_description = create_optimized_meta_tags(city, state)
    
    # Update title tag
    title_pattern = r'<title>.*?</title>'
    new_title_tag = f'<title>{new_title}</title>'
    content = re.sub(title_pattern, new_title_tag, content, flags=re.DOTALL)
    
    # Update meta description
    desc_pattern = r'<meta name="description" content="[^"]*">'
    new_desc_tag = f'<meta name="description" content="{new_description}">'
    content = re.sub(desc_pattern, new_desc_tag, content)
    
    # Update Open Graph title
    og_title_pattern = r'<meta property="og:title" content="[^"]*">'
    new_og_title = f'<meta property="og:title" content="{new_title}">'
    content = re.sub(og_title_pattern, new_og_title, content)
    
    # Update Open Graph description
    og_desc_pattern = r'<meta property="og:description" content="[^"]*">'
    new_og_desc = f'<meta property="og:description" content="{new_description}">'
    content = re.sub(og_desc_pattern, new_og_desc, content)
    
    # Update Twitter title
    twitter_title_pattern = r'<meta name="twitter:title" content="[^"]*">'
    new_twitter_title = f'<meta name="twitter:title" content="{new_title}">'
    content = re.sub(twitter_title_pattern, new_twitter_title, content)
    
    # Update Twitter description
    twitter_desc_pattern = r'<meta name="twitter:description" content="[^"]*">'
    new_twitter_desc = f'<meta name="twitter:description" content="{new_description}">'
    content = re.sub(twitter_desc_pattern, new_twitter_desc, content)
    
    # Write updated content back to file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        return {"error": f"Error writing file: {str(e)}"}
    
    return {
        "success": True,
        "location": f"{city}, {state}",
        "title": new_title,
        "description": new_description,
        "title_length": len(new_title),
        "description_length": len(new_description)
    }

def update_all_location_pages():
    """Update meta tags for all location pages in the website"""
    
    locations_dir = "/home/ubuntu/dollar-fence-website/locations"
    
    if not os.path.exists(locations_dir):
        return {"error": f"Locations directory not found: {locations_dir}"}
    
    results = []
    success_count = 0
    error_count = 0
    
    # Walk through all state directories
    for state_dir in os.listdir(locations_dir):
        state_path = os.path.join(locations_dir, state_dir)
        
        if not os.path.isdir(state_path):
            continue
            
        # Convert state directory name to proper state name
        state_name = state_dir.replace('-', ' ').title()
        
        # Walk through all city directories in this state
        for city_dir in os.listdir(state_path):
            city_path = os.path.join(state_path, city_dir)
            
            if not os.path.isdir(city_path):
                continue
                
            # Look for index.html file
            index_file = os.path.join(city_path, "index.html")
            
            if not os.path.exists(index_file):
                continue
                
            # Convert city directory name to proper city name
            city_name = city_dir.replace('-', ' ').title()
            
            # Handle special cases
            if city_name == "St ":
                city_name = city_name.replace("St ", "St. ")
            
            # Update the page
            result = update_location_page_meta(index_file, city_name, state_name)
            
            if result.get("success"):
                success_count += 1
            else:
                error_count += 1
                
            results.append(result)
            
            # Progress update every 50 pages
            if (success_count + error_count) % 50 == 0:
                print(f"Processed {success_count + error_count} pages... (✅ {success_count} success, ❌ {error_count} errors)")
    
    return {
        "total_processed": len(results),
        "success_count": success_count,
        "error_count": error_count,
        "results": results
    }

def update_single_location(city, state):
    """Update meta tags for a single location (for testing)"""
    
    # Convert to URL format
    state_url = state.lower().replace(' ', '-')
    city_url = city.lower().replace(' ', '-').replace('.', '').replace("'", '')
    
    file_path = f"/home/ubuntu/dollar-fence-website/locations/{state_url}/{city_url}/index.html"
    
    return update_location_page_meta(file_path, city, state)

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) == 3:
        # Update single location
        city = sys.argv[1]
        state = sys.argv[2]
        result = update_single_location(city, state)
        print(json.dumps(result, indent=2))
    elif len(sys.argv) == 2 and sys.argv[1] == "all":
        # Update all locations
        print("Starting meta tag optimization for all location pages...")
        result = update_all_location_pages()
        print(f"\n🎯 Meta Tag Optimization Complete!")
        print(f"✅ Successfully updated: {result['success_count']} pages")
        print(f"❌ Errors: {result['error_count']} pages")
        print(f"📊 Total processed: {result['total_processed']} pages")
        
        # Show some examples of successful updates
        successful_results = [r for r in result['results'] if r.get('success')]
        if successful_results:
            print(f"\n📝 Sample optimized meta tags:")
            for i, sample in enumerate(successful_results[:3]):
                print(f"\n{i+1}. {sample['location']}")
                print(f"   Title ({sample['title_length']} chars): {sample['title']}")
                print(f"   Description ({sample['description_length']} chars): {sample['description']}")
    else:
        # Test with Lafayette, Louisiana
        result = update_single_location("Lafayette", "Louisiana")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

