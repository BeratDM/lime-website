// Sidebar small screen close button
document.addEventListener("DOMContentLoaded", function () {
  var closeButton = document.querySelector(".btn-close");
  closeButton.addEventListener("click", function () {
    var sidebar = document.getElementById("sidebar-nav");
    var bsOffcanvas = bootstrap.Offcanvas.getInstance(sidebar);
    if (bsOffcanvas) {
      bsOffcanvas.hide();
    }
  });
});

// Sidebar acting lowkey weird fix (scrolls back up after close, adds delay, closes upon section selection)

document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar-nav");
  const navLinks = sidebar.querySelectorAll(".nav-link");

  function handleNavLinkClick(event) {
    event.preventDefault();

    const targetId = this.getAttribute("href").substring(1);
    const targetElement = document.getElementById(targetId);

    if (targetElement) {
      let bsOffcanvas = bootstrap.Offcanvas.getInstance(sidebar);

      const afterOffcanvasHidden = () => {
        targetElement.scrollIntoView({ behavior: "smooth" });
        sidebar.removeEventListener(
          "hidden.bs.offcanvas",
          afterOffcanvasHidden
        ); // Important: Remove the listener
      };

      if (bsOffcanvas && bsOffcanvas._isShown) {
        // Check if offcanvas is shown
        sidebar.addEventListener("hidden.bs.offcanvas", afterOffcanvasHidden);
        bsOffcanvas.hide();
      } else {
        targetElement.scrollIntoView({ behavior: "smooth" }); // For non-offcanvas or already hidden
      }
    }
  }

  // Attach event listeners ONCE, but use a function to handle clicks
  navLinks.forEach((link) => {
    link.addEventListener("click", handleNavLinkClick);
  });

  // Intersection Observer (Active States) - Keep this code as it was
  // ... (Your Intersection Observer code here) ...

  // Mutation Observer to handle dynamic changes in the DOM
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (
        mutation.type === "attributes" &&
        mutation.attributeName === "class" &&
        mutation.target === sidebar
      ) {
        // Check if the sidebar's class changed (e.g., from offcanvas to regular)
        // Re-attach event listeners to .nav-link elements
        navLinks.forEach((link) => {
          link.removeEventListener("click", handleNavLinkClick); // Remove old listener
          link.addEventListener("click", handleNavLinkClick); // Add new listener
        });
      }
    });
  });

  observer.observe(sidebar, { attributes: true });
});
document.addEventListener("DOMContentLoaded", function () {
  var sections = document.querySelectorAll("main section");
  var navLinks = document.querySelectorAll("#sidebar-nav .nav-link");

  // Detect parent-child relationships dynamically
  let sectionHierarchy = {};
  sections.forEach((section) => {
    let id = section.getAttribute("id");
    let parentId = id.includes("-") ? id.split("-")[0] : null; // Extract parent part
    if (parentId && document.getElementById(parentId)) {
      sectionHierarchy[id] = parentId; // Map child to parent
    }
  });

  let observer = new IntersectionObserver(
    (entries) => {
      let activeSections = new Set();

      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          let sectionId = entry.target.getAttribute("id");
          activeSections.add(sectionId);

          // If a child section is active, mark its parent as well
          if (sectionHierarchy[sectionId]) {
            activeSections.add(sectionHierarchy[sectionId]);
          }
        }
      });

      // Update sidebar links
      navLinks.forEach((link) => {
        let linkHref = link.getAttribute("href").substring(1); // Remove #
        if (activeSections.has(linkHref)) {
          link.classList.add("active");
        } else {
          link.classList.remove("active");
        }
      });
    },
    { rootMargin: "-10% 0px -90% 0px", threshold: 0 }
  );

  sections.forEach((section) => observer.observe(section));
});
