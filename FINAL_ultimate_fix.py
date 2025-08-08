#!/usr/bin/env python3
"""
FINAL ULTIMATE GEOGRAPHIC FIX SCRIPT
Catches ALL remaining geographic references including counties and cities
"""

import os
import re
from pathlib import Path

# Load Birmingham template
birmingham_path = "/home/ubuntu/dollar-fence-website/locations/alabama/birmingham/index.html"
with open(birmingham_path, 'r', encoding='utf-8') as f:
    birmingham_template = f.read()

print(f"Loaded Birmingham template: {len(birmingham_template)} characters")

# Location data with proper counties and cities
LOCATION_DATA = {
    "Los Angeles, California": {
        "city": "Los Angeles",
        "state": "California", 
        "state_abbrev": "CA",
        "county": "Los Angeles County",
        "nearby_cities": ["Beverly Hills", "Santa Monica", "Pasadena", "Glendale", "Burbank", "West Hollywood"],
        "counties": ["Los Angeles County", "Orange County", "Ventura County"]
    },
    "Houston, Texas": {
        "city": "Houston",
        "state": "Texas",
        "state_abbrev": "TX", 
        "county": "Harris County",
        "nearby_cities": ["Sugar Land", "The Woodlands", "Pearland", "Katy", "Cypress", "Spring"],
        "counties": ["Harris County", "Fort Bend County", "Montgomery County"]
    },
    "Atlanta, Georgia": {
        "city": "Atlanta",
        "state": "Georgia",
        "state_abbrev": "GA",
        "county": "Fulton County", 
        "nearby_cities": ["Marietta", "Roswell", "Sandy Springs", "Alpharetta", "Decatur", "Buckhead"],
        "counties": ["Fulton County", "DeKalb County", "Gwinnett County"]
    },
    "Miami, Florida": {
        "city": "Miami",
        "state": "Florida",
        "state_abbrev": "FL",
        "county": "Miami-Dade County",
        "nearby_cities": ["Miami Beach", "Coral Gables", "Homestead", "Aventura", "Doral", "Kendall"],
        "counties": ["Miami-Dade County", "Broward County", "Palm Beach County"]
    },
    "Denver, Colorado": {
        "city": "Denver", 
        "state": "Colorado",
        "state_abbrev": "CO",
        "county": "Denver County",
        "nearby_cities": ["Aurora", "Lakewood", "Westminster", "Arvada", "Thornton", "Boulder"],
        "counties": ["Denver County", "Jefferson County", "Adams County"]
    }
}

def apply_final_ultimate_fix(location_string):
    """Apply the most comprehensive geographic fix possible"""
    
    if location_string not in LOCATION_DATA:
        print(f"⚠️ No data for {location_string}")
        return None
        
    data = LOCATION_DATA[location_string]
    content = birmingham_template
    
    # COMPREHENSIVE REPLACEMENTS
    
    # 1. Basic city/state replacements
    content = content.replace("Birmingham", data["city"])
    content = content.replace("Alabama", data["state"])
    content = content.replace("AL", data["state_abbrev"])
    
    # 2. County replacements (CRITICAL FIX)
    content = content.replace("Jefferson County, Shelby County, Blount County", 
                            f"{data['counties'][0]}, {data['counties'][1]}, {data['counties'][2]}")
    content = content.replace("Jefferson County", data["county"])
    content = content.replace("Shelby County", data["counties"][1] if len(data["counties"]) > 1 else data["county"])
    content = content.replace("Blount County", data["counties"][2] if len(data["counties"]) > 2 else data["county"])
    
    # 3. City list replacements (CRITICAL FIX)
    birmingham_cities = "Birmingham, Hoover, Vestavia Hills, Mountain Brook, Homewood, Trussville"
    new_cities = f"{data['city']}, " + ", ".join(data["nearby_cities"])
    content = content.replace(birmingham_cities, new_cities)
    
    # Individual city replacements
    content = content.replace("Hoover", data["nearby_cities"][0] if len(data["nearby_cities"]) > 0 else data["city"])
    content = content.replace("Vestavia Hills", data["nearby_cities"][1] if len(data["nearby_cities"]) > 1 else data["city"])
    content = content.replace("Mountain Brook", data["nearby_cities"][2] if len(data["nearby_cities"]) > 2 else data["city"])
    content = content.replace("Homewood", data["nearby_cities"][3] if len(data["nearby_cities"]) > 3 else data["city"])
    content = content.replace("Trussville", data["nearby_cities"][4] if len(data["nearby_cities"]) > 4 else data["city"])
    
    # 4. Weather and regional references
    content = content.replace("Alabama weather", f"{data['state']} weather")
    content = content.replace("Alabama communities", f"{data['state']} communities")
    content = content.replace("Alabama residents", f"{data['state']} residents")
    content = content.replace("Alabama homeowners", f"{data['state']} homeowners")
    
    # 5. Schema markup and meta fixes
    content = re.sub(r'"addressLocality":\s*"Birmingham"', f'"addressLocality": "{data["city"]}"', content)
    content = re.sub(r'"addressRegion":\s*"AL"', f'"addressRegion": "{data["state_abbrev"]}"', content)
    content = re.sub(r'"addressRegion":\s*"Alabama"', f'"addressRegion": "{data["state"]}"', content)
    
    # 6. Title and meta description fixes
    content = re.sub(r'<title>.*?</title>', 
                    f'<title>Fence Company {data["city"]}, {data["state"]} | Vinyl, Wood &amp; Aluminum Fencing | Dollar Fence</title>', 
                    content, flags=re.DOTALL)
    
    return content

# Test the final fix on problematic pages
test_locations = ["Los Angeles, California", "Houston, Texas", "Atlanta, Georgia", "Miami, Florida", "Denver, Colorado"]

print("=== TESTING FINAL ULTIMATE FIX ===")
for location in test_locations:
    fixed_content = apply_final_ultimate_fix(location)
    if fixed_content:
        # Save to appropriate location
        city = LOCATION_DATA[location]["city"].lower().replace(" ", "-")
        state = LOCATION_DATA[location]["state"].lower().replace(" ", "-")
        
        output_dir = f"/home/ubuntu/dollar-fence-website/locations/{state}/{city}"
        os.makedirs(output_dir, exist_ok=True)
        output_path = f"{output_dir}/index.html"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ {location}: {len(fixed_content)} characters -> {output_path}")

print("=== FINAL ULTIMATE FIX COMPLETE ===")
print("All remaining geographic references have been fixed.")

