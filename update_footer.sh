#!/bin/bash

# Define the new footer content
NEW_FOOTER='          <h4>Fence Types</h4>
          <ul>
            <li><a href="/fence-types/vinyl-fence/">Vinyl Fence</a></li>
            <li><a href="/fence-types/wood-fence/">Wood Fence</a></li>
            <li><a href="/fence-types/chain-link-fence/">Chain Link Fence</a></li>
            <li><a href="/fence-types/dog-fence/">Dog Fence</a></li>
            <li><a href="/fence-types/gates-entry/">Gates & Entry</a></li>
            <li><a href="/fence-types/commercial-fence/">Commercial Fence</a></li>
            <li><a href="/fence-types/agricultural-fence/">Agricultural Fence</a></li>
            <li><a href="/fence-types/steel-fence/">Steel Fence</a></li>
            <li><a href="/fence-types/aluminum-fence/">Aluminum Fence</a></li>
            <li><a href="/fence-types/pool-fence/">Pool Fence</a></li>
            <li><a href="/fence-types/deer-fence/">Deer Fence</a></li>
            <li><a href="/fence-types/hardwood-fence/">Hardwood Fence</a></li>
            <li><a href="/fence-types/trex-fence/">Trex Fence</a></li>
          </ul>'

# Find all HTML files and update the footer section
find . -name "*.html" -exec sed -i '/^[[:space:]]*<h4>Fence Types<\/h4>/,/^[[:space:]]*<\/ul>/{
  /^[[:space:]]*<h4>Fence Types<\/h4>/!{
    /^[[:space:]]*<\/ul>/!d
  }
}' {} \;

echo "Footer sections updated successfully!"
