#!/usr/bin/env python3
"""
Check for 4XX Status Code Issues - Fixed Version
Properly handles XML namespaces
"""

import requests
import xml.etree.ElementTree as ET
import time
from urllib.parse import urljoin, urlparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_sitemap_urls():
    """Extract all URLs from the sitemap with proper namespace handling"""
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        
        # Handle namespace
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = []
        # Try with namespace first
        for url in root.findall('ns:url', namespace):
            loc = url.find('ns:loc', namespace)
            if loc is not None and loc.text:
                urls.append(loc.text)
        
        # If no URLs found with namespace, try without
        if not urls:
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
        response = requests.get(url, timeout=10, allow_redirects=True)
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

def check_sample_urls(urls, sample_size=50):
    """Check a sample of URLs to identify patterns"""
    print(f"Checking sample of {min(sample_size, len(urls))} URLs...")
    
    # Take a representative sample
    sample_urls = urls[:sample_size] if len(urls) <= sample_size else urls[::len(urls)//sample_size][:sample_size]
    
    results = []
    for i, url in enumerate(sample_urls):
        result = check_url_status(url)
        results.append(result)
        
        status_icon = "✅" if result['status_code'] == 200 else "❌"
        print(f"{status_icon} {result['status_code']} - {url}")
        
        # Be respectful to the server
        time.sleep(0.2)
    
    return results

def analyze_sample_results(results):
    """Analyze sample results to identify patterns"""
    
    # Categorize results
    success_codes = [200, 201, 202, 204]
    redirect_codes = [301, 302, 303, 307, 308]
    client_errors = []  # 4XX codes
    server_errors = []  # 5XX codes
    network_errors = []
    successful = []
    redirects = []
    
    for result in results:
        status = result['status_code']
        
        if result['error']:
            network_errors.append(result)
        elif status in success_codes:
            successful.append(result)
        elif status in redirect_codes:
            redirects.append(result)
        elif status and 400 <= status < 500:
            client_errors.append(result)
        elif status and 500 <= status < 600:
            server_errors.append(result)
    
    print(f"\n=== SAMPLE ANALYSIS ===")
    print(f"Sample size: {len(results)}")
    print(f"✅ Successful (2XX): {len(successful)}")
    print(f"🔄 Redirects (3XX): {len(redirects)}")
    print(f"❌ Client Errors (4XX): {len(client_errors)}")
    print(f"🔥 Server Errors (5XX): {len(server_errors)}")
    print(f"🌐 Network Errors: {len(network_errors)}")
    
    # Show specific 4XX errors
    if client_errors:
        print(f"\n=== 4XX ERRORS FOUND ===")
        for error in client_errors:
            print(f"❌ {error['status_code']} - {error['url']}")
    
    # Show network errors
    if network_errors:
        print(f"\n=== NETWORK ERRORS ===")
        for error in network_errors:
            print(f"🌐 {error['url']} - {error['error']}")
    
    return {
        'successful': successful,
        'redirects': redirects,
        'client_errors': client_errors,
        'server_errors': server_errors,
        'network_errors': network_errors
    }

def estimate_full_site_issues(sample_analysis, total_urls):
    """Estimate issues across the full site based on sample"""
    
    sample_size = len(sample_analysis['successful']) + len(sample_analysis['redirects']) + \
                  len(sample_analysis['client_errors']) + len(sample_analysis['server_errors']) + \
                  len(sample_analysis['network_errors'])
    
    if sample_size == 0:
        return
    
    # Calculate percentages
    error_rate = len(sample_analysis['client_errors']) / sample_size
    server_error_rate = len(sample_analysis['server_errors']) / sample_size
    
    estimated_4xx = int(error_rate * total_urls)
    estimated_5xx = int(server_error_rate * total_urls)
    
    print(f"\n=== ESTIMATED FULL SITE ISSUES ===")
    print(f"Total URLs in sitemap: {total_urls}")
    print(f"Estimated 4XX errors: {estimated_4xx} ({error_rate:.1%})")
    print(f"Estimated 5XX errors: {estimated_5xx} ({server_error_rate:.1%})")
    
    if estimated_4xx > 0:
        print(f"\n🔧 RECOMMENDED ACTIONS:")
        print(f"1. Review the {len(sample_analysis['client_errors'])} 4XX errors found in sample")
        print(f"2. If pattern is consistent, expect ~{estimated_4xx} total 4XX errors")
        print(f"3. Remove broken URLs from sitemap or fix the pages")
        print(f"4. This should improve your Site Health Score significantly")

def main():
    print("=== 4XX STATUS CODE CHECK (SAMPLE) ===")
    
    # Get URLs from sitemap
    urls = get_sitemap_urls()
    if not urls:
        print("❌ No URLs found in sitemap")
        return
    
    print(f"Found {len(urls)} URLs in sitemap")
    
    # Check sample of URLs (faster than checking all)
    sample_results = check_sample_urls(urls, sample_size=50)
    
    # Analyze sample results
    analysis = analyze_sample_results(sample_results)
    
    # Estimate full site issues
    estimate_full_site_issues(analysis, len(urls))
    
    # Save results
    with open('4xx_sample_results.json', 'w') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_urls': len(urls),
            'sample_size': len(sample_results),
            'analysis': analysis
        }, f, indent=2, default=str)
    
    print(f"\n📄 Sample results saved to: 4xx_sample_results.json")
    
    # Provide specific recommendations
    if analysis['client_errors']:
        print(f"\n⚠️  IMMEDIATE ACTION NEEDED:")
        print(f"Found {len(analysis['client_errors'])} 4XX errors in sample")
        print(f"These URLs should be removed from sitemap or fixed:")
        for error in analysis['client_errors']:
            print(f"  - {error['url']} (HTTP {error['status_code']})")
    else:
        print(f"\n✅ No 4XX errors found in sample!")
        print(f"Your sitemap appears to be clean.")

if __name__ == "__main__":
    main()

