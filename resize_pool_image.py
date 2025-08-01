#!/usr/bin/env python3
"""
Script to crop and resize the pool fence image to match other fence thumbnails
"""

from PIL import Image
import os

def resize_pool_fence_image():
    """Crop and resize the pool fence image to match other fence thumbnails"""
    
    # Input and output paths (relative to script location)
    script_dir = os.path.dirname(__file__)
    input_path = os.path.join(script_dir, "assets", "images", "pool-fence-resort.jpg")
    backup_path = os.path.join(script_dir, "assets", "images", "pool-fence-resort-original.jpg")
    
    # Create backup if it doesn't exist
    if not os.path.exists(backup_path):
        print("Creating backup of original image...")
        original = Image.open(input_path)
        original.save(backup_path, "JPEG", quality=95)
        print(f"Backup saved to: {backup_path}")
    
    # Open the image
    print("Opening pool fence image...")
    img = Image.open(input_path)
    print(f"Original dimensions: {img.size}")
    
    # The image is 800x600. Let's crop it to focus more on the fence
    # and less on the tall palm trees and buildings
    # We'll crop from the bottom portion to focus on the fence and pool area
    
    # Crop parameters (left, top, right, bottom)
    # Focus on the fence and pool area, reducing the tall palm trees
    crop_box = (0, 150, 800, 600)  # Remove top 150 pixels with tall palm trees
    
    print("Cropping image to focus on fence area...")
    cropped = img.crop(crop_box)
    print(f"Cropped dimensions: {cropped.size}")
    
    # Resize back to 800x600 to maintain consistency
    print("Resizing to standard 800x600...")
    # Handle Pillow version compatibility
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.LANCZOS
    resized = cropped.resize((800, 600), resample)
    print(f"Final dimensions: {resized.size}")
    
    # Save the processed image
    print("Saving processed image...")
    resized.save(input_path, "JPEG", quality=95, optimize=True)
    
    print("✅ Pool fence image successfully processed!")
    print(f"✅ Original backed up to: {backup_path}")
    print(f"✅ Updated image saved to: {input_path}")
    
    return True

if __name__ == "__main__":
    try:
        resize_pool_fence_image()
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        exit(1)

