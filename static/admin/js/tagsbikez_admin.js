/* ============================================================
   TagsBikez admin fixes (loads on every admin page)

   1. Tab fallback  - if Bootstrap's tab JS fails to initialise
      for any reason, clicking a tab (SEO, Content Paragraphs,
      etc.) still switches panes via this manual handler.
   2. Bottom save bar - clones the Save buttons below the form
      so they are always reachable without hunting for the
      right-hand actions column.
   ============================================================ */

(function () {
    'use strict';

    function ready(fn) {
        if (document.readyState !== 'loading') { fn(); }
        else { document.addEventListener('DOMContentLoaded', fn); }
    }

    /* ---------- 1. Manual tab switching fallback ---------- */
    function initTabFallback() {
        var tabBar = document.getElementById('jazzy-tabs');
        if (!tabBar) { return; }

        var links = tabBar.querySelectorAll('a.nav-link');

        links.forEach(function (link) {
            link.addEventListener('click', function (e) {
                // Always prevent the default anchor jump.
                e.preventDefault();

                var targetId = (link.getAttribute('href') || '').replace('#', '');
                if (!targetId) { return; }
                var targetPane = document.getElementById(targetId);
                if (!targetPane) { return; }

                // Deactivate every tab + pane.
                links.forEach(function (l) {
                    l.classList.remove('active');
                    l.setAttribute('aria-selected', 'false');
                });
                var panes = targetPane.parentElement.querySelectorAll('.tab-pane');
                panes.forEach(function (p) {
                    p.classList.remove('active', 'show');
                });

                // Activate the clicked one.
                link.classList.add('active');
                link.setAttribute('aria-selected', 'true');
                targetPane.classList.add('active', 'show');

                // Keep the hash so a reload restores the tab.
                if (history.replaceState) {
                    history.replaceState(null, null, '#' + targetId);
                }

                // Let widgets (selects, inlines) recalc sizes.
                window.dispatchEvent(new Event('resize'));
            });
        });

        // Restore tab from URL hash on load.
        var hash = window.location.hash;
        if (hash) {
            var restore = tabBar.querySelector('a[href="' + hash + '"]');
            if (restore) { restore.click(); }
        }
    }

    /* ---------- 2. Bottom save bar ---------- */
    function initBottomSaveBar() {
        var actions = document.getElementById('jazzy-actions');
        var form = actions ? actions.closest('form') : null;
        if (!actions || !form) { return; }

        // Don't add twice.
        if (form.querySelector('.tagsbikez-bottom-save')) { return; }

        var bar = document.createElement('div');
        bar.className = 'tagsbikez-bottom-save';

        var buttons = actions.querySelectorAll(
            'input[type="submit"], button[type="submit"]'
        );
        if (!buttons.length) { return; }

        buttons.forEach(function (btn) {
            var clone = btn.cloneNode(true);
            clone.classList.remove('btn-sm');
            bar.appendChild(clone);
        });

        // Place the bar at the very end of the form (below inlines).
        form.appendChild(bar);
    }

    ready(function () {
        initTabFallback();
        initBottomSaveBar();
    });
})();
