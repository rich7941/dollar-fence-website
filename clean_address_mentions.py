#!/usr/bin/env python3
"""
Clean up Regus/Servcorp mentions from business addresses in location pages
"""

import os
import re
import glob

def clean_address_mentions():
    """Remove Regus/Servcorp company mentions from streetAddress fields"""
    
    # Find all location index.html files
    location_files = glob.glob('locations/*/*/index.html')
    
    updated_count = 0
    total_files = len(location_files)
    
    print(f"🔍 Checking {total_files} location pages for Regus/Servcorp mentions...")
    
    for file_path in location_files:
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Clean up various Regus/Servcorp patterns
            patterns_to_clean = [
                # "Various Regus locations in Birmingham" -> "Business Center Birmingham"
                (r'"streetAddress":\s*"Various Regus locations in ([^"]+)"', r'"streetAddress": "Business Center \1"'),
                
                # "Regus (requires inquiry for specific address)" -> "Business Center (inquiry required)"
                (r'"streetAddress":\s*"Regus \(requires inquiry for specific address\)"', r'"streetAddress": "Business Center (inquiry required)"'),
                
                # "Regus Westminster Square" -> "Westminster Square"
                (r'"streetAddress":\s*"Regus ([^"]+)"', r'"streetAddress": "\1"'),
                
                # "Servcorp [location]" -> "[location]"
                (r'"streetAddress":\s*"Servcorp ([^"]+)"', r'"streetAddress": "\1"'),
                
                # Any remaining "Regus" or "Servcorp" mentions
                (r'"streetAddress":\s*"([^"]*)\bRegus\b([^"]*)"', r'"streetAddress": "\1Business Center\2"'),
                (r'"streetAddress":\s*"([^"]*)\bServcorp\b([^"]*)"', r'"streetAddress": "\1Business Center\2"'),
            ]
            
            # Apply all cleaning patterns
            for pattern, replacement in patterns_to_clean:
                content = re.sub(pattern, replacement, content)
            
            # Check if content was modified
            if content != original_content:
                # Write the updated content back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                updated_count += 1
                
                # Extract city/state for reporting
                city_state = file_path.replace('locations/', '').replace('/index.html', '').replace('/', ', ').title()
                print(f"✅ Cleaned: {city_state}")
        
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    print(f"\n🎉 Address Cleanup Complete!")
    print(f"✅ Updated: {updated_count} location pages")
    print(f"📊 Total checked: {total_files} pages")
    print(f"🎯 Result: Addresses now appear as professional business locations")
    print(f"📈 Impact: Maintains SEO benefits while removing company mentions")

if __name__ == "__main__":
    clean_address_mentions()

