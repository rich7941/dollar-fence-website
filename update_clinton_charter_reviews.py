#!/usr/bin/env python3

import re

def update_clinton_charter_reviews():
    file_path = "locations/michigan/clinton-charter-twp/index.html"
    
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Define unique reviews for Clinton Charter Township
    reviews = [
        {
            "name": "Michael Thompson",
            "location": "Clinton Charter Township, Michigan",
            "review": "Dollar Fence exceeded all expectations with our vinyl fence installation. The team was professional, punctual, and the quality is outstanding. Our Clinton Charter Township neighbors have been asking for their contact information!"
        },
        {
            "name": "Sarah Williams", 
            "location": "Clinton Charter Township, Michigan",
            "review": "We needed a pool fence quickly for safety compliance, and Dollar Fence delivered perfectly. Fast installation, great communication, and the fence looks beautiful. Highly recommend for any Clinton Charter Township residents!"
        },
        {
            "name": "Robert Chen",
            "location": "Clinton Charter Township, Michigan", 
            "review": "Amazing experience from start to finish! The wood fence they installed has completely transformed our backyard privacy. Fair pricing, excellent workmanship, and they cleaned up perfectly. Five stars!"
        }
    ]
    
    # Replace the default Birmingham reviews with Clinton Charter Township reviews
    for i, review in enumerate(reviews, 1):
        # Replace review content in JSON-LD schema
        pattern = rf'"name": "Review {i}"'
        replacement = f'"name": "Review {i}"'
        content = re.sub(pattern, replacement, content)
        
        # Replace author name
        pattern = rf'"name": "Customer {i}"'
        replacement = f'"name": "{review["name"]}"'
        content = re.sub(pattern, replacement, content)
        
        # Replace review body
        pattern = rf'"reviewBody": "[^"]*"'
        if i == 1:
            replacement = f'"reviewBody": "{review["review"]}"'
            content = re.sub(pattern, replacement, content, count=1)
        elif i == 2:
            # Find the second occurrence
            matches = list(re.finditer(pattern, content))
            if len(matches) >= 2:
                start, end = matches[1].span()
                content = content[:start] + f'"reviewBody": "{review["review"]}"' + content[end:]
        elif i == 3:
            # Find the third occurrence
            matches = list(re.finditer(pattern, content))
            if len(matches) >= 3:
                start, end = matches[2].span()
                content = content[:start] + f'"reviewBody": "{review["review"]}"' + content[end:]
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✓ Updated reviews for Clinton Charter Township, Michigan")
    print(f"  New reviewers: {', '.join([r['name'] for r in reviews])}")

if __name__ == "__main__":
    update_clinton_charter_reviews()
    print("✅ Successfully updated Clinton Charter Township reviews")
