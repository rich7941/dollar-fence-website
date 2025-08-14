#!/usr/bin/env python3
"""
XML Sitemap Optimization Script for Complete Dollar Fence Backup (498 pages)
Optimizes priority and change frequency for all location pages to accelerate Google indexing
"""

import xml.etree.ElementTree as ET
from datetime import datetime

# Define major metropolitan markets (Tier 1 - Priority 0.9)
TIER_1_MARKETS = [
    'new-york', 'los-angeles', 'chicago', 'houston', 'phoenix', 'philadelphia',
    'san-antonio', 'san-diego', 'dallas', 'san-jose', 'austin', 'jacksonville',
    'fort-worth', 'columbus', 'charlotte', 'san-francisco', 'indianapolis',
    'seattle', 'denver', 'washington', 'boston', 'el-paso', 'nashville',
    'detroit', 'oklahoma-city', 'portland', 'las-vegas', 'memphis', 'louisville',
    'baltimore', 'milwaukee', 'albuquerque', 'tucson', 'fresno', 'sacramento',
    'mesa', 'kansas-city', 'atlanta', 'long-beach', 'colorado-springs',
    'raleigh', 'miami', 'virginia-beach', 'omaha', 'oakland', 'minneapolis',
    'tulsa', 'arlington', 'tampa', 'new-orleans', 'greater-boston', 'twin-cities'
]

def optimize_sitemap():
    """Optimize the sitemap with strategic priority and frequency settings"""
    
    # Parse the existing sitemap
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    
    # Define namespace
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    # Get current date for lastmod
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Track changes
    changes_made = 0
    tier_1_count = 0
    tier_2_count = 0
    
    # Process each URL
    for url in root.findall('ns:url', namespace):
        loc = url.find('ns:loc', namespace)
        if loc is None:
            continue
            
        url_path = loc.text
        
        # Skip non-location pages
        if '/locations/' not in url_path:
            continue
            
        # Get existing elements
        lastmod = url.find('ns:lastmod', namespace)
        changefreq = url.find('ns:changefreq', namespace)
        priority = url.find('ns:priority', namespace)
        
        # Update lastmod to current date
        if lastmod is not None:
            lastmod.text = current_date
        
        # Determine if this is a Tier 1 market
        is_tier_1 = any(market in url_path.lower() for market in TIER_1_MARKETS)
        
        # Update changefreq to weekly for all location pages
        if changefreq is not None:
            if changefreq.text == 'monthly':
                changefreq.text = 'weekly'
                changes_made += 1
        
        # Update priority based on market tier
        if priority is not None:
            old_priority = priority.text
            if is_tier_1:
                priority.text = '0.9'
                tier_1_count += 1
            elif url_path.endswith('/locations/'):
                # Main locations page stays high priority
                priority.text = '0.9'
            else:
                # Secondary markets get 0.8
                priority.text = '0.8'
                tier_2_count += 1
            
            if old_priority != priority.text:
                changes_made += 1
                print(f"Updated {url_path}: priority {old_priority} -> {priority.text}")
    
    # Save the optimized sitemap
    tree.write('sitemap.xml', encoding='UTF-8', xml_declaration=True)
    
    print(f"\n=== SITEMAP OPTIMIZATION COMPLETE ===")
    print(f"Total changes made: {changes_made}")
    print(f"Updated lastmod dates to: {current_date}")
    print(f"Changed location page frequency from 'monthly' to 'weekly'")
    print(f"Tier 1 markets (priority 0.9): {tier_1_count}")
    print(f"Tier 2 markets (priority 0.8): {tier_2_count}")
    print(f"Total location pages optimized: {tier_1_count + tier_2_count}")
    
    return changes_made

if __name__ == "__main__":
    print("Starting sitemap optimization for complete 498-page backup...")
    optimize_sitemap()

