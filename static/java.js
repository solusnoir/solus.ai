document.addEventListener("DOMContentLoaded", () => {
  const mainTitle = document.querySelector("#main-title");
  const navTitle = document.querySelector(".nav-title");
  const header = document.querySelector(".header");

  window.addEventListener("scroll", () => {
    const scrollY = window.scrollY;

    // Scale and fade title as you scroll
    const scale = Math.max(1 - scrollY / 500, 0.5);
    mainTitle.style.transform = `scale(${scale})`;
    mainTitle.style.opacity = Math.max(1 - scrollY / 200, 0);

    // Fade in the nav title
    navTitle.style.opacity = Math.min(scrollY / 200, 1);

    // Shrink header after scrolling
    if (scrollY > 200) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  });
});

window.addEventListener("DOMContentLoaded", () => {
  window.history.scrollRestoration = "manual"; // Disable browser scroll preservation
  window.scrollTo(0, 0); // Ensure page loads at the top
});
