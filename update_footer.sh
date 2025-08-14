#!/bin/bash

# Script to add privacy policy and terms links to footer copyright text

echo "Updating footer copyright text in all HTML files..."

# Find all HTML files with the copyright text and update them
find . -name "*.html" -exec grep -l "2024 Dollar Fence" {} \; | while read file; do
    echo "Updating: $file"
    
    # Replace the copyright line with the new version that includes privacy and terms links
    sed -i 's/<p>&copy; 2024 Dollar Fence\. All rights reserved\.<\/p>/<p>\&copy; 2024 Dollar Fence. All rights reserved. | <a href="\/privacy\/">Privacy Policy<\/a> | <a href="\/terms\/">Terms \& Conditions<\/a><\/p>/g' "$file"
done

echo "Footer update complete!"
echo "Updated files:"
find . -name "*.html" -exec grep -l "Privacy Policy.*Terms" {} \; | wc -l
echo "files now contain the privacy and terms links."

