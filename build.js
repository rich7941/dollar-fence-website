#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { minify } = require('terser');
const CleanCSS = require('clean-css');

// Configuration
const config = {
  jsFiles: [
    'assets/js/lazy-loading.js',
    'assets/js/main.js',
    'assets/js/responsive-images.js'
  ],
  cssFiles: [
    'assets/css/styles.css',
    'assets/css/location-page-fix.css'
  ]
};

// Minify JavaScript files
async function minifyJS() {
  console.log('🔧 Minifying JavaScript files...');
  
  for (const file of config.jsFiles) {
    if (!fs.existsSync(file)) {
      console.log(`⚠️  File not found: ${file}`);
      continue;
    }
    
    try {
      const code = fs.readFileSync(file, 'utf8');
      const result = await minify(code, {
        compress: {
          drop_console: false, // Keep console logs for debugging
          drop_debugger: true,
          pure_funcs: ['console.log'] // Remove console.log in production
        },
        mangle: true,
        format: {
          comments: false
        }
      });
      
      if (result.error) {
        console.error(`❌ Error minifying ${file}:`, result.error);
        continue;
      }
      
      const minFile = file.replace('.js', '.min.js');
      fs.writeFileSync(minFile, result.code);
      
      const originalSize = fs.statSync(file).size;
      const minifiedSize = fs.statSync(minFile).size;
      const savings = ((originalSize - minifiedSize) / originalSize * 100).toFixed(1);
      
      console.log(`✅ ${file} → ${minFile} (${originalSize}B → ${minifiedSize}B, ${savings}% smaller)`);
    } catch (error) {
      console.error(`❌ Error processing ${file}:`, error.message);
    }
  }
}

// Minify CSS files
function minifyCSS() {
  console.log('🎨 Minifying CSS files...');
  
  const cleanCSS = new CleanCSS({
    level: 2, // Advanced optimizations
    returnPromise: false
  });
  
  for (const file of config.cssFiles) {
    if (!fs.existsSync(file)) {
      console.log(`⚠️  File not found: ${file}`);
      continue;
    }
    
    try {
      const css = fs.readFileSync(file, 'utf8');
      const result = cleanCSS.minify(css);
      
      if (result.errors.length > 0) {
        console.error(`❌ Error minifying ${file}:`, result.errors);
        continue;
      }
      
      const minFile = file.replace('.css', '.min.css');
      fs.writeFileSync(minFile, result.styles);
      
      const originalSize = fs.statSync(file).size;
      const minifiedSize = fs.statSync(minFile).size;
      const savings = ((originalSize - minifiedSize) / originalSize * 100).toFixed(1);
      
      console.log(`✅ ${file} → ${minFile} (${originalSize}B → ${minifiedSize}B, ${savings}% smaller)`);
    } catch (error) {
      console.error(`❌ Error processing ${file}:`, error.message);
    }
  }
}

// Main build function
async function build() {
  console.log('🚀 Starting build process...\n');
  
  await minifyJS();
  console.log('');
  minifyCSS();
  
  console.log('\n✨ Build complete!');
  console.log('\n📊 Performance Impact:');
  console.log('- Reduced file sizes improve page load times');
  console.log('- Smaller files reduce bandwidth usage');
  console.log('- Better compression ratios for gzip/brotli');
  console.log('- Improved Core Web Vitals scores');
}

// Run the build
if (require.main === module) {
  build().catch(console.error);
}

module.exports = { build, minifyJS, minifyCSS };

