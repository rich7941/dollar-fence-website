#!/bin/bash

# Script to update all fence type page titles to exact keyword format
# Format: [Fence Type] Fence Company | Dollar Fence

echo "Updating fence type page titles to exact keyword format..."

# Vinyl Fence
sed -i 's/<title>Vinyl Fence Installation | Premium Vinyl Fencing | Dollar Fence<\/title>/<title>Vinyl Fence Company | Dollar Fence<\/title>/' ./fence-types/vinyl-fence/index.html

# Wood Fence  
sed -i 's/<title>Wood Fence Installation | Premium Wood Fencing | Dollar Fence<\/title>/<title>Wood Fence Company | Dollar Fence<\/title>/' ./fence-types/wood-fence/index.html

# Chain Link Fence
sed -i 's/<title>Chain Link Fence Installation | Affordable & Durable | Dollar Fence<\/title>/<title>Chain Link Fence Company | Dollar Fence<\/title>/' ./fence-types/chain-link-fence/index.html

# Dog Fence
sed -i 's/<title>Dog Fence Installation | Pet Fencing Solutions | Dollar Fence<\/title>/<title>Dog Fence Company | Dollar Fence<\/title>/' ./fence-types/dog-fence/index.html

# Gates & Entry
sed -i 's/<title>Gates & Entry Installation | Premium Gate Systems | Dollar Fence<\/title>/<title>Gates & Entry Company | Dollar Fence<\/title>/' ./fence-types/gates-entry/index.html

# Commercial Fence
sed -i 's/<title>Commercial Fence Installation | Business Fencing Solutions | Dollar Fence<\/title>/<title>Commercial Fence Company | Dollar Fence<\/title>/' ./fence-types/commercial-fence/index.html

# Agricultural Fence
sed -i 's/<title>Agricultural Fence Installation | Farm & Ranch Fencing | Dollar Fence<\/title>/<title>Agricultural Fence Company | Dollar Fence<\/title>/' ./fence-types/agricultural-fence/index.html

# Steel Fence
sed -i 's/<title>Steel Fence Installation | Ornamental Steel Fencing | Dollar Fence<\/title>/<title>Steel Fence Company | Dollar Fence<\/title>/' ./fence-types/steel-fence/index.html

# Aluminum Fence
sed -i 's/<title>Aluminum Fence Installation | Premium Aluminum Fencing | Dollar Fence<\/title>/<title>Aluminum Fence Company | Dollar Fence<\/title>/' ./fence-types/aluminum-fence/index.html

# Pool Fence
sed -i 's/<title>Pool Fence Installation | Premium Pool Fencing | Dollar Fence<\/title>/<title>Pool Fence Company | Dollar Fence<\/title>/' ./fence-types/pool-fence/index.html

# Deer Fence
sed -i 's/<title>Deer Fence Installation | Wildlife Protection Fencing | Dollar Fence<\/title>/<title>Deer Fence Company | Dollar Fence<\/title>/' ./fence-types/deer-fence/index.html

# Hardwood Fence
sed -i 's/<title>Hardwood Fence Installation | Premium Hardwood Fencing | Dollar Fence<\/title>/<title>Hardwood Fence Company | Dollar Fence<\/title>/' ./fence-types/hardwood-fence/index.html

# Trex Fence
sed -i 's/<title>Trex Fence Installation | Premium Trex Fencing | Dollar Fence<\/title>/<title>Trex Fence Company | Dollar Fence<\/title>/' ./fence-types/trex-fence/index.html

echo "All fence type page titles updated successfully!"
echo "Updated pages:"
echo "- Vinyl Fence Company"
echo "- Wood Fence Company"
echo "- Chain Link Fence Company"
echo "- Dog Fence Company"
echo "- Gates & Entry Company"
echo "- Commercial Fence Company"
echo "- Agricultural Fence Company"
echo "- Steel Fence Company"
echo "- Aluminum Fence Company"
echo "- Pool Fence Company"
echo "- Deer Fence Company"
echo "- Hardwood Fence Company"
echo "- Trex Fence Company"

