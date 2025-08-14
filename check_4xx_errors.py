#!/usr/bin/env python3
"""
Check for 4XX Status Code Issues
Identifies broken links and pages that return 4XX errors
"""

import requests
import xml.etree.ElementTree as ET
import time
from urllib.parse import urljoin, urlparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_sitemap_urls():
    """Extract all URLs from the sitemap"""
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        
        urls = []
        for url in root.findall('url'):
            loc = url.find('loc')
            if loc is not None and loc.text:
                urls.append(loc.text)
        
        return urls
    except Exception as e:
        print(f"Error reading sitemap: {e}")
        return []

def check_url_status(url):
    """Check the HTTP status of a single URL"""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return {
            'url': url,
            'status_code': response.status_code,
            'final_url': response.url,
            'redirected': url != response.url,
            'error': None
        }
    except requests.exceptions.RequestException as e:
        return {
            'url': url,
            'status_code': None,
            'final_url': None,
            'redirected': False,
            'error': str(e)
        }

def check_all_urls(urls, max_workers=10):
    """Check status codes for all URLs"""
    print(f"Checking {len(urls)} URLs for 4XX errors...")
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(check_url_status, url): url for url in urls}
        
        for i, future in enumerate(as_completed(future_to_url)):
            result = future.result()
            results.append(result)
            
            if (i + 1) % 50 == 0:
                print(f"Progress: {i + 1}/{len(urls)} URLs checked")
            
            # Be respectful to the server
            time.sleep(0.1)
    
    return results

def analyze_results(results):
    """Analyze the results and identify issues"""
    
    # Categorize results
    success_codes = [200, 201, 202, 204, 301, 302, 303, 307, 308]
    client_errors = []  # 4XX codes
    server_errors = []  # 5XX codes
    network_errors = []
    redirects = []
    
    for result in results:
        status = result['status_code']
        
        if result['error']:
            network_errors.append(result)
        elif status and 400 <= status < 500:
            client_errors.append(result)
        elif status and 500 <= status < 600:
            server_errors.append(result)
        elif result['redirected']:
            redirects.append(result)
    
    print(f"\n=== STATUS CODE ANALYSIS ===")
    print(f"Total URLs checked: {len(results)}")
    print(f"4XX Client Errors: {len(client_errors)}")
    print(f"5XX Server Errors: {len(server_errors)}")
    print(f"Network Errors: {len(network_errors)}")
    print(f"Redirects: {len(redirects)}")
    
    # Show 4XX errors in detail
    if client_errors:
        print(f"\n=== 4XX CLIENT ERRORS ({len(client_errors)}) ===")
        for error in client_errors[:20]:  # Show first 20
            print(f"❌ {error['status_code']} - {error['url']}")
        
        if len(client_errors) > 20:
            print(f"... and {len(client_errors) - 20} more 4XX errors")
    
    # Show server errors
    if server_errors:
        print(f"\n=== 5XX SERVER ERRORS ({len(server_errors)}) ===")
        for error in server_errors:
            print(f"🔥 {error['status_code']} - {error['url']}")
    
    # Show network errors
    if network_errors:
        print(f"\n=== NETWORK ERRORS ({len(network_errors)}) ===")
        for error in network_errors[:10]:  # Show first 10
            print(f"🌐 {error['url']} - {error['error']}")
    
    return {
        'client_errors': client_errors,
        'server_errors': server_errors,
        'network_errors': network_errors,
        'redirects': redirects
    }

def generate_fixes(analysis):
    """Generate recommendations for fixing issues"""
    
    fixes = []
    client_errors = analysis['client_errors']
    
    if client_errors:
        print(f"\n=== RECOMMENDED FIXES ===")
        
        # Group by status code
        by_status = {}
        for error in client_errors:
            status = error['status_code']
            if status not in by_status:
                by_status[status] = []
            by_status[status].append(error['url'])
        
        for status_code, urls in by_status.items():
            print(f"\n{status_code} Errors ({len(urls)} URLs):")
            
            if status_code == 404:
                fixes.append({
                    'issue': f'{len(urls)} pages return 404 Not Found',
                    'action': 'Remove from sitemap or create missing pages',
                    'urls': urls[:10]  # First 10 URLs
                })
                print("  → Remove these URLs from sitemap.xml")
                print("  → Or create the missing pages if they should exist")
                
            elif status_code == 403:
                fixes.append({
                    'issue': f'{len(urls)} pages return 403 Forbidden',
                    'action': 'Check server permissions and access controls',
                    'urls': urls[:10]
                })
                print("  → Check server permissions")
                print("  → Review access controls")
                
            elif status_code == 410:
                fixes.append({
                    'issue': f'{len(urls)} pages return 410 Gone',
                    'action': 'Remove from sitemap - pages intentionally deleted',
                    'urls': urls[:10]
                })
                print("  → Remove from sitemap (pages intentionally deleted)")
            
            # Show sample URLs
            for url in urls[:5]:
                print(f"    - {url}")
            if len(urls) > 5:
                print(f"    ... and {len(urls) - 5} more")
    
    return fixes

def create_sitemap_without_4xx(original_urls, client_errors):
    """Create a cleaned sitemap without 4XX error URLs"""
    
    error_urls = set(error['url'] for error in client_errors)
    clean_urls = [url for url in original_urls if url not in error_urls]
    
    print(f"\nCreating cleaned sitemap...")
    print(f"Original URLs: {len(original_urls)}")
    print(f"URLs with 4XX errors: {len(error_urls)}")
    print(f"Clean URLs: {len(clean_urls)}")
    
    # Create new sitemap XML
    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    current_date = time.strftime('%Y-%m-%d')
    
    for url in clean_urls:
        url_elem = ET.SubElement(root, 'url')
        
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = url
        
        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = current_date
        
        changefreq = ET.SubElement(url_elem, 'changefreq')
        changefreq.text = 'weekly'
        
        priority = ET.SubElement(url_elem, 'priority')
        # Set priority based on URL type
        if '/locations/' in url:
            if any(city in url.lower() for city in ['new-york', 'los-angeles', 'chicago', 'houston']):
                priority.text = '0.9'
            else:
                priority.text = '0.8'
        elif url.endswith('.com/'):
            priority.text = '1.0'
        else:
            priority.text = '0.8'
    
    # Write cleaned sitemap
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write('sitemap_clean.xml', encoding='UTF-8', xml_declaration=True)
    
    print(f"✅ Created sitemap_clean.xml with {len(clean_urls)} URLs")
    return 'sitemap_clean.xml'

def main():
    print("=== 4XX STATUS CODE CHECK ===")
    
    # Get URLs from sitemap
    urls = get_sitemap_urls()
    if not urls:
        print("❌ No URLs found in sitemap")
        return
    
    print(f"Found {len(urls)} URLs in sitemap")
    
    # Check all URLs
    results = check_all_urls(urls)
    
    # Analyze results
    analysis = analyze_results(results)
    
    # Generate fixes
    fixes = generate_fixes(analysis)
    
    # Save detailed results
    with open('4xx_check_results.json', 'w') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_urls': len(urls),
            'analysis': analysis,
            'fixes': fixes
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: 4xx_check_results.json")
    
    # Create cleaned sitemap if there are 4XX errors
    if analysis['client_errors']:
        create_sitemap_without_4xx(urls, analysis['client_errors'])
        print("\n🔧 To fix 4XX errors:")
        print("1. Review the URLs with errors")
        print("2. Either create missing pages or remove URLs from sitemap")
        print("3. Replace sitemap.xml with sitemap_clean.xml if appropriate")
    else:
        print("\n✅ No 4XX errors found! Sitemap is clean.")

if __name__ == "__main__":
    main()

