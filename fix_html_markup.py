#!/usr/bin/env python3
"""
Fix Common HTML Markup Errors
Addresses typical validation issues found in website audits
"""

import os
import re
from pathlib import Path

def fix_html_file(file_path):
    """Fix common HTML markup errors in a single file"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_applied = []
        
        # Fix 1: Ensure proper DOCTYPE declaration
        if not content.strip().startswith('<!DOCTYPE html>'):
            if '<!DOCTYPE' in content:
                content = re.sub(r'<!DOCTYPE[^>]*>', '<!DOCTYPE html>', content)
                fixes_applied.append("Fixed DOCTYPE declaration")
        
        # Fix 2: Remove duplicate IDs (common cause of validation errors)
        id_pattern = r'id="([^"]+)"'
        ids_found = re.findall(id_pattern, content)
        duplicate_ids = set([x for x in ids_found if ids_found.count(x) > 1])
        
        for dup_id in duplicate_ids:
            # Replace duplicate IDs with unique ones
            count = 0
            def replace_duplicate_id(match):
                nonlocal count
                count += 1
                if count == 1:
                    return match.group(0)  # Keep first occurrence
                else:
                    return f'id="{match.group(1)}-{count}"'
            
            content = re.sub(f'id="{re.escape(dup_id)}"', replace_duplicate_id, content)
            fixes_applied.append(f"Fixed duplicate ID: {dup_id}")
        
        # Fix 3: Ensure alt attributes on images
        img_without_alt = r'<img(?![^>]*alt=)[^>]*>'
        if re.search(img_without_alt, content):
            content = re.sub(r'<img([^>]*?)(?<!alt="[^"]*")>', r'<img\1 alt="">', content)
            fixes_applied.append("Added missing alt attributes to images")
        
        # Fix 4: Fix unclosed meta tags (should be self-closing)
        content = re.sub(r'<meta([^>]*?)(?<!/)>', r'<meta\1/>', content)
        
        # Fix 5: Fix unclosed link tags (should be self-closing)
        content = re.sub(r'<link([^>]*?)(?<!/)>', r'<link\1/>', content)
        
        # Fix 6: Ensure proper lang attribute on html tag
        if '<html>' in content:
            content = content.replace('<html>', '<html lang="en">')
            fixes_applied.append("Added lang attribute to html tag")
        
        # Fix 7: Remove any stray closing tags without opening tags
        # This is a simplified approach - in practice, you'd need more sophisticated parsing
        
        # Fix 8: Ensure proper encoding declaration
        if '<meta charset=' not in content and '<meta http-equiv="Content-Type"' not in content:
            # Add charset declaration after <head>
            content = content.replace('<head>', '<head>\n  <meta charset="UTF-8">')
            fixes_applied.append("Added charset declaration")
        
        # Fix 9: Remove empty href attributes
        content = re.sub(r'href=""', 'href="#"', content)
        
        # Fix 10: Ensure proper nesting of elements (basic check)
        # Remove any obvious nesting issues like <p><div></div></p>
        content = re.sub(r'<p>(\s*<div[^>]*>.*?</div>\s*)</p>', r'\1', content, flags=re.DOTALL)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return fixes_applied
        else:
            return []
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def fix_all_html_files():
    """Fix HTML markup errors in all HTML files"""
    
    print("=== HTML MARKUP FIX ===")
    print("Scanning for HTML files...")
    
    html_files = []
    
    # Find all HTML files
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files")
    
    total_fixes = 0
    files_fixed = 0
    
    for file_path in html_files:
        fixes = fix_html_file(file_path)
        if fixes:
            files_fixed += 1
            total_fixes += len(fixes)
            print(f"✅ {file_path}: {len(fixes)} fixes applied")
            for fix in fixes[:3]:  # Show first 3 fixes
                print(f"   - {fix}")
            if len(fixes) > 3:
                print(f"   - ... and {len(fixes) - 3} more fixes")
        else:
            print(f"✓ {file_path}: No issues found")
    
    print(f"\n=== SUMMARY ===")
    print(f"Files processed: {len(html_files)}")
    print(f"Files fixed: {files_fixed}")
    print(f"Total fixes applied: {total_fixes}")
    
    return files_fixed, total_fixes

def validate_sample_files():
    """Validate a sample of fixed files"""
    print("\n=== VALIDATION ===")
    
    # Check a few key files
    key_files = ['index.html', 'about/index.html', 'contact/index.html']
    
    for file_path in key_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            
            # Check for common issues
            if not content.strip().startswith('<!DOCTYPE html>'):
                issues.append("Missing or incorrect DOCTYPE")
            
            if '<html lang=' not in content:
                issues.append("Missing lang attribute")
            
            if '<meta charset=' not in content:
                issues.append("Missing charset declaration")
            
            # Check for duplicate IDs
            ids = re.findall(r'id="([^"]+)"', content)
            duplicates = set([x for x in ids if ids.count(x) > 1])
            if duplicates:
                issues.append(f"Duplicate IDs: {', '.join(duplicates)}")
            
            if issues:
                print(f"⚠️  {file_path}: {len(issues)} remaining issues")
                for issue in issues:
                    print(f"   - {issue}")
            else:
                print(f"✅ {file_path}: Validation passed")

if __name__ == "__main__":
    files_fixed, total_fixes = fix_all_html_files()
    
    if files_fixed > 0:
        validate_sample_files()
        print(f"\n🎉 HTML markup fixes completed!")
        print(f"This should resolve many of the 978 markup errors reported in the site audit.")
    else:
        print("No HTML markup issues found to fix.")

