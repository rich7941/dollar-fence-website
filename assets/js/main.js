// Main JavaScript file for the fence company website
document.addEventListener('DOMContentLoaded', function() {
  // Mobile navigation toggle - now using the existing button in the HTML
  const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
  const nav = document.querySelector('.main-nav');
  
  // Initially hide the nav on mobile - ensure this happens immediately
  function setInitialMenuState() {
    if (window.innerWidth < 768) {
      nav.classList.add('mobile-hidden');
    } else {
      nav.classList.remove('mobile-hidden');
    }
  }
  
  // Set initial state on page load
  setInitialMenuState();
  
  // Toggle menu visibility when button is clicked
  if (mobileNavToggle) {
    mobileNavToggle.addEventListener('click', function() {
      nav.classList.toggle('mobile-hidden');
      mobileNavToggle.classList.toggle('active');
    });
  }
  
  // Handle window resize
  window.addEventListener('resize', function() {
    if (window.innerWidth < 768) {
      if (!mobileNavToggle.classList.contains('active')) {
        nav.classList.add('mobile-hidden');
      }
    } else {
      nav.classList.remove('mobile-hidden');
      mobileNavToggle.classList.remove('active');
    }
  });
  
  // Form validation
  const contactForm = document.querySelector('.contact-form form');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      // Basic validation
      let valid = true;
      const requiredFields = contactForm.querySelectorAll('[required]');
      
      requiredFields.forEach(field => {
        if (!field.value.trim()) {
          valid = false;
          field.classList.add('error');
        } else {
          field.classList.remove('error');
        }
      });
      
      // Email validation
      const emailField = contactForm.querySelector('input[type="email"]');
      if (emailField && emailField.value) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailField.value)) {
          valid = false;
          emailField.classList.add('error');
        }
      }
      
      if (!valid) {
        e.preventDefault(); // Only prevent submission if validation fails
      }
      // If valid, allow the form to submit naturally to Netlify
    });
  }
  
  // Lazy load images
  if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });
    
    lazyImages.forEach(img => {
      imageObserver.observe(img);
    });
  }
  
  // Add schema markup dynamically if needed
  function addSchemaMarkup(locationData) {
    if (!locationData) return;
    
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    
    const schema = {
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "Dollar Fence - " + locationData.city,
      "image": locationData.image || "https://dollarfence.com/assets/images/logo.jpg",
      "telephone": locationData.phone || "(888) 964-7778",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": locationData.street || "123 Main St",
        "addressLocality": locationData.city || "Austin",
        "addressRegion": locationData.state || "TX",
        "postalCode": locationData.zip || "78701",
        "addressCountry": "US"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": locationData.lat || "30.2672",
        "longitude": locationData.lng || "-97.7431"
      },
      "url": locationData.url || "https://dollarfence.com",
      "priceRange": "$$$"
    };
    
    script.textContent = JSON.stringify(schema);
    document.head.appendChild(script);
  }
  
  // Example usage for location pages
  const locationPage = document.querySelector('.location-page');
  if (locationPage) {
    const locationId = locationPage.dataset.locationId;
    // In a real implementation, this would fetch location data from a data file
    // For now, we'll just use placeholder data for Austin
    if (locationId === 'austin') {
      addSchemaMarkup({
        city: 'Austin',
        state: 'TX',
        zip: '78701',
        lat: '30.2672',
        lng: '-97.7431'
      });
    }
  }
});
