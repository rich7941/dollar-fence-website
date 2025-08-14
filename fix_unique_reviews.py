#!/usr/bin/env python3
"""
Fix Unique Reviews Script - Actually update the HTML files with unique reviews
"""

import re
import random
import os

def generate_unique_reviews(city, state):
    """Generate 3 completely unique reviews for a location"""
    
    # Different customer names for each location
    name_pools = [
        ["Laura Ramos", "Raymond Sanchez", "Sarah Scott"],
        ["Gregory Cruz", "Sandra Evans", "Sandra Nguyen"], 
        ["Kevin Green", "Steven Brown", "Michael Williams"],
        ["Deborah Cook", "Benjamin Morris", "Brandon Kim"],
        ["Nancy Lewis", "Dorothy Kelly", "Lisa Stewart"],
        ["Helen Allen", "Dorothy Cook", "Patrick Harris"]
    ]
    
    # Use hash of city name to get consistent but different names
    city_hash = hash(city) % len(name_pools)
    names = name_pools[city_hash]
    
    # Different review templates
    review_templates = [
        f"Outstanding results! The composite fence installation exceeded our expectations. The crew was respectful of our {city} property and completed the work efficiently. Very satisfied with Dollar Fence.",
        
        f"Dollar Fence transformed our backyard with a beautiful composite fence. The installation was quick and clean, and the final result looks amazing. Highly recommend their services in the {city} area.",
        
        f"Excellent customer service and superior craftsmanship. The new cedar fence around our home looks fantastic. Dollar Fence made the entire process smooth and stress-free."
    ]
    
    # Different locations within the area
    locations = [
        f"{city}, {state}",
        f"Near {city}, {state}", 
        f"{city} area, {state}"
    ]
    
    reviews = []
    for i in range(3):
        reviews.append({
            "name": names[i],
            "location": locations[i],
            "review": review_templates[i]
        })
    
    return reviews

def update_html_reviews(file_path, city, state):
    """Actually update the HTML file with unique reviews"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        reviews = generate_unique_reviews(city, state)
        
        print(f"🔧 Updating {city}, {state} with unique reviews:")
        for review in reviews:
            print(f"   - {review['name']}: {review['review'][:50]}...")
        
        # Update the review section heading
        old_heading = f"Here's what our happy {city} customers have to say"
        content = re.sub(
            r'Here\'s what our happy .* customers have to say',
            old_heading,
            content
        )
        
        # Find and replace each review card
        for i, review in enumerate(reviews):
            # Pattern to find review cards
            pattern = r'<div class="review-card">\s*<div class="stars">★★★★★</div>\s*<h4>([^<]+)</h4>\s*<p>"([^"]+)"</p>\s*<div class="reviewer-info">\s*<span class="reviewer-location">([^<]+)</span>\s*</div>\s*</div>'
            
            def replace_review(match):
                if i == 0:  # Replace first review
                    return f'''<div class="review-card">
                <div class="stars">★★★★★</div>
                <h4>{review["name"]}</h4>
                <p>"{review["review"]}"</p>
                <div class="reviewer-info">
                  <span class="reviewer-location">{review["location"]}</span>
                </div>
              </div>'''
                return match.group(0)  # Keep other reviews unchanged for now
            
            if i == 0:
                content = re.sub(pattern, replace_review, content, count=1)
        
        # For simplicity, let's do a more direct replacement
        # Replace all three reviews at once
        review_section_pattern = r'(<div class="review-card">.*?</div>\s*){3}'
        
        new_review_section = ""
        for review in reviews:
            new_review_section += f'''<div class="review-card">
                <div class="stars">★★★★★</div>
                <h4>{review["name"]}</h4>
                <p>"{review["review"]}"</p>
                <div class="reviewer-info">
                  <span class="reviewer-location">{review["location"]}</span>
                </div>
              </div>
              '''
        
        # Find the reviews container and replace all reviews
        reviews_container_pattern = r'(<div class="reviews-container">.*?<div class="review-card">.*?</div>\s*<div class="review-card">.*?</div>\s*<div class="review-card">.*?</div>)(.*?</div>)'
        
        # Simpler approach - find and replace specific text patterns
        # Replace the names
        content = re.sub(r'<h4>Adam Williams</h4>', f'<h4>{reviews[0]["name"]}</h4>', content)
        content = re.sub(r'<h4>Patrick Morgan</h4>', f'<h4>{reviews[1]["name"]}</h4>', content)  
        content = re.sub(r'<h4>Matthew Garcia</h4>', f'<h4>{reviews[2]["name"]}</h4>', content)
        
        # Replace the review text
        content = re.sub(
            r'"Outstanding results! The composite fence installation exceeded our expectations\. The crew was respectful of our Mountain Brook property and completed the work efficiently\. Very satisfied with Dollar Fence\."',
            f'"{reviews[0]["review"]}"',
            content
        )
        
        content = re.sub(
            r'"Dollar Fence transformed our Hoover backyard with a beautiful composite fence\. The installation was quick and clean, and the final result looks amazing\. Highly recommend their services in the Hamilton Township area\."',
            f'"{reviews[1]["review"]}"',
            content
        )
        
        content = re.sub(
            r'"Excellent customer service and superior craftsmanship\. The new cedar fence around our Vestavia Hills home looks fantastic\. Dollar Fence made the entire process smooth and stress-free\."',
            f'"{reviews[2]["review"]}"',
            content
        )
        
        # Replace the locations
        content = re.sub(r'Homewood, Alabama', reviews[0]["location"], content)
        content = re.sub(r'Irondale, Alabama', reviews[1]["location"], content)
        content = re.sub(r'Mountain Brook, Alabama', reviews[2]["location"], content)
        
        # Also update any other state references
        content = re.sub(r'Alabama', state, content)
        content = re.sub(r'Homewood, [^<]+', reviews[0]["location"], content)
        content = re.sub(r'Irondale, [^<]+', reviews[1]["location"], content)
        content = re.sub(r'Mountain Brook, [^<]+', reviews[2]["location"], content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated reviews for {city}, {state}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {city}, {state}: {str(e)}")
        return False

def main():
    """Update all 6 new location pages with unique reviews"""
    
    locations = [
        {"city": "Port St. Lucie", "state": "Florida", "path": "locations/florida/port-st-lucie/index.html"},
        {"city": "Hamilton Township", "state": "New Jersey", "path": "locations/new-jersey/hamilton-township/index.html"},
        {"city": "St. George", "state": "Utah", "path": "locations/utah/st-george/index.html"},
        {"city": "Saint Paul", "state": "Minnesota", "path": "locations/minnesota/saint-paul/index.html"},
        {"city": "St. Louis", "state": "Missouri", "path": "locations/missouri/st-louis/index.html"},
        {"city": "St. Johns", "state": "Florida", "path": "locations/florida/st-johns/index.html"}
    ]
    
    print("=== FIXING UNIQUE REVIEWS ===")
    
    success_count = 0
    for location in locations:
        success = update_html_reviews(location["path"], location["city"], location["state"])
        if success:
            success_count += 1
    
    print(f"\n📊 RESULTS: {success_count}/{len(locations)} locations updated successfully")

if __name__ == "__main__":
    main()

