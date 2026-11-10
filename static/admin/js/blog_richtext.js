/* ============================================================
   TagsBikez - Blog paragraph rich-text editor
   static/admin/js/blog_richtext.js

   Upgrades every <textarea class="tb-richtext"> (the "Text" field
   in Blog Posts -> Content Paragraphs) into a small editor with:

     Bold, Italic, Underline, Strike, Heading 2/3, Normal text,
     Bullet list, Numbered list, Quote, Hyperlink (add / edit),
     Remove link, Clear formatting, Undo / Redo and a
     "</> HTML" button to see / type the raw HTML tags.

   The textarea stays the real form field - it always holds the
   HTML, so Django saves it exactly like before. The server
   sanitises it again (apps/blog/html_sanitizer.py).

   No external libraries. Works with rows added by
   "Add another Paragraph".
   ============================================================ */

(function () {
    'use strict';

    /* ---------- allowed HTML (keep in sync with html_sanitizer.py) ---------- */
    var ALLOWED = {
        A: ['href', 'target', 'title'],
        B: [], STRONG: [], I: [], EM: [], U: [], S: [],
        P: [], BR: [], UL: [], OL: [], LI: [],
        H2: [], H3: [], H4: [], BLOCKQUOTE: []
    };
    var DROP_WITH_CONTENT = ['SCRIPT', 'STYLE', 'IFRAME', 'OBJECT', 'EMBED', 'NOSCRIPT', 'TEMPLATE', 'META', 'LINK', 'TITLE'];
    var RENAME = { DIV: 'P', STRIKE: 'S', DEL: 'S' };

    function ready(fn) {
        if (document.readyState !== 'loading') { fn(); }
        else { document.addEventListener('DOMContentLoaded', fn); }
    }

    function normaliseUrl(url) {
        url = (url || '').trim();
        if (!url) { return ''; }
        if (/^(https?:\/\/|mailto:|tel:|\/|#|\?)/i.test(url)) { return url; }
        if (/^[a-z][a-z0-9+.-]*:/i.test(url)) { return ''; }   // javascript:, data: ...
        if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(url)) { return 'mailto:' + url; }
        return 'https://' + url;
    }

    /* Clean an HTML string down to the allowed tags (used on paste + save). */
    function cleanHtml(html) {
        var doc = new DOMParser().parseFromString('<body>' + (html || '') + '</body>', 'text/html');
        var out = document.createElement('div');

        function walk(src, dest) {
            Array.prototype.forEach.call(src.childNodes, function (node) {
                if (node.nodeType === 3) {                       // text
                    dest.appendChild(document.createTextNode(node.nodeValue));
                    return;
                }
                if (node.nodeType !== 1) { return; }             // comments etc.
                var tag = node.tagName.toUpperCase();
                if (DROP_WITH_CONTENT.indexOf(tag) !== -1) { return; }

                // Word / Google Docs send <span style="font-weight:700"> etc.
                var style = (node.getAttribute('style') || '').toLowerCase();
                if (tag === 'SPAN') {
                    var wrap = dest;
                    if (/font-weight:\s*(bold|[6-9]00)/.test(style)) { wrap = wrap.appendChild(document.createElement('strong')); }
                    if (/font-style:\s*italic/.test(style)) { wrap = wrap.appendChild(document.createElement('em')); }
                    if (/text-decoration[^;]*underline/.test(style)) { wrap = wrap.appendChild(document.createElement('u')); }
                    walk(node, wrap);
                    return;
                }

                tag = RENAME[tag] || tag;
                if (!ALLOWED[tag]) { walk(node, dest); return; }  // unwrap, keep text

                var el = document.createElement(tag.toLowerCase());
                ALLOWED[tag].forEach(function (attr) {
                    var v = node.getAttribute(attr);
                    if (v === null) { return; }
                    if (attr === 'href') { v = normaliseUrl(v); if (!v) { return; } }
                    if (attr === 'target') { if (v !== '_blank') { return; } el.setAttribute('rel', 'noopener noreferrer'); }
                    el.setAttribute(attr, v);
                });
                if (tag === 'A' && !el.getAttribute('href')) { walk(node, dest); return; }
                dest.appendChild(el);
                walk(node, el);
            });
        }
        walk(doc.body, out);

        var result = out.innerHTML.trim();
        if (result === '<br>' || result === '<p></p>' || result === '<p><br></p>') { result = ''; }
        return result;
    }

    function escapeHtml(text) {
        var d = document.createElement('div');
        d.textContent = text;
        return d.innerHTML;
    }

    /* ---------------------------- toolbar -------------------------------- */
    var BUTTONS = [
        { cmd: 'bold',          icon: 'fas fa-bold',          label: 'B',   title: 'Bold (Ctrl+B)' },
        { cmd: 'italic',        icon: 'fas fa-italic',        label: 'I',   title: 'Italic (Ctrl+I)' },
        { cmd: 'underline',     icon: 'fas fa-underline',     label: 'U',   title: 'Underline (Ctrl+U)' },
        { cmd: 'strikeThrough', icon: 'fas fa-strikethrough', label: 'S',   title: 'Strikethrough' },
        { sep: true },
        { block: 'h2', label: 'H2', title: 'Heading 2' },
        { block: 'h3', label: 'H3', title: 'Heading 3' },
        { block: 'p',  label: '¶',  title: 'Normal text' },
        { sep: true },
        { cmd: 'insertUnorderedList', icon: 'fas fa-list-ul',     label: '•',  title: 'Bullet list' },
        { cmd: 'insertOrderedList',   icon: 'fas fa-list-ol',     label: '1.', title: 'Numbered list' },
        { block: 'blockquote',        icon: 'fas fa-quote-right', label: '“',  title: 'Quote' },
        { sep: true },
        { action: 'link',   icon: 'fas fa-link',   label: 'Link',   title: 'Add / edit hyperlink (Ctrl+K)', text: ' Link' },
        { cmd: 'unlink',    icon: 'fas fa-unlink', label: 'Unlink', title: 'Remove hyperlink' },
        { cmd: 'removeFormat', icon: 'fas fa-remove-format', label: 'Tx', title: 'Clear formatting' },
        { sep: true },
        { cmd: 'undo', icon: 'fas fa-undo', label: '↶', title: 'Undo (Ctrl+Z)' },
        { cmd: 'redo', icon: 'fas fa-redo', label: '↷', title: 'Redo (Ctrl+Y)' },
        { spacer: true },
        { action: 'source', icon: 'fas fa-code', label: '</>', title: 'Show / edit the HTML tags', text: ' HTML' }
    ];

    function makeButton(def) {
        var b = document.createElement('button');
        b.type = 'button';                          // never submits the form
        b.className = 'tb-rte-btn';
        b.title = def.title;
        b.setAttribute('aria-label', def.title);
        if (def.icon) {
            var i = document.createElement('i');
            i.className = def.icon;
            i.setAttribute('aria-hidden', 'true');
            b.appendChild(i);
            if (def.text) { b.appendChild(document.createTextNode(def.text)); }
        } else {
            b.textContent = def.label;
        }
        return b;
    }

    /* ----------------------------- editor -------------------------------- */
    function initEditor(textarea) {
        if (textarea.dataset.tbRte) { return; }
        // Skip Django's hidden "empty form" template row - it gets cloned.
        if ((textarea.name || '').indexOf('__prefix__') !== -1) { return; }
        textarea.dataset.tbRte = '1';

        var wrap = document.createElement('div');
        wrap.className = 'tb-rte';

        var toolbar = document.createElement('div');
        toolbar.className = 'tb-rte-toolbar';
        toolbar.setAttribute('role', 'toolbar');

        var area = document.createElement('div');
        area.className = 'tb-rte-area';
        area.contentEditable = 'true';
        area.setAttribute('role', 'textbox');
        area.setAttribute('aria-multiline', 'true');
        area.setAttribute('data-placeholder', 'Write the paragraph… select text and click Link to add a hyperlink.');

        /* link bar */
        var linkBar = document.createElement('div');
        linkBar.className = 'tb-rte-linkbar';
        linkBar.hidden = true;
        linkBar.innerHTML =
            '<input type="text" class="tb-rte-url" placeholder="https://example.com or /blog/my-post" autocomplete="off">' +
            '<input type="text" class="tb-rte-linktext" placeholder="Link text (optional)" autocomplete="off">' +
            '<label class="tb-rte-newtab"><input type="checkbox"> Open in new tab</label>' +
            '<button type="button" class="tb-rte-apply">Apply</button>' +
            '<button type="button" class="tb-rte-remove">Remove link</button>' +
            '<button type="button" class="tb-rte-cancel">Cancel</button>';
        var urlInput   = linkBar.querySelector('.tb-rte-url');
        var textInput  = linkBar.querySelector('.tb-rte-linktext');
        var newTabBox  = linkBar.querySelector('.tb-rte-newtab input');

        var hint = document.createElement('div');
        hint.className = 'tb-rte-hint';
        hint.textContent = 'Select words → Link (Ctrl+K) to add a hyperlink. “HTML” lets you type tags directly.';

        textarea.parentNode.insertBefore(wrap, textarea);
        wrap.appendChild(toolbar);
        wrap.appendChild(linkBar);
        wrap.appendChild(area);
        wrap.appendChild(textarea);
        wrap.appendChild(hint);
        textarea.classList.add('tb-rte-source');

        area.innerHTML = cleanHtml(textarea.value);

        var sourceMode = false;
        var savedRange = null;
        var editingLink = null;
        var stateButtons = [];
        var sourceBtn = null;

        function sync() {
            if (!sourceMode) { textarea.value = cleanHtml(area.innerHTML); }
        }

        function saveSelection() {
            var sel = window.getSelection();
            if (sel.rangeCount && area.contains(sel.anchorNode)) {
                savedRange = sel.getRangeAt(0).cloneRange();
            }
        }

        function restoreSelection() {
            area.focus();
            if (!savedRange) { return; }
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(savedRange);
        }

        function closestLink() {
            var sel = window.getSelection();
            var node = sel.rangeCount ? sel.anchorNode : null;
            while (node && node !== area) {
                if (node.nodeType === 1 && node.tagName === 'A') { return node; }
                node = node.parentNode;
            }
            return null;
        }

        function exec(cmd, value) {
            area.focus();
            try { document.execCommand('styleWithCSS', false, false); } catch (e) { /* ignore */ }
            document.execCommand(cmd, false, value || null);
            sync();
            updateState();
        }

        function formatBlock(tag) {
            var current = (document.queryCommandValue('formatBlock') || '').toLowerCase();
            // Clicking the same block style again turns it back into normal text.
            exec('formatBlock', '<' + (current === tag ? 'p' : tag) + '>');
        }

        /* ---- hyperlink ---- */
        function openLinkBar() {
            if (sourceMode) { return; }
            saveSelection();
            editingLink = closestLink();
            var selectedText = savedRange ? savedRange.toString() : '';
            if (editingLink) {
                urlInput.value  = editingLink.getAttribute('href') || '';
                textInput.value = editingLink.textContent;
                newTabBox.checked = editingLink.getAttribute('target') === '_blank';
            } else {
                urlInput.value  = '';
                textInput.value = selectedText;
                newTabBox.checked = false;
            }
            linkBar.querySelector('.tb-rte-remove').hidden = !editingLink;
            linkBar.hidden = false;
            urlInput.focus();
            urlInput.select();
        }

        function closeLinkBar() {
            linkBar.hidden = true;
            editingLink = null;
            restoreSelection();
        }

        function setTarget(a) {
            if (newTabBox.checked) {
                a.setAttribute('target', '_blank');
                a.setAttribute('rel', 'noopener noreferrer');
            } else {
                a.removeAttribute('target');
                a.removeAttribute('rel');
            }
        }

        function caretAfter(node) {
            if (!node || !node.parentNode) { return; }
            var r = document.createRange();
            r.setStartAfter(node);
            r.collapse(true);
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(r);
        }

        function applyLink() {
            var url = normaliseUrl(urlInput.value);
            if (!url) {
                urlInput.classList.add('is-invalid');
                urlInput.focus();
                return;
            }
            urlInput.classList.remove('is-invalid');
            var text = textInput.value;
            var lastLink = null;

            if (editingLink) {
                lastLink = editingLink;
                editingLink.setAttribute('href', url);
                if (text && text !== editingLink.textContent) { editingLink.textContent = text; }
                setTarget(editingLink);
            } else {
                restoreSelection();
                var selected = savedRange ? savedRange.toString() : '';
                if (!selected || (text && text !== selected)) {
                    // Nothing selected (or new text typed) -> insert a new link.
                    var marker = 'tb-new-link-' + Date.now();
                    document.execCommand('insertHTML', false,
                        '<a href="' + escapeHtml(url).replace(/"/g, '&quot;') + '" data-tb="' + marker + '">' +
                        escapeHtml(text || url) + '</a>&nbsp;');
                    var created = area.querySelector('a[data-tb="' + marker + '"]');
                    if (created) { created.removeAttribute('data-tb'); setTarget(created); lastLink = created; }
                } else {
                    // Turn the selected words into a link.
                    var tmp = 'about:tb-link-' + Date.now();
                    document.execCommand('createLink', false, tmp);
                    Array.prototype.forEach.call(area.querySelectorAll('a[href="' + tmp + '"]'), function (a) {
                        a.setAttribute('href', url);
                        setTarget(a);
                        lastLink = a;
                    });
                }
            }
            linkBar.hidden = true;
            editingLink = null;
            area.focus();
            // Put the cursor just after the link so typing doesn't replace it.
            if (lastLink) { caretAfter(lastLink); }
            sync();
            updateState();
        }

        function removeLink() {
            if (editingLink) {
                var parent = editingLink.parentNode;
                while (editingLink.firstChild) { parent.insertBefore(editingLink.firstChild, editingLink); }
                parent.removeChild(editingLink);
            }
            linkBar.hidden = true;
            editingLink = null;
            area.focus();
            sync();
        }

        /* ---- HTML source view ---- */
        function toggleSource() {
            if (!sourceMode) {
                sync();
                sourceMode = true;
                wrap.classList.add('is-source');
                linkBar.hidden = true;
                textarea.focus();
            } else {
                area.innerHTML = cleanHtml(textarea.value);
                sourceMode = false;
                wrap.classList.remove('is-source');
                sync();
                area.focus();
            }
            sourceBtn.classList.toggle('is-active', sourceMode);
            sourceBtn.setAttribute('aria-pressed', String(sourceMode));
        }

        /* ---- active state of B / I / U ... ---- */
        function updateState() {
            if (sourceMode) { return; }
            var block = (document.queryCommandValue('formatBlock') || '').toLowerCase();
            stateButtons.forEach(function (item) {
                var on = false;
                try {
                    if (item.def.cmd) { on = document.queryCommandState(item.def.cmd); }
                    else if (item.def.block) { on = block === item.def.block; }
                    else if (item.def.action === 'link') { on = !!closestLink(); }
                } catch (e) { on = false; }
                item.btn.classList.toggle('is-active', !!on);
            });
        }

        /* ---- build toolbar ---- */
        BUTTONS.forEach(function (def) {
            if (def.sep) {
                var s = document.createElement('span');
                s.className = 'tb-rte-sep';
                toolbar.appendChild(s);
                return;
            }
            if (def.spacer) {
                var sp = document.createElement('span');
                sp.className = 'tb-rte-spacer';
                toolbar.appendChild(sp);
                return;
            }
            var btn = makeButton(def);
            // mousedown + preventDefault keeps the text selection in the editor.
            btn.addEventListener('mousedown', function (e) { e.preventDefault(); });
            btn.addEventListener('click', function () {
                if (def.action === 'source') { toggleSource(); return; }
                if (sourceMode) { return; }
                if (def.action === 'link') { openLinkBar(); return; }
                if (def.block) { formatBlock(def.block); return; }
                exec(def.cmd);
            });
            if (def.action === 'source') { sourceBtn = btn; btn.classList.add('tb-rte-source-btn'); }
            else if (def.cmd !== 'undo' && def.cmd !== 'redo' && def.cmd !== 'unlink' && def.cmd !== 'removeFormat') {
                stateButtons.push({ btn: btn, def: def });
            }
            toolbar.appendChild(btn);
        });

        /* ---- events ---- */
        area.addEventListener('input', sync);
        area.addEventListener('blur', sync);
        area.addEventListener('keyup', updateState);
        area.addEventListener('mouseup', updateState);
        area.addEventListener('focus', function () {
            try { document.execCommand('defaultParagraphSeparator', false, 'p'); } catch (e) { /* ignore */ }
        });

        area.addEventListener('keydown', function (e) {
            if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
                e.preventDefault();
                openLinkBar();
            }
        });

        // Ctrl/Cmd + click opens a link in a new tab for checking it.
        area.addEventListener('click', function (e) {
            var a = e.target.closest ? e.target.closest('a') : null;
            if (a && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                window.open(a.href, '_blank', 'noopener');
            }
        });

        // Paste: keep links / bold / lists, drop Word / website styling.
        area.addEventListener('paste', function (e) {
            var cd = e.clipboardData || window.clipboardData;
            if (!cd) { return; }
            e.preventDefault();
            var html = cd.getData('text/html');
            var clean;
            if (html) {
                clean = cleanHtml(html);
            } else {
                var text = cd.getData('text/plain') || '';
                clean = escapeHtml(text).replace(/\r?\n/g, '<br>');
            }
            document.execCommand('insertHTML', false, clean);
            sync();
        });

        // Link bar keyboard: Enter applies (and must NOT submit the Django form).
        [urlInput, textInput].forEach(function (inp) {
            inp.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') { e.preventDefault(); applyLink(); }
                if (e.key === 'Escape') { e.preventDefault(); closeLinkBar(); }
            });
        });
        linkBar.querySelector('.tb-rte-apply').addEventListener('click', applyLink);
        linkBar.querySelector('.tb-rte-remove').addEventListener('click', removeLink);
        linkBar.querySelector('.tb-rte-cancel').addEventListener('click', closeLinkBar);

        // Make sure the latest HTML is in the textarea before saving.
        var form = textarea.form;
        if (form && !form.dataset.tbRteSubmit) {
            form.dataset.tbRteSubmit = '1';
            form.addEventListener('submit', function () {
                Array.prototype.forEach.call(form.querySelectorAll('.tb-rte'), function (w) {
                    if (w._tbSync) { w._tbSync(); }
                });
            }, true);
        }
        wrap._tbSync = function () {
            if (sourceMode) { textarea.value = cleanHtml(textarea.value); }
            else { sync(); }
        };
    }

    function initAll(root) {
        var scope = root && root.querySelectorAll ? root : document;
        Array.prototype.forEach.call(scope.querySelectorAll('textarea.tb-richtext'), initEditor);
        if (scope.matches && scope.matches('textarea.tb-richtext')) { initEditor(scope); }
    }

    ready(function () {
        initAll(document);

        // "Add another Paragraph" - Django 4.1+ fires a native event ...
        document.addEventListener('formset:added', function (e) { initAll(e.target); });
        // ... older jQuery-based event (Jazzmin / django.jQuery).
        if (window.django && window.django.jQuery) {
            window.django.jQuery(document).on('formset:added', function (e, row) {
                initAll(row && row[0] ? row[0] : document);
            });
        }
        // Fallback: watch for any new rows being inserted.
        if (window.MutationObserver) {
            new MutationObserver(function (mutations) {
                mutations.forEach(function (m) {
                    Array.prototype.forEach.call(m.addedNodes, function (n) {
                        if (n.nodeType === 1) { initAll(n); }
                    });
                });
            }).observe(document.body, { childList: true, subtree: true });
        }
    });
})();
