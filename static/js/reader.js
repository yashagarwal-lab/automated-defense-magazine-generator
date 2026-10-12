// Interactive Military Defense Magazine Flipbook Logic
document.addEventListener("DOMContentLoaded", () => {
  const pages = Array.from(document.querySelectorAll(".reader-page-card"));
  const totalPages = pages.length;
  let currentPage = 1;
  let isSpreadView = true;

  const currPageEl = document.getElementById("curr-page");
  const btnPrev = document.getElementById("btn-prev");
  const btnNext = document.getElementById("btn-next");
  const btnSpread = document.getElementById("btn-spread");
  const btnToc = document.getElementById("btn-toc");
  const btnCloseToc = document.getElementById("btn-close-toc");
  const tocDrawer = document.getElementById("toc-drawer");
  const btnFullscreen = document.getElementById("btn-fullscreen");

  function updateView() {
    pages.forEach(p => p.classList.remove("active"));

    if (isSpreadView) {
      if (currentPage === 1 || currentPage === totalPages) {
        const target = document.getElementById("card-" + currentPage);
        if (target) target.classList.add("active");
      } else {
        const leftNum = (currentPage % 2 === 0) ? currentPage : currentPage - 1;
        const rightNum = leftNum + 1;
        const leftPage = document.getElementById("card-" + leftNum);
        const rightPage = document.getElementById("card-" + rightNum);
        if (leftPage) leftPage.classList.add("active");
        if (rightPage) rightPage.classList.add("active");
      }
    } else {
      const target = document.getElementById("card-" + currentPage);
      if (target) target.classList.add("active");
    }

    if (currPageEl) currPageEl.textContent = currentPage;
    if (btnPrev) btnPrev.disabled = (currentPage <= 1);
    if (btnNext) btnNext.disabled = (currentPage >= totalPages);
  }

  function goToPage(n) {
    if (n < 1) n = 1;
    if (n > totalPages) n = totalPages;
    currentPage = n;
    updateView();
  }

  function nextPage() {
    if (isSpreadView && currentPage > 1 && currentPage < totalPages - 1) {
      goToPage(currentPage + 2);
    } else {
      goToPage(currentPage + 1);
    }
  }

  function prevPage() {
    if (isSpreadView && currentPage > 2) {
      goToPage(currentPage - 2);
    } else {
      goToPage(currentPage - 1);
    }
  }

  if (btnPrev) btnPrev.addEventListener("click", prevPage);
  if (btnNext) btnNext.addEventListener("click", nextPage);

  if (btnSpread) {
    btnSpread.addEventListener("click", () => {
      isSpreadView = !isSpreadView;
      btnSpread.classList.toggle("active", isSpreadView);
      updateView();
    });
  }

  if (btnToc && tocDrawer) {
    btnToc.addEventListener("click", () => tocDrawer.classList.toggle("open"));
  }
  if (btnCloseToc && tocDrawer) {
    btnCloseToc.addEventListener("click", () => tocDrawer.classList.remove("open"));
  }

  document.querySelectorAll(".toc-nav-item").forEach(item => {
    item.addEventListener("click", () => {
      const target = parseInt(item.getAttribute("data-target-page"), 10);
      if (!isNaN(target)) {
        goToPage(target);
        if (tocDrawer) tocDrawer.classList.remove("open");
      }
    });
  });

  if (btnFullscreen) {
    btnFullscreen.addEventListener("click", () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    });
  }

  window.addEventListener("keydown", e => {
    if (e.key === "ArrowRight" || e.key === "PageDown") {
      nextPage();
    } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
      prevPage();
    } else if (e.key === "Home") {
      goToPage(1);
    } else if (e.key === "End") {
      goToPage(totalPages);
    } else if (e.key === "Escape") {
      if (tocDrawer) tocDrawer.classList.remove("open");
    }
  });

  updateView();
});
