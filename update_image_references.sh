#!/bin/bash

# Script to update image references from PNG to JPG in HTML files

echo "Updating image references from PNG to JPG..."

# List of image name changes (without extension)
images=(
    "new-farm-fence-wire"
    "new-deer-fence-wire"
    "deer-fence-new"
    "farm-fench-ranch"
    "pool-fence-resort"
    "zinc-chain-link-fence"
    "new-wooden-ranch-fence"
    "pool-fence-house"
    "pool-fence-hotel"
    "farm-fence-new"
    "pool-fence-large-house"
    "black-vinyl-coated-chain-link-fence"
    "pool-fence-sports-club"
    "new-chain-link-fence"
)

# Find all HTML files and update image references
for image in "${images[@]}"; do
    echo "Updating references for $image..."
    
    # Update in all HTML files
    find . -name "*.html" -type f -exec sed -i "s/${image}\.png/${image}.jpg/g" {} \;
    
    # Update in CSS files
    find . -name "*.css" -type f -exec sed -i "s/${image}\.png/${image}.jpg/g" {} \;
    
    echo "✅ Updated $image.png -> $image.jpg"
done

echo "Image reference updates complete!"

