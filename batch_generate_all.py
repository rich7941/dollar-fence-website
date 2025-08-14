#!/usr/bin/env python3
"""
Batch generate all location pages directly in the repository
"""

import json
from generate_location_page import generate_location_page_with_reviews as generate_location_page

def main():
    # Read all locations
    with open('location_strings.txt', 'r') as f:
        locations = [line.strip() for line in f if line.strip()]
    
    print(f"Generating {len(locations)} location pages...")
    
    success_count = 0
    error_count = 0
    errors = []
    
    for i, location in enumerate(locations):
        try:
            result = generate_location_page(location)
            if result.get('success'):
                success_count += 1
                if (i + 1) % 50 == 0:
                    print(f"Generated {i + 1}/{len(locations)} pages...")
            else:
                error_count += 1
                errors.append(f"{location}: {result.get('error', 'Unknown error')}")
        except Exception as e:
            error_count += 1
            errors.append(f"{location}: {str(e)}")
    
    print(f"\nGeneration complete!")
    print(f"✅ Success: {success_count}")
    print(f"❌ Errors: {error_count}")
    
    if errors:
        print("\nErrors:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    return success_count, error_count

if __name__ == "__main__":
    main()

