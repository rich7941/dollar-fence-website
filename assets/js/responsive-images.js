// Minimal responsive images - zero blocking
(function() {
  'use strict';
  
  function initResponsive() {
    // Only handle critical responsive behavior
    const imgs = document.querySelectorAll('img[data-mobile], img[data-desktop]');
    if (imgs.length === 0) return;
    
    function updateImages() {
      const isMobile = window.innerWidth < 768;
      imgs.forEach(function(img) {
        const mobileSrc = img.getAttribute('data-mobile');
        const desktopSrc = img.getAttribute('data-desktop');
        
        if (isMobile && mobileSrc) {
          img.src = mobileSrc;
        } else if (!isMobile && desktopSrc) {
          img.src = desktopSrc;
        }
      });
    }
    
    updateImages();
    
    // Throttled resize handler
    let resizeTimer;
    window.addEventListener('resize', function() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(updateImages, 250);
    });
  }
  
  // Maximum deferral
  if ('requestIdleCallback' in window) {
    requestIdleCallback(initResponsive, { timeout: 20000 });
  } else {
    setTimeout(initResponsive, 3000);
  }
})();

