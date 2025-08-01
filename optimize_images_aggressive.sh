#!/bin/bash

# More aggressive image optimization script for Dollar Fence website
# Targets 100-150KB file sizes

echo "Starting aggressive image optimization for SEO..."

# List of JPEG files to further optimize
jpg_files=(
    "new-farm-fence-wire.jpg"
    "new-deer-fence-wire.jpg"
    "deer-fence-new.jpg"
    "farm-fench-ranch.jpg"
    "pool-fence-resort.jpg"
    "zinc-chain-link-fence.jpg"
    "new-wooden-ranch-fence.jpg"
    "pool-fence-house.jpg"
    "pool-fence-hotel.jpg"
    "farm-fence-new.jpg"
    "pool-fence-large-house.jpg"
    "black-vinyl-coated-chain-link-fence.jpg"
    "pool-fence-sports-club.jpg"
    "new-chain-link-fence.jpg"
)

cd assets/images

for jpg_file in "${jpg_files[@]}"; do
    if [ -f "$jpg_file" ]; then
        echo "Further optimizing $jpg_file"
        
        # Get current size
        size=$(stat -c%s "$jpg_file")
        size_kb=$((size / 1024))
        echo "Current size: ${size_kb}KB"
        
        # Create backup
        cp "$jpg_file" "${jpg_file}.backup"
        
        # If file is larger than 150KB, optimize more aggressively
        if [ $size_kb -gt 150 ]; then
            echo "Reducing to target 120KB..."
            
            # Try quality 50 first
            convert "${jpg_file}.backup" -quality 50 -strip -interlace Plane -resize 1200x800\> "$jpg_file"
            size=$(stat -c%s "$jpg_file")
            size_kb=$((size / 1024))
            echo "Quality 50 size: ${size_kb}KB"
            
            # If still too large, try quality 40
            if [ $size_kb -gt 150 ]; then
                echo "Still too large, trying quality 40..."
                convert "${jpg_file}.backup" -quality 40 -strip -interlace Plane -resize 1200x800\> "$jpg_file"
                size=$(stat -c%s "$jpg_file")
                size_kb=$((size / 1024))
                echo "Quality 40 size: ${size_kb}KB"
            fi
            
            # If still too large, try quality 35 with smaller dimensions
            if [ $size_kb -gt 150 ]; then
                echo "Still too large, trying quality 35 with smaller dimensions..."
                convert "${jpg_file}.backup" -quality 35 -strip -interlace Plane -resize 1000x700\> "$jpg_file"
                size=$(stat -c%s "$jpg_file")
                size_kb=$((size / 1024))
                echo "Quality 35 + resize size: ${size_kb}KB"
            fi
        fi
        
        # Remove backup
        rm "${jpg_file}.backup"
        
        echo "✅ Final optimized size: ${size_kb}KB"
        echo ""
    else
        echo "❌ File not found: $jpg_file"
    fi
done

echo "Aggressive image optimization complete!"

