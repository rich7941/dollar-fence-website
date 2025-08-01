// Universal mobile navigation JavaScript - works with all pages
(function() {
  'use strict';
  
  // Critical mobile navigation - immediate execution
  function initCritical() {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const nav = document.querySelector('.main-nav');
    
    if (mobileNavToggle && nav) {
      mobileNavToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        
        // Simplified logic: always use mobile-hidden for consistency
        if (this.classList.contains('active')) {
          // Opening menu: remove mobile-hidden
          nav.classList.remove('mobile-hidden');
        } else {
          // Closing menu: add mobile-hidden
          nav.classList.add('mobile-hidden');
        }
      });
    }
  }
  
  // Chunk 1: Basic navigation (immediate)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCritical);
  } else {
    initCritical();
  }
  
  // Chunk 2: Resize handlers (deferred)
  function chunk2() {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const nav = document.querySelector('.main-nav');
    
    if (nav && mobileNavToggle) {
      window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
          // Desktop: ensure menu is visible and reset mobile classes
          nav.classList.remove('mobile-hidden', 'mobile-show');
          mobileNavToggle.classList.remove('active');
        }
      });
    }
  }
  
  // Chunk 3: Form validation (deferred)
  function chunk3() {
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
      contactForm.addEventListener('submit', function(e) {
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
        
        const emailField = contactForm.querySelector('input[type="email"]');
        if (emailField && emailField.value) {
          const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailPattern.test(emailField.value)) {
            valid = false;
            emailField.classList.add('error');
          }
        }
        
        if (!valid) {
          e.preventDefault();
        }
      });
    }
  }
  
  // Chunk 4: Lazy loading (deferred)
  function chunk4() {
    if ('IntersectionObserver' in window) {
      const lazyImages = document.querySelectorAll('img[data-src]');
      
      if (lazyImages.length > 0) {
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
    }
  }
  
  // Schedule chunks with maximum deferral to avoid main-thread blocking
  if (typeof requestIdleCallback !== 'undefined') {
    requestIdleCallback(chunk2, { timeout: 5000 });
    requestIdleCallback(chunk3, { timeout: 8000 });
    requestIdleCallback(chunk4, { timeout: 10000 });
  } else {
    // Fallback with aggressive timeouts
    setTimeout(chunk2, 200);
    setTimeout(chunk3, 500);
    setTimeout(chunk4, 1000);
  }
})();
// Cache bust Tue Jul 29 15:53:45 UTC 2025

