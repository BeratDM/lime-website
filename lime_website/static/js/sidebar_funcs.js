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

// Sidebar active section logic
document.addEventListener("DOMContentLoaded", function () {
  const sections = document.querySelectorAll("main section");
  const navLinks = document.querySelectorAll("#sidebar-nav .nav-link");

  // Track parent-child relationships
  let sectionHierarchy = {};
  sections.forEach((section) => {
    let id = section.id;
    let parentId = id.includes("-") ? id.split("-")[0] : null;
    if (parentId && document.getElementById(parentId)) {
      sectionHierarchy[id] = parentId;
    }
  });

  let activeParents = new Set();
  let observer = new IntersectionObserver(
    (entries) => {
      let activeSections = new Set();

      entries.forEach((entry) => {
        let sectionId = entry.target.id;
        if (entry.isIntersecting) {
          activeSections.add(sectionId);
          if (sectionHierarchy[sectionId])
            activeParents.add(sectionHierarchy[sectionId]);
        } else if (!sectionHierarchy[sectionId]) {
          activeParents.delete(sectionId); // Remove parent only when it leaves
        }
      });

      // Merge parents & active sections
      activeSections = new Set([...activeSections, ...activeParents]);

      // Update sidebar links
      navLinks.forEach((link) => {
        let linkHref = link.getAttribute("href").substring(1);
        link.classList.toggle("active", activeSections.has(linkHref));
      });
    },
    { rootMargin: "-10% 0px -90% 0px", threshold: 0 }
  );

  sections.forEach((section) => observer.observe(section));
});

// Makes the sidebar stick to top - MIGHT NOT NEED IT AFTER USING "sticky-mb-top" from bootstrap
// document.addEventListener("DOMContentLoaded", function () {
//   const sidebar = document.getElementById("sidebar-nav");

//   function adjustSidebarPosition() {
//     const contentTop = document.getElementById("main-content").offsetTop;
//     const scrollTop = window.scrollY;

//     if (scrollTop > contentTop) {
//       sidebar.style.top = "0px"; // Stick to top when scrolling
//     } else {
//       sidebar.style.top = `${contentTop - scrollTop}px`;
//     }
//   }

//   window.addEventListener("scroll", adjustSidebarPosition);
//   adjustSidebarPosition(); // Page load
// });
