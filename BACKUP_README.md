# Dollar Fence Website - Complete Backup

This is a complete backup of the Dollar Fence website (https://dollarfence.com) that includes all source code, assets, and external dependencies needed for full duplication.

## What's Included

### Core Website Files
- **HTML Pages**: All main pages including index.html, gallery.html, success.html
- **CSS Stylesheets**: Custom styles in assets/css/
- **Images**: All website images in assets/images/ (217+ files)
- **JavaScript**: Any custom scripts and functionality
- **Configuration**: netlify.toml, site.webmanifest, sitemap.xml
- **Favicons**: Complete set of favicon files for all devices

### External Dependencies (Self-Contained)
- **Google Fonts**: Inter font family (400, 500, 600, 700 weights)
  - Located in: `external-assets/fonts/`
  - Includes both CSS and font files (.ttf)
- **Font Awesome**: Complete icon font library (v6.5.1)
  - Located in: `external-assets/fontawesome/`
  - Includes CSS and all webfont files (.woff2, .ttf)

### Directory Structure
```
dollar-fence-website/
├── index.html                 # Main homepage
├── gallery.html              # Gallery page
├── success.html               # Success/thank you page
├── sitemap.xml               # SEO sitemap
├── netlify.toml              # Netlify configuration
├── site.webmanifest          # PWA manifest
├── favicon files             # Complete favicon set
├── assets/
│   ├── css/                  # Custom stylesheets
│   └── images/               # All website images
├── about/                    # About page
├── contact/                  # Contact page
├── fence-types/              # Fence type pages
├── locations/                # Location pages
├── privacy/                  # Privacy policy
├── reviews/                  # Reviews page
├── terms/                    # Terms of service
├── external-assets/          # Downloaded external dependencies
│   ├── fonts/               # Google Fonts (Inter)
│   └── fontawesome/         # Font Awesome icons
└── scripts/                  # Utility scripts
```

## How to Use This Backup

### Option 1: Direct Deployment
1. Extract the ZIP file to your web server directory
2. Point your domain to the extracted folder
3. The site should work immediately with all assets

### Option 2: Netlify Deployment
1. Extract the ZIP file
2. Upload to a new Git repository
3. Connect the repository to Netlify
4. Deploy using the included netlify.toml configuration

### Option 3: Local Development
1. Extract the ZIP file
2. Open index.html in a web browser
3. For full functionality, serve via a local web server:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   ```

## Making It Self-Contained

To use the downloaded external assets instead of CDNs:

1. **Update Google Fonts References**:
   Replace CDN links in HTML files:
   ```html
   <!-- Replace this -->
   <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
   
   <!-- With this -->
   <link href="external-assets/fonts/inter.css" rel="stylesheet">
   ```

2. **Update Font Awesome References**:
   Replace CDN links in HTML files:
   ```html
   <!-- Replace this -->
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
   
   <!-- With this -->
   <link rel="stylesheet" href="external-assets/fontawesome/fontawesome.css">
   ```

## Technical Details

- **Total Files**: 320+ files
- **Repository**: https://github.com/rich7941/dollar-fence-website
- **Live Site**: https://dollarfence.com
- **Backup Date**: $(date)
- **Netlify Project ID**: 9c350974-125d-4848-8e58-991245a61636

## Scripts Included

The backup includes several utility scripts:
- `optimize_images.sh` - Image optimization
- `update_fence_titles.sh` - Bulk title updates
- `update_footer.sh` - Footer updates
- `fix_fontawesome.sh` - Font Awesome fixes

## Support

This backup contains everything needed to recreate the Dollar Fence website. All external dependencies have been downloaded and included to ensure the site works offline and without external CDN dependencies.

For questions about the original website, contact Dollar Fence at (888) 964-7778.

