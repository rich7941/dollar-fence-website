#!/usr/bin/env python3

import os
import random

# Define unique customer names and review templates
customer_names = [
    "Gregory Cruz", "Sandra Evans", "Sandra Nguyen", "Kevin Green", "Steven Brown", 
    "Michael Williams", "Deborah Cook", "Benjamin Morris", "Brandon Kim", "Nancy Lewis",
    "Dorothy Kelly", "Lisa Stewart", "Helen Allen", "Dorothy Cook", "Patrick Harris",
    "Laura Ramos", "Raymond Sanchez", "Sarah Scott", "Jennifer Martinez", "David Johnson",
    "Maria Rodriguez", "Robert Davis", "Linda Wilson", "James Anderson", "Patricia Taylor"
]

review_templates = [
    "Outstanding results! The {fence_type} fence installation exceeded our expectations. The crew was respectful of our {location} property and completed the work efficiently. Very satisfied with Dollar Fence.",
    "Dollar Fence transformed our {location} backyard with a beautiful {fence_type} fence. The installation was quick and clean, and the final result looks amazing. Highly recommend their services in the {area}.",
    "Excellent customer service and superior craftsmanship. The new {fence_type} fence around our {neighborhood} home looks fantastic. Dollar Fence made the entire process smooth and stress-free.",
    "Professional team and quality work. The {fence_type} fencing project was completed on time and within budget. Great experience with Dollar Fence in {location}.",
    "Impressed with the attention to detail and quality materials. Our new {fence_type} fence has enhanced both privacy and curb appeal of our {location} property.",
    "Top-notch service from start to finish. The {fence_type} fence installation was handled professionally and the results speak for themselves. Highly recommend Dollar Fence.",
    "Fantastic experience with Dollar Fence. The {fence_type} fencing project exceeded our expectations and the team was courteous and efficient throughout the process.",
    "Quality craftsmanship and reliable service. Our {fence_type} fence looks great and has added significant value to our {location} home.",
    "Excellent work and fair pricing. The {fence_type} fence installation was completed professionally and we couldn't be happier with the results.",
    "Outstanding customer service and beautiful results. The new {fence_type} fence has transformed our {location} property and we highly recommend Dollar Fence."
]

fence_types = ["composite", "vinyl", "wood", "cedar", "aluminum"]
neighborhoods = ["Vestavia Hills", "Mountain Brook", "Homewood", "Irondale", "Hoover"]

# Location-specific data
locations_data = {
    "hamilton-township": {
        "city": "Hamilton Township",
        "state": "New Jersey",
        "area": "Hamilton Township area",
        "neighborhoods": ["Mountain Brook", "Homewood", "Irondale"]
    },
    "port-st-lucie": {
        "city": "Port St. Lucie", 
        "state": "Florida",
        "area": "Port St. Lucie area",
        "neighborhoods": ["Mountain Brook", "Homewood", "Irondale"]
    },
    "st-george": {
        "city": "St. George",
        "state": "Utah", 
        "area": "St. George area",
        "neighborhoods": ["Mountain Brook", "Homewood", "Irondale"]
    },
    "saint-paul": {
        "city": "St. Paul",
        "state": "Minnesota",
        "area": "St. Paul area", 
        "neighborhoods": ["Mountain Brook", "Homewood", "Irondale"]
    },
    "st-louis": {
        "city": "St. Louis",
        "state": "Missouri",
        "area": "St. Louis area",
        "neighborhoods": ["Mountain Brook", "Homewood", "Irondale"]
    },
    "st-johns": {
        "city": "St. Johns",
        "state": "Florida",
        "area": "St. Johns area",
        "neighborhoods": ["Mountain Brook", "Homewood", "Irondale"]
    }
}

def generate_unique_reviews(location_key, location_data):
    """Generate 3 unique reviews for a location"""
    reviews = []
    used_names = set()
    
    for i in range(3):
        # Get unique customer name
        name = random.choice([n for n in customer_names if n not in used_names])
        used_names.add(name)
        
        # Generate review content
        template = random.choice(review_templates)
        fence_type = random.choice(fence_types)
        neighborhood = random.choice(location_data["neighborhoods"])
        
        review_text = template.format(
            fence_type=fence_type,
            location=location_data["city"],
            area=location_data["area"],
            neighborhood=neighborhood
        )
        
        reviews.append({
            "name": name,
            "text": review_text,
            "location": f"{neighborhood}, {location_data['state']}"
        })
    
    return reviews

def update_location_reviews(location_key):
    """Update reviews for a specific location"""
    if location_key not in locations_data:
        print(f"Location {location_key} not found in data")
        return False
    
    # Find the HTML file
    if location_key == "hamilton-township":
        file_path = "locations/new-jersey/hamilton-township/index.html"
    elif location_key == "port-st-lucie":
        file_path = "locations/florida/port-st-lucie/index.html"
    elif location_key == "st-george":
        file_path = "locations/utah/st-george/index.html"
    elif location_key == "saint-paul":
        file_path = "locations/minnesota/saint-paul/index.html"
    elif location_key == "st-louis":
        file_path = "locations/missouri/st-louis/index.html"
    elif location_key == "st-johns":
        file_path = "locations/florida/st-johns/index.html"
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate unique reviews
    location_data = locations_data[location_key]
    reviews = generate_unique_reviews(location_key, location_data)
    
    # Replace the reviews section
    city_name = location_data["city"]
    
    # Find and replace the reviews section
    start_marker = f'<h2 class="text-center mb-5">Here\'s what our happy {city_name} customers have to say</h2>'
    end_marker = '</div>\n    </div>\n  </section>'
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"Could not find reviews section start marker in {file_path}")
        return False
    
    # Find the end of the reviews section
    temp_content = content[start_idx:]
    end_idx = temp_content.find(end_marker)
    if end_idx == -1:
        print(f"Could not find reviews section end marker in {file_path}")
        return False
    
    # Build new reviews HTML
    new_reviews_html = f'''<h2 class="text-center mb-5">Here's what our happy {city_name} customers have to say</h2>
    <div class="reviews-grid">
      <div class="review-card">
        <div class="review-content">
          <p>"{reviews[0]['text']}"</p>
        </div>
        <div class="review-author">
          <h3>{reviews[0]['name']}</h3>
          <p>{reviews[0]['location']}</p>
          <div class="stars">
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
          </div>
        </div>
      </div>
      <div class="review-card">
        <div class="review-content">
          <p>"{reviews[1]['text']}"</p>
        </div>
        <div class="review-author">
          <h3>{reviews[1]['name']}</h3>
          <p>{reviews[1]['location']}</p>
          <div class="stars">
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
          </div>
        </div>
      </div>
      <div class="review-card">
        <div class="review-content">
          <p>"{reviews[2]['text']}"</p>
        </div>
        <div class="review-author">
          <h3>{reviews[2]['name']}</h3>
          <p>{reviews[2]['location']}</p>
          <div class="stars">
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
            <span class="star">★</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>'''
    
    # Replace the content
    new_content = content[:start_idx] + new_reviews_html + content[start_idx + end_idx + len(end_marker):]
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated reviews for {city_name}")
    print(f"   - {reviews[0]['name']}")
    print(f"   - {reviews[1]['name']}")
    print(f"   - {reviews[2]['name']}")
    
    return True

# Update all 6 locations
locations_to_update = [
    "hamilton-township",
    "port-st-lucie", 
    "st-george",
    "saint-paul",
    "st-louis",
    "st-johns"
]

print("🔧 Updating reviews for all 6 new location pages...")
print()

for location in locations_to_update:
    success = update_location_reviews(location)
    if not success:
        print(f"❌ Failed to update {location}")
    print()

print("✅ Review updates complete!")

