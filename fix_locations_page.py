#!/usr/bin/env python3
"""
Fix Locations Page Internal Links
Updates the /locations/ page to fix all broken internal links
"""

import os
import json
import re

def load_link_mapping():
    """Load the mapping of broken links to working alternatives"""
    
    with open('broken_link_mapping.json', 'r') as f:
        mapping = json.load(f)
    
    with open('page_creation_report.json', 'r') as f:
        creation_report = json.load(f)
    
    return mapping, creation_report

def create_link_fixes(mapping, creation_report):
    """Create a comprehensive list of link fixes needed"""
    
    fixes = []
    
    # Add fixes for links with existing alternatives
    for item in mapping['has_alternative']:
        # Extract the correct URL path from working_url
        working_path = item['working_url'].replace('https://dollarfence.com', '')
        
        fixes.append({
            'type': 'redirect_to_existing',
            'display_name': item['display_name'],
            'broken_url_path': item['broken_url'].replace('https://dollarfence.com', ''),
            'working_url_path': working_path,
            'description': f"Redirect {item['display_name']} to existing page"
        })
    
    # Add fixes for newly created pages
    for page in creation_report['created_pages']:
        # Find the corresponding broken link
        broken_item = None
        for item in mapping['needs_creation']:
            if item['display_name'] == page['display_name']:
                broken_item = item
                break
        
        if broken_item:
            fixes.append({
                'type': 'redirect_to_new',
                'display_name': page['display_name'],
                'broken_url_path': broken_item['broken_url'].replace('https://dollarfence.com', ''),
                'working_url_path': page['url_path'],
                'description': f"Redirect {page['display_name']} to newly created page"
            })
    
    return fixes

def fix_locations_page_links(fixes):
    """Fix the internal links on the locations page"""
    
    print("=== FIXING LOCATIONS PAGE INTERNAL LINKS ===")
    
    # Read the current locations page
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
        
        for fix in fixes:
            display_name = fix['display_name']
            broken_path = fix['broken_url_path']
            working_path = fix['working_url_path']
            
            print(f"\n🔧 Fixing: {display_name}")
            print(f"   From: {broken_path}")
            print(f"   To: {working_path}")
            
            # Look for various link patterns that might reference the broken URL
            patterns_to_fix = [
                # Direct href links
                f'href="{broken_path}"',
                f"href='{broken_path}'",
                # Without leading slash
                f'href="{broken_path[1:]}"' if broken_path.startswith('/') else f'href="/{broken_path}"',
                f"href='{broken_path[1:]}'" if broken_path.startswith('/') else f"href='/{broken_path}'",
            ]
            
            replacements = [
                f'href="{working_path}"',
                f"href='{working_path}'",
                f'href="{working_path[1:]}"' if working_path.startswith('/') else f'href="/{working_path}"',
                f"href='{working_path[1:]}'" if working_path.startswith('/') else f"href='/{working_path}'",
            ]
            
            found_and_fixed = False
            
            for i, pattern in enumerate(patterns_to_fix):
                if pattern in content:
                    content = content.replace(pattern, replacements[i])
                    fixes_applied += 1
                    found_and_fixed = True
                    print(f"   ✅ Fixed pattern: {pattern}")
            
            # Also try to fix based on display name patterns
            # Look for the display name in the HTML and fix nearby links
            if display_name in content:
                # Find sections containing the display name
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if display_name in line:
                        # Check surrounding lines for broken links
                        for j in range(max(0, i-3), min(len(lines), i+4)):
                            for pattern in patterns_to_fix:
                                if pattern in lines[j]:
                                    lines[j] = lines[j].replace(pattern, replacements[patterns_to_fix.index(pattern)])
                                    found_and_fixed = True
                                    print(f"   ✅ Fixed in context of {display_name}")
                
                content = '\n'.join(lines)
            
            if not found_and_fixed:
                print(f"   ⚠️  No matching patterns found for {display_name}")
        
        # Write the updated content
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

def verify_fixes(fixes):
    """Verify that the fixes were applied correctly"""
    
    print(f"\n=== VERIFYING FIXES ===")
    
    locations_file = 'locations/index.html'
    
    try:
        with open(locations_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        verification_results = []
        
        for fix in fixes:
            broken_path = fix['broken_url_path']
            working_path = fix['working_url_path']
            display_name = fix['display_name']
            
            # Check if broken links still exist
            broken_patterns = [
                f'href="{broken_path}"',
                f"href='{broken_path}'",
            ]
            
            still_broken = any(pattern in content for pattern in broken_patterns)
            
            # Check if working links exist
            working_patterns = [
                f'href="{working_path}"',
                f"href='{working_path}'",
            ]
            
            has_working = any(pattern in content for pattern in working_patterns)
            
            verification_results.append({
                'display_name': display_name,
                'still_broken': still_broken,
                'has_working': has_working,
                'status': 'FIXED' if not still_broken and has_working else 'NEEDS_ATTENTION'
            })
            
            if not still_broken and has_working:
                print(f"✅ {display_name}: Fixed successfully")
            elif still_broken:
                print(f"❌ {display_name}: Still has broken links")
            elif not has_working:
                print(f"⚠️  {display_name}: No working links found")
        
        return verification_results
        
    except Exception as e:
        print(f"❌ Error verifying fixes: {str(e)}")
        return []

def generate_fix_report(fixes, verification_results):
    """Generate a comprehensive fix report"""
    
    print(f"\n=== FIX SUMMARY ===")
    
    successful_fixes = [v for v in verification_results if v['status'] == 'FIXED']
    needs_attention = [v for v in verification_results if v['status'] == 'NEEDS_ATTENTION']
    
    print(f"Total fixes attempted: {len(fixes)}")
    print(f"Successfully fixed: {len(successful_fixes)}")
    print(f"Needs attention: {len(needs_attention)}")
    
    if successful_fixes:
        print(f"\n=== SUCCESSFULLY FIXED ===")
        for result in successful_fixes:
            print(f"✅ {result['display_name']}")
    
    if needs_attention:
        print(f"\n=== NEEDS ATTENTION ===")
        for result in needs_attention:
            print(f"⚠️  {result['display_name']}")
    
    # Save report
    report = {
        'fixes_attempted': fixes,
        'verification_results': verification_results,
        'summary': {
            'total_fixes': len(fixes),
            'successful': len(successful_fixes),
            'needs_attention': len(needs_attention)
        }
    }
    
    with open('locations_page_fix_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: locations_page_fix_report.json")
    
    return report

def main():
    print("Starting locations page fix process...")
    
    # Change to website directory
    os.chdir('/home/ubuntu/dollar-fence-website')
    
    # Load mapping and creation report
    mapping, creation_report = load_link_mapping()
    
    # Create comprehensive list of fixes needed
    fixes = create_link_fixes(mapping, creation_report)
    print(f"Identified {len(fixes)} links to fix")
    
    # Fix the locations page links
    success = fix_locations_page_links(fixes)
    
    if success:
        # Verify the fixes
        verification_results = verify_fixes(fixes)
        
        # Generate comprehensive report
        report = generate_fix_report(fixes, verification_results)
        
        return report
    else:
        print("❌ Failed to fix locations page")
        return None

if __name__ == "__main__":
    report = main()

