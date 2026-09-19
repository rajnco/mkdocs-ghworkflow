(function () {
  const storageKey = 'newtons_law_page_hits';

  function getPageKey() {
    const path = window.location.pathname || '/';
    return path.replace(/\/+$/, '') || '/';
  }

  function getHits() {
    try {
      const raw = localStorage.getItem(storageKey);
      return raw ? JSON.parse(raw) : {};
    } catch (error) {
      return {};
    }
  }

  function setHits(hits) {
    try {
      localStorage.setItem(storageKey, JSON.stringify(hits));
    } catch (error) {
      // Ignore storage issues gracefully.
    }
  }

  function updateStats() {
    const page = getPageKey();
    const hits = getHits();
    hits[page] = (Number(hits[page]) || 0) + 1;
    setHits(hits);

    const statsNode = document.getElementById('page-stats');
    if (statsNode) {
      const total = Object.values(hits).reduce((sum, value) => sum + Number(value || 0), 0);
      statsNode.textContent = 'Page hit count: ' + hits[page] + ' | Total visits: ' + total;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateStats);
  } else {
    updateStats();
  }
})();
