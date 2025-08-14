#!/bin/bash

# Script to fix FontAwesome CORS issues by replacing kit script with standard CDN

echo "Fixing FontAwesome CORS issues in all HTML files..."

# Find all HTML files and replace the FontAwesome kit script
find . -name "*.html" -type f -exec sed -i 's|<!-- Font Awesome for icons -->|<!-- Font Awesome CSS -->|g' {} \;
find . -name "*.html" -type f -exec sed -i 's|<script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>|<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />|g' {} \;

echo "FontAwesome fix completed!"
echo "Checking remaining files with kit.fontawesome.com..."
find . -name "*.html" -exec grep -l "kit.fontawesome.com" {} \;

if [ $? -eq 0 ]; then
    echo "Some files still contain kit.fontawesome.com references"
else
    echo "All FontAwesome kit references have been successfully replaced!"
fi

