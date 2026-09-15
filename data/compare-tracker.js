/* VIVIAN — Compare Tool Tracker
 * Loaded by all 8 product pages. Adds "Add to Compare" button next to h1.product-title
 * and a floating bubble (bottom-right) showing selected count.
 * Selected products are stored in sessionStorage as {a: <id>, b: <id>}.
 * compare.html reads this on load.
 */
(function () {
  'use strict';

  const STORE_KEY = 'vivian-compare-selection';

  // ----- Identify current product from URL -----
  const path = location.pathname;
  const m = path.match(/product-(bl\d+-\d+)\.html/);
  if (!m) return;
  const productId = m[1];

  // ----- Inject CSS once -----
  if (!document.getElementById('compare-tracker-css')) {
    const style = document.createElement('style');
    style.id = 'compare-tracker-css';
    style.textContent = `
      .compare-add-btn {
        display: inline-flex; align-items: center; gap: 6px;
        margin: 8px 0 4px;
        padding: 9px 16px;
        background: #fff;
        border: 1.5px solid #0F6E56;
        color: #0F6E56;
        border-radius: 6px;
        font-size: 0.88rem;
        font-weight: 600;
        font-family: inherit;
        cursor: pointer;
        transition: background .15s, color .15s;
        vertical-align: middle;
      }
      .compare-add-btn:hover {
        background: #0F6E56;
        color: #fff;
      }
      .compare-add-btn.selected {
        background: #0F6E56;
        color: #fff;
      }
      .compare-add-btn .compare-icon {
        font-size: 1rem;
      }

      .compare-bubble {
        position: fixed;
        right: 24px;
        bottom: 24px;
        z-index: 99;
        background: #fff;
        border: 1.5px solid #0F6E56;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 8px 24px rgba(15, 110, 86, 0.18);
        min-width: 220px;
        max-width: 320px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif;
        font-size: 0.9rem;
        color: #1A1A1A;
        animation: compare-bubble-in .25s ease-out;
      }
      @keyframes compare-bubble-in {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }
      .compare-bubble-header {
        display: flex; align-items: center; gap: 8px;
        margin-bottom: 8px;
        font-weight: 700;
      }
      .compare-bubble-header .count {
        background: #0F6E56;
        color: #fff;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.78rem;
      }
      .compare-bubble-ids {
        font-size: 0.8rem;
        color: #5C5C5C;
        margin-bottom: 10px;
        line-height: 1.4;
      }
      .compare-bubble-ids .pill {
        display: inline-block;
        background: #E8F0EC;
        color: #0F6E56;
        padding: 2px 8px;
        border-radius: 10px;
        font-weight: 600;
        margin-right: 4px;
        font-size: 0.75rem;
      }
      .compare-bubble-actions {
        display: flex; gap: 8px; align-items: center;
      }
      .compare-bubble-actions a {
        flex: 1;
        text-align: center;
        background: #0F6E56;
        color: #fff;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem;
        text-decoration: none;
      }
      .compare-bubble-actions a:hover {
        background: #094739;
        color: #fff;
        text-decoration: none;
      }
      .compare-bubble-actions button {
        background: transparent;
        border: 1px solid #E5E0D5;
        color: #5C5C5C;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        cursor: pointer;
        font-family: inherit;
      }
      .compare-bubble-actions button:hover {
        border-color: #EF9F27;
        color: #EF9F27;
      }
      @media (max-width: 480px) {
        .compare-bubble {
          right: 12px; left: 12px; bottom: 12px;
          max-width: none;
        }
        .compare-add-btn { font-size: 0.82rem; padding: 8px 12px; }
      }
    `;
    document.head.appendChild(style);
  }

  // ----- Helpers -----
  function readSelection() {
    try {
      const raw = sessionStorage.getItem(STORE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) { return {}; }
  }
  function writeSelection(s) {
    try { sessionStorage.setItem(STORE_KEY, JSON.stringify(s)); } catch (e) {}
  }
  function getIds() {
    const s = readSelection();
    return [s.a, s.b].filter(Boolean);
  }

  // ----- Insert button next to h1.product-title -----
  const h1 = document.querySelector('h1.product-title');
  if (h1) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'compare-add-btn';
    btn.className = 'compare-add-btn';
    btn.setAttribute('aria-label', 'Add this model to comparison');
    btn.innerHTML = '<span class="compare-icon">⚖</span> <span class="compare-add-btn-label">Add to Compare</span>';
    btn.addEventListener('click', toggle);
    h1.insertAdjacentElement('afterend', btn);
  }

  // ----- Floating bubble -----
  const bubble = document.createElement('div');
  bubble.id = 'compare-bubble';
  bubble.className = 'compare-bubble';
  bubble.style.display = 'none';
  bubble.innerHTML = `
    <div class="compare-bubble-header">
      <span class="count">0/2</span>
      <span>Compare list</span>
    </div>
    <div class="compare-bubble-ids"></div>
    <div class="compare-bubble-actions">
      <a href="compare.html">Compare now →</a>
      <button type="button" class="compare-bubble-clear">Clear</button>
    </div>
  `;
  document.body.appendChild(bubble);
  bubble.querySelector('.compare-bubble-clear').addEventListener('click', clearAll);

  // ----- Toggle add/remove -----
  function toggle() {
    const sel = readSelection();
    const ids = getIds();
    if (ids.includes(productId)) {
      if (sel.a === productId) sel.a = null;
      else if (sel.b === productId) sel.b = null;
      writeSelection(sel);
    } else {
      if (!sel.a) sel.a = productId;
      else if (!sel.b) sel.b = productId;
      else {
        // Already 2 selected, prompt to clear
        if (window.confirm('You already picked 2 models. Clear the list first?')) {
          writeSelection({ a: productId });
        }
        refresh();
        return;
      }
      writeSelection(sel);
    }
    refresh();
  }

  function clearAll() {
    writeSelection({});
    refresh();
  }

  // ----- Render -----
  function refresh() {
    const sel = readSelection();
    const ids = getIds();
    const btn = document.getElementById('compare-add-btn');
    if (btn) {
      const labelEl = btn.querySelector('.compare-add-btn-label');
        if (ids.includes(productId)) {
          btn.classList.add('selected');
          labelEl.textContent = 'Added ✓';
        } else {
          btn.classList.remove('selected');
          labelEl.textContent = 'Add to Compare';
        }
    }

    if (ids.length === 0) {
      bubble.style.display = 'none';
      return;
    }
    bubble.style.display = '';
    bubble.querySelector('.count').textContent = ids.length + '/2';

    const idsEl = bubble.querySelector('.compare-bubble-ids');
    idsEl.innerHTML = ids.map(id => '<span class="pill">' + id.toUpperCase() + '</span>').join('');

    const link = bubble.querySelector('.compare-bubble-actions a');
    if (ids.length === 2) {
      link.href = 'compare.html?a=' + sel.a + '&b=' + sel.b;
      link.textContent = 'Compare now →';
    } else {
      link.href = 'compare.html';
      link.textContent = 'Pick 2nd model →';
    }
  }

  refresh();
})();