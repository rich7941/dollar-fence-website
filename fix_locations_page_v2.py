#!/usr/bin/env python3
"""
Fix Locations Page Internal Links - Version 2
Updates the /locations/ page to fix the actual broken internal links found
"""

import os
import re

def fix_locations_page_links():
    """Fix the specific broken links found in the locations page"""
    
    print("=== FIXING LOCATIONS PAGE INTERNAL LINKS ===")
    
    locations_file = 'locations/index.html'
    
    if not os.path.exists(locations_file):
        print(f"❌ Locations page not found: {locations_file}")
        return False
    
    try:
        with open(locations_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_applied = 0
        
        print(f"📄 Processing: {locations_file}")
        
        # Define the specific broken links and their fixes
        link_fixes = [
            {
                'name': 'Port St. Lucie',
                'broken': '/locations/florida/port-st.-lucie/',
                'working': '/locations/florida/port-st-lucie/',
                'status': 'newly_created'
            },
            {
                'name': 'St. Johns', 
                'broken': '/locations/florida/st.-johns/',
                'working': '/locations/florida/st-johns/',
                'status': 'newly_created'
            },
            {
                'name': 'St. Petersburg',
                'broken': '/locations/florida/st.-petersburg/',
                'working': '/locations/florida/st-petersburg/',
                'status': 'existing_alternative'
            },
            {
                'name': 'Sandy Springs',
                'broken': '/locations/georgia/Sandy Springs/',
                'working': '/locations/georgia/sandy-springs/',
                'status': 'existing_alternative'
            },
            {
                'name': 'St. Paul',
                'broken': '/locations/minnesota/st.-paul/',
                'working': '/locations/minnesota/saint-paul/',
                'status': 'newly_created'
            },
            {
                'name': 'St. Louis',
                'broken': '/locations/missouri/st.-louis/',
                'working': '/locations/missouri/st-louis/',
                'status': 'newly_created'
            },
            {
                'name': 'Hamilton Township',
                'broken': '/locations/new-jersey/hamilton-twp./',
                'working': '/locations/new-jersey/hamilton-township/',
                'status': 'newly_created'
            },
            {
                'name': 'St. George',
                'broken': '/locations/utah/st.-george/',
                'working': '/locations/utah/st-george/',
                'status': 'newly_created'
            }
        ]
        
        for fix in link_fixes:
            name = fix['name']
            broken_link = fix['broken']
            working_link = fix['working']
            status = fix['status']
            
            print(f"\n🔧 Fixing: {name} ({status})")
            print(f"   From: {broken_link}")
            print(f"   To: {working_link}")
            
            # Look for the exact broken link pattern
            if broken_link in content:
                content = content.replace(broken_link, working_link)
                fixes_applied += 1
                print(f"   ✅ Fixed: {broken_link} → {working_link}")
            else:
                print(f"   ⚠️  Pattern not found: {broken_link}")
        
        # Also check for any remaining problematic patterns
        # Fix any remaining links with periods in city names
        period_patterns = [
            (r'/locations/([^/]+)/([^/]*st\.-[^/]*)', r'/locations/\1/\2'),
            (r'/locations/([^/]+)/([^/]*-twp\.)', r'/locations/\1/\2'),
        ]
        
        for pattern, replacement in period_patterns:
            matches = re.findall(pattern, content)
            if matches:
                print(f"\n🔧 Fixing period patterns...")
                for match in matches:
                    state, city_with_period = match
                    city_fixed = city_with_period.replace('st.-', 'st-').replace('-twp.', '-township')
                    old_path = f'/locations/{state}/{city_with_period}'
                    new_path = f'/locations/{state}/{city_fixed}'
                    
                    if old_path in content:
                        content = content.replace(old_path, new_path)
                        fixes_applied += 1
                        print(f"   ✅ Pattern fix: {old_path} → {new_path}")
        
        # Write the updated content if changes were made
        if content != original_content:
            with open(locations_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"\n✅ Updated locations page with {fixes_applied} fixes")
            return True
        else:
            print(f"\n⚠️  No changes made to locations page")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing locations page: {str(e)}")
        return False

def verify_fixes():
    """Verify that all broken links have been fixed"""
    
    print(f"\n=== VERIFYING FIXES ===")
    
    locations_file = 'locations/index.html'
    
    try:
        with open(locations_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for any remaining problematic patterns
        problematic_patterns = [
            r'/locations/[^/]+/[^/]*st\.-[^/]*',  # st.- patterns
            r'/locations/[^/]+/[^/]*-twp\.',      # -twp. patterns  
            r'/locations/[^/]+/[^/]*\s[^/]*/',    # spaces in URLs
        ]
        
        issues_found = []
        
        for pattern in problematic_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues_found.extend(matches)
        
        if issues_found:
            print(f"❌ Still found {len(issues_found)} problematic patterns:")
            for issue in issues_found:
                print(f"   • {issue}")
            return False
        else:
            print(f"✅ No problematic link patterns found")
            return True
            
    except Exception as e:
        print(f"❌ Error verifying fixes: {str(e)}")
        return False

def test_specific_links():
    """Test the specific links that were reported as broken"""
    
    print(f"\n=== TESTING SPECIFIC BROKEN LINKS ===")
    
    locations_file = 'locations/index.html'
    
    try:
        with open(locations_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # These are the exact broken links from the audit
        broken_links_to_check = [
            '/locations/florida/port-st.-lucie/',
            '/locations/new-jersey/hamilton-twp./',
            '/locations/utah/st.-george/',
            '/locations/florida/st.-petersburg/',
            '/locations/minnesota/st.-paul/',
            '/locations/missouri/st.-louis/',
            '/locations/florida/st.-johns/',
            '/locations/georgia/Sandy Springs/',
        ]
        
        still_broken = []
        
        for broken_link in broken_links_to_check:
            if broken_link in content:
                still_broken.append(broken_link)
        
        if still_broken:
            print(f"❌ Still found {len(still_broken)} broken links:")
            for link in still_broken:
                print(f"   • {link}")
            return False
        else:
            print(f"✅ All previously broken links have been fixed")
            return True
            
    except Exception as e:
        print(f"❌ Error testing links: {str(e)}")
        return False

def main():
    print("Starting locations page fix process (v2)...")
    
    # Change to website directory
    os.chdir('/home/ubuntu/dollar-fence-website')
    
    # Fix the locations page links
    success = fix_locations_page_links()
    
    if success:
        # Verify the fixes
        verification_success = verify_fixes()
        
        # Test specific broken links
        test_success = test_specific_links()
        
        if verification_success and test_success:
            print(f"\n🎉 ALL FIXES SUCCESSFUL!")
            print(f"   • Locations page updated")
            print(f"   • All broken links fixed")
            print(f"   • No problematic patterns remaining")
            return True
        else:
            print(f"\n⚠️  FIXES APPLIED BUT ISSUES REMAIN")
            return False
    else:
        print("❌ Failed to apply fixes")
        return False

if __name__ == "__main__":
    success = main()

