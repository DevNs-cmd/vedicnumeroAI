gsap.registerPlugin(ScrollTrigger);

gsap.from(".num-feature-card", {
  scrollTrigger: {
    trigger: ".num-features-section",
    start: "top 75%",
  },
  opacity: 0,
  y: 40,
  duration: 0.9,
  stagger: 0.15,
  ease: "power3.out",
});


gsap.registerPlugin(ScrollTrigger);

gsap.from(".hiw-step-card", {
  scrollTrigger: {
    trigger: ".hiw-section",
    start: "top 70%",
  },
  opacity: 0,
  y: 50,
  duration: 0.9,
  stagger: 0.2,
  ease: "power3.out",
});
