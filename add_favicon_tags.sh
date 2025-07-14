#!/bin/bash

# Script to add favicon meta tags to all HTML files in the Dollar Fence website

FAVICON_TAGS='  <!-- Favicon and SEO Meta Tags -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
  <link rel="icon" type="image/png" sizes="64x64" href="/favicon-64x64.png">
  <link rel="icon" type="image/png" sizes="128x128" href="/favicon-128x128.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#2d5016">
  <meta name="msapplication-TileColor" content="#2d5016">'

# Find all HTML files and add favicon tags if they don't already exist
find . -name "*.html" -type f | while read -r file; do
    # Check if favicon tags are already present
    if ! grep -q "favicon.ico" "$file"; then
        echo "Processing: $file"
        
        # Look for the pattern where we should insert favicon tags
        if grep -q '<link rel="preconnect" href="https://fonts.googleapis.com">' "$file"; then
            # Insert before Google Fonts
            sed -i '/<link rel="preconnect" href="https:\/\/fonts.googleapis.com">/i\
'"$FAVICON_TAGS"'\
' "$file"
        elif grep -q '<link rel="stylesheet"' "$file"; then
            # Insert before first stylesheet
            sed -i '0,/<link rel="stylesheet"/s//<link rel="stylesheet"/' "$file"
            sed -i '/<link rel="stylesheet"/i\
'"$FAVICON_TAGS"'\
' "$file"
        elif grep -q '</head>' "$file"; then
            # Insert before closing head tag as fallback
            sed -i '/<\/head>/i\
'"$FAVICON_TAGS"'\
' "$file"
        fi
    else
        echo "Favicon tags already present in: $file"
    fi
done

echo "Favicon tags added to all HTML files!"

