
   // Navbar Toggle
   function toggleMenu() {
    document.getElementById('navLinks').classList.toggle('active');
}
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
    }
  });
}, { threshold: 0.2 });

document.querySelectorAll(".animate").forEach(card => {
  observer.observe(card);
});

