#!/bin/bash

# Image optimization script for Dollar Fence website
# Converts large PNG files to optimized JPEG format targeting 100-150KB

echo "Starting image optimization for SEO..."

# List of PNG files to optimize
png_files=(
    "new-farm-fence-wire.png"
    "new-deer-fence-wire.png"
    "deer-fence-new.png"
    "farm-fence-ranch.png"
    "pool-fence-resort.png"
    "zinc-chain-link-fence.png"
    "new-wooden-ranch-fence.png"
    "pool-fence-house.png"
    "pool-fence-hotel.png"
    "farm-fence-new.png"
    "pool-fence-large-house.png"
    "black-vinyl-coated-chain-link-fence.png"
    "pool-fence-sports-club.png"
    "new-chain-link-fence.png"
)

cd assets/images

for png_file in "${png_files[@]}"; do
    if [ -f "$png_file" ]; then
        # Get base name without extension
        base_name="${png_file%.png}"
        jpg_file="${base_name}.jpg"
        
        echo "Optimizing $png_file -> $jpg_file"
        
        # Convert PNG to JPEG with optimization
        # Start with quality 85 and adjust if needed
        convert "$png_file" -quality 85 -strip -interlace Plane "$jpg_file"
        
        # Check file size and adjust quality if needed
        size=$(stat -c%s "$jpg_file")
        size_kb=$((size / 1024))
        
        echo "Initial size: ${size_kb}KB"
        
        # If file is too large, reduce quality
        if [ $size_kb -gt 150 ]; then
            echo "File too large, reducing quality to 75..."
            convert "$png_file" -quality 75 -strip -interlace Plane "$jpg_file"
            size=$(stat -c%s "$jpg_file")
            size_kb=$((size / 1024))
            echo "New size: ${size_kb}KB"
        fi
        
        # If still too large, reduce quality further
        if [ $size_kb -gt 150 ]; then
            echo "File still too large, reducing quality to 65..."
            convert "$png_file" -quality 65 -strip -interlace Plane "$jpg_file"
            size=$(stat -c%s "$jpg_file")
            size_kb=$((size / 1024))
            echo "Final size: ${size_kb}KB"
        fi
        
        echo "✅ Optimized $png_file -> $jpg_file (${size_kb}KB)"
        echo ""
    else
        echo "❌ File not found: $png_file"
    fi
done

echo "Image optimization complete!"

