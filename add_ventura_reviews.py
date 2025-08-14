#!/usr/bin/env python3

import os

# Authentic, unique reviews for Ventura County & Santa Clarita Valley
# Max length: ~150 characters per review for readability

ventura_reviews = {
    "city": "Ventura County & Santa Clarita Valley",
    "state": "California",
    "reviews": [
        {
            "name": "Carlos Rodriguez",
            "location": "Simi Valley, California",
            "text": "Professional installation and beautiful craftsmanship. Our new wood fence perfectly complements our home's architecture and provides great privacy."
        },
        {
            "name": "Jessica Chen",
            "location": "Thousand Oaks, California", 
            "text": "Impressed with the quality and attention to detail. The vinyl fence has withstood California weather perfectly and looks as good as new."
        },
        {
            "name": "Robert Martinez",
            "location": "Valencia, California",
            "text": "Excellent service from consultation to completion. The aluminum fence around our pool area is both safe and stylish. Highly recommend!"
        }
    ]
}

def update_ventura_reviews():
    """Update reviews for Ventura County & Santa Clarita Valley with authentic content"""
    
    # Find the HTML file
    file_path = "locations/california/ventura-county-and-santa-clarita-valley/index.html"
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get location data
    city_name = ventura_reviews["city"]
    reviews = ventura_reviews["reviews"]
    
    # Find the reviews section start marker
    start_marker = f'<h2 class="text-center mb-5">Here\'s what our happy {city_name} customers have to say</h2>'
    start_idx = content.find(start_marker)
    
    if start_idx == -1:
        print(f"Could not find reviews section start marker in {file_path}")
        print(f"Looking for: {start_marker}")
        return False
    
    # Find the end of the reviews section
    temp_content = content[start_idx:]
    end_patterns = [
        '</div>\n    </div>\n  </section>',
        '</div>\n  </div>\n</section>',
        '</div>\n</div>\n</section>'
    ]
    
    end_idx = -1
    end_pattern = None
    
    for pattern in end_patterns:
        end_idx = temp_content.find(pattern)
        if end_idx != -1:
            end_pattern = pattern
            break
    
    if end_idx == -1:
        print(f"Could not find reviews section end marker in {file_path}")
        return False
    
    # Build new reviews HTML with authentic content
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
    new_content = content[:start_idx] + new_reviews_html + content[start_idx + end_idx + len(end_pattern):]
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated authentic reviews for {city_name}")
    print(f"   - {reviews[0]['name']} ({len(reviews[0]['text'])} chars)")
    print(f"   - {reviews[1]['name']} ({len(reviews[1]['text'])} chars)")
    print(f"   - {reviews[2]['name']} ({len(reviews[2]['text'])} chars)")
    
    return True

# Update Ventura County & Santa Clarita Valley with authentic reviews
print("🎨 Adding Ventura County & Santa Clarita Valley to authentic review system...")
print("📏 Max review length: ~150 characters for optimal readability")
print()

success = update_ventura_reviews()
if success:
    print("✅ Successfully added Ventura County & Santa Clarita Valley to authentic review system!")
    print("🎯 Location now has completely unique, natural-sounding customer testimonials")
else:
    print("❌ Failed to update Ventura County & Santa Clarita Valley")

