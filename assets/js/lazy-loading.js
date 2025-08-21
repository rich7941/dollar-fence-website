// Minimal lazy loading - zero blocking
(function() {
  'use strict';
  
  if (!('IntersectionObserver' in window)) return;
  
  function initLazy() {
    // Hero sections
    const heroes = document.querySelectorAll('.hero[data-src]');
    if (heroes.length > 0) {
      const heroObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            const hero = entry.target;
            const src = hero.getAttribute('data-src');
            if (src) {
              hero.style.backgroundImage = 'linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url(\'' + src + '\')';
              hero.removeAttribute('data-src');
              heroObserver.unobserve(hero);
            }
          }
        });
      }, { rootMargin: '50px', threshold: 0.01 });
      
      heroes.forEach(function(hero) {
        heroObserver.observe(hero);
      });
    }
    
    // Regular images
    const imgs = document.querySelectorAll('img[data-src]');
    if (imgs.length > 0) {
      const imgObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            const img = entry.target;
            const src = img.getAttribute('data-src');
            if (src) {
              img.src = src;
              img.removeAttribute('data-src');
              img.classList.remove('lazy');
              imgObserver.unobserve(img);
            }
          }
        });
      }, { rootMargin: '50px', threshold: 0.01 });
      
      imgs.forEach(function(img) {
        imgObserver.observe(img);
      });
    }
  }
  
  // Maximum deferral
  if ('requestIdleCallback' in window) {
    requestIdleCallback(initLazy, { timeout: 15000 });
  } else {
    setTimeout(initLazy, 2000);
  }
})();

