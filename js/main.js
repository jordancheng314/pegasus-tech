(() => {
  const dropdown = document.querySelector(".nav-dropdown");
  const trigger = document.querySelector(".nav-trigger");

  if (dropdown && trigger) {
    const closeMenu = () => {
      dropdown.classList.remove("is-open");
      trigger.setAttribute("aria-expanded", "false");
    };

    trigger.addEventListener("click", (event) => {
      event.stopPropagation();
      const open = dropdown.classList.toggle("is-open");
      trigger.setAttribute("aria-expanded", String(open));
    });

    document.addEventListener("click", (event) => {
      if (!dropdown.contains(event.target)) closeMenu();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });
  }

  const lightbox = document.querySelector("[data-lightbox]");
  const lightboxImg = document.querySelector("[data-lightbox-img]");
  const lightboxClose = document.querySelector("[data-lightbox-close]");
  const galleryItems = document.querySelectorAll("[data-lightbox-gallery] .gallery-item");

  const closeLightbox = () => {
    if (!lightbox) return;
    lightbox.hidden = true;
    if (lightboxImg) lightboxImg.src = "";
  };

  galleryItems.forEach((item) => {
    item.addEventListener("click", () => {
      if (!lightbox || !lightboxImg) return;
      lightboxImg.src = item.dataset.full || item.querySelector("img")?.src || "";
      lightboxImg.alt = item.querySelector("img")?.alt || "";
      lightbox.hidden = false;
    });
  });

  lightboxClose?.addEventListener("click", closeLightbox);
  lightbox?.addEventListener("click", (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeLightbox();
  });

  const carousel = document.querySelector("[data-carousel]");
  if (!carousel) return;

  const slides = Array.from(carousel.querySelectorAll("[data-slide]"));
  const dotsWrap = carousel.querySelector("[data-dots]");
  const prevBtn = carousel.querySelector("[data-prev]");
  const nextBtn = carousel.querySelector("[data-next]");
  const progressBar = carousel.querySelector(".carousel-progress");

  if (!slides.length) return;

  let index = 0;
  let timer = null;
  const INTERVAL = 6000;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const renderDots = () => {
    if (!dotsWrap) return;
    dotsWrap.innerHTML = "";
    slides.forEach((_, i) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.setAttribute("aria-label", `前往第 ${i + 1} 張`);
      if (i === index) btn.classList.add("is-active");
      btn.addEventListener("click", () => goTo(i));
      dotsWrap.appendChild(btn);
    });
  };

  const restartProgress = () => {
    if (!progressBar || reduceMotion) return;
    progressBar.classList.remove("is-running");
    void progressBar.offsetWidth;
    progressBar.classList.add("is-running");
  };

  const goTo = (nextIndex) => {
    slides[index].classList.remove("is-active");
    index = (nextIndex + slides.length) % slides.length;
    slides[index].classList.add("is-active");
    renderDots();
    restartProgress();
    restartTimer();
  };

  const restartTimer = () => {
    if (reduceMotion) return;
    clearInterval(timer);
    timer = setInterval(() => goTo(index + 1), INTERVAL);
  };

  prevBtn?.addEventListener("click", () => goTo(index - 1));
  nextBtn?.addEventListener("click", () => goTo(index + 1));

  carousel.addEventListener("mouseenter", () => clearInterval(timer));
  carousel.addEventListener("mouseleave", restartTimer);

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) clearInterval(timer);
    else restartTimer();
  });

  renderDots();
  restartProgress();
  restartTimer();
})();
