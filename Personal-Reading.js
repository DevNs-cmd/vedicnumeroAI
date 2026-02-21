
   // Navbar Toggle
   function toggleMenu() {
    document.getElementById('navLinks').classList.toggle('active');
}


// Animate on Scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
      }
    });
  }, {
    threshold: 0.3
  });

  document.querySelectorAll(".animate-on-scroll").forEach(el => {
    observer.observe(el);
  });




  