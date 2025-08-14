#!/usr/bin/env python3
"""
Fix Canonical URL Formatting Issues
Scans all location pages and fixes canonical URLs to match actual page URLs
"""

import os
import re
import glob
from urllib.parse import urlparse

def scan_canonical_issues():
    """Scan all location pages for canonical URL formatting issues"""
    
    print("=== SCANNING FOR CANONICAL URL ISSUES ===")
    
    # Find all location HTML files
    location_files = glob.glob("locations/**/*.html", recursive=True)
    print(f"Found {len(location_files)} location pages to check")
    
    issues_found = []
    
    for file_path in location_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract canonical URL
            canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', content)
            if canonical_match:
                canonical_url = canonical_match.group(1)
                
                # Determine expected URL from file path
                # Convert file path to URL format
                expected_path = file_path.replace('locations/', '/locations/')
                expected_path = expected_path.replace('/index.html', '/')
                expected_path = expected_path.replace('\\', '/')  # Handle Windows paths
                expected_url = f"https://dollarfence.com{expected_path}"
                
                # Check if canonical URL matches expected URL
                if canonical_url != expected_url:
                    issues_found.append({
                        'file': file_path,
                        'canonical_url': canonical_url,
                        'expected_url': expected_url,
                        'issue_type': 'mismatch'
                    })
                    print(f"❌ MISMATCH: {file_path}")
                    print(f"   Canonical: {canonical_url}")
                    print(f"   Expected:  {expected_url}")
                    print()
            else:
                issues_found.append({
                    'file': file_path,
                    'canonical_url': None,
                    'expected_url': None,
                    'issue_type': 'missing'
                })
                print(f"⚠️  MISSING: {file_path} - No canonical URL found")
        
        except Exception as e:
            print(f"❌ ERROR reading {file_path}: {e}")
    
    print(f"\n=== SCAN SUMMARY ===")
    print(f"Total files scanned: {len(location_files)}")
    print(f"Issues found: {len(issues_found)}")
    
    # Categorize issues
    mismatches = [issue for issue in issues_found if issue['issue_type'] == 'mismatch']
    missing = [issue for issue in issues_found if issue['issue_type'] == 'missing']
    
    print(f"Canonical URL mismatches: {len(mismatches)}")
    print(f"Missing canonical URLs: {len(missing)}")
    
    return issues_found

def fix_canonical_urls(issues):
    """Fix canonical URL issues"""
    
    print(f"\n=== FIXING CANONICAL URL ISSUES ===")
    
    fixed_count = 0
    error_count = 0
    
    for issue in issues:
        file_path = issue['file']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if issue['issue_type'] == 'mismatch':
                # Replace incorrect canonical URL with correct one
                old_canonical = issue['canonical_url']
                new_canonical = issue['expected_url']
                
                # Create the replacement pattern
                old_tag = f'<link rel="canonical" href="{old_canonical}"'
                new_tag = f'<link rel="canonical" href="{new_canonical}"'
                
                if old_tag in content:
                    content = content.replace(old_tag, new_tag)
                    
                    # Write back to file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ FIXED: {file_path}")
                    print(f"   {old_canonical} → {new_canonical}")
                    fixed_count += 1
                else:
                    print(f"❌ PATTERN NOT FOUND: {file_path}")
                    error_count += 1
            
            elif issue['issue_type'] == 'missing':
                # Add missing canonical URL
                expected_path = file_path.replace('locations/', '/locations/').replace('/index.html', '/').replace('\\', '/')
                expected_url = f"https://dollarfence.com{expected_path}"
                
                # Find head section and add canonical URL
                head_pattern = r'(<head[^>]*>)'
                canonical_tag = f'\\1\n  <link rel="canonical" href="{expected_url}" />'
                
                if re.search(head_pattern, content):
                    content = re.sub(head_pattern, canonical_tag, content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ ADDED: {file_path}")
                    print(f"   Added canonical: {expected_url}")
                    fixed_count += 1
                else:
                    print(f"❌ NO HEAD TAG: {file_path}")
                    error_count += 1
        
        except Exception as e:
            print(f"❌ ERROR fixing {file_path}: {e}")
            error_count += 1
    
    print(f"\n=== FIX SUMMARY ===")
    print(f"Files fixed: {fixed_count}")
    print(f"Errors: {error_count}")
    
    return fixed_count

def verify_fixes():
    """Verify that canonical URLs are now correct"""
    
    print(f"\n=== VERIFYING FIXES ===")
    
    location_files = glob.glob("locations/**/*.html", recursive=True)
    verified_count = 0
    remaining_issues = 0
    
    for file_path in location_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract canonical URL
            canonical_match = re.search(r'<link rel="canonical" href="([^"]+)"', content)
            if canonical_match:
                canonical_url = canonical_match.group(1)
                
                # Determine expected URL from file path
                expected_path = file_path.replace('locations/', '/locations/')
                expected_path = expected_path.replace('/index.html', '/')
                expected_path = expected_path.replace('\\', '/')
                expected_url = f"https://dollarfence.com{expected_path}"
                
                if canonical_url == expected_url:
                    verified_count += 1
                else:
                    remaining_issues += 1
                    print(f"⚠️  STILL INCORRECT: {file_path}")
                    print(f"   Canonical: {canonical_url}")
                    print(f"   Expected:  {expected_url}")
            else:
                remaining_issues += 1
                print(f"⚠️  STILL MISSING: {file_path}")
        
        except Exception as e:
            print(f"❌ ERROR verifying {file_path}: {e}")
            remaining_issues += 1
    
    print(f"\n=== VERIFICATION SUMMARY ===")
    print(f"Correctly formatted: {verified_count}")
    print(f"Remaining issues: {remaining_issues}")
    print(f"Success rate: {verified_count/(verified_count+remaining_issues)*100:.1f}%")
    
    return remaining_issues == 0

def main():
    print("Starting canonical URL fix process...")
    
    # Change to website directory
    os.chdir('/home/ubuntu/dollar-fence-website')
    
    # Step 1: Scan for issues
    issues = scan_canonical_issues()
    
    if not issues:
        print("✅ No canonical URL issues found!")
        return
    
    # Step 2: Fix issues
    fixed_count = fix_canonical_urls(issues)
    
    if fixed_count > 0:
        print(f"\n🎉 Fixed {fixed_count} canonical URL issues!")
        
        # Step 3: Verify fixes
        success = verify_fixes()
        
        if success:
            print("✅ All canonical URLs are now correctly formatted!")
        else:
            print("⚠️  Some issues remain - manual review may be needed")
    else:
        print("❌ No fixes were applied - check for errors above")

if __name__ == "__main__":
    main()

