"""
apps/blog/html_sanitizer.py

Small, dependency-free HTML cleaner for blog paragraph text.

Only a safe whitelist of tags survives (bold, italic, underline, links,
lists, headings, line breaks ...). Everything else is stripped, all
attributes except a link's href / target / title are dropped, and
"javascript:" style links are removed. Plain text (old paragraphs)
passes through safely escaped.
"""

from html import escape
from html.parser import HTMLParser

# tag -> allowed attributes
ALLOWED_TAGS = {
    'a': {'href', 'target', 'title'},
    'b': set(), 'strong': set(),
    'i': set(), 'em': set(),
    'u': set(), 's': set(),
    'p': set(), 'br': set(),
    'ul': set(), 'ol': set(), 'li': set(),
    'h2': set(), 'h3': set(), 'h4': set(),
    'blockquote': set(),
}
VOID_TAGS = {'br'}
# Tags whose *content* must be thrown away too (not just the tag).
DROP_CONTENT_TAGS = {'script', 'style', 'iframe', 'object', 'embed', 'noscript', 'template'}
# Tags that are converted rather than stripped.
RENAME_TAGS = {'div': 'p'}

SAFE_URL_PREFIXES = ('http://', 'https://', 'mailto:', 'tel:', '/', '#', '?')


def _safe_href(value):
    value = (value or '').strip()
    if not value:
        return None
    # Remove whitespace/control chars browsers ignore (blocks "java\tscript:").
    compact = ''.join(ch for ch in value if ch > ' ').lower()
    if compact.startswith(SAFE_URL_PREFIXES):
        return value
    # Bare domain like "www.example.com" -> make it absolute.
    if ':' not in compact.split('/')[0] and '.' in compact.split('/')[0]:
        return 'https://' + value
    return None


class _Cleaner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.open_tags = []
        self.drop_depth = 0

    # -- tags ---------------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in DROP_CONTENT_TAGS:
            self.drop_depth += 1
            return
        if self.drop_depth:
            return
        tag = RENAME_TAGS.get(tag, tag)
        if tag not in ALLOWED_TAGS:
            return

        allowed = ALLOWED_TAGS[tag]
        clean = []
        for name, value in attrs:
            name = (name or '').lower()
            if name not in allowed:
                continue
            if name == 'href':
                value = _safe_href(value)
                if value is None:
                    continue
            if name == 'target':
                value = '_blank' if value == '_blank' else None
                if value is None:
                    continue
            clean.append((name, value or ''))

        if tag == 'a':
            if not any(n == 'href' for n, _ in clean):
                # A link without a usable href -> keep only its text.
                self.open_tags.append(None)
                return
            if any(n == 'target' for n, _ in clean):
                clean.append(('rel', 'noopener noreferrer'))

        attr_str = ''.join(f' {n}="{escape(v, quote=True)}"' for n, v in clean)
        if tag in VOID_TAGS:
            self.out.append(f'<{tag}{attr_str}>')
            return
        self.out.append(f'<{tag}{attr_str}>')
        self.open_tags.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        tag = RENAME_TAGS.get(tag.lower(), tag.lower())
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in DROP_CONTENT_TAGS:
            self.drop_depth = max(0, self.drop_depth - 1)
            return
        if self.drop_depth:
            return
        tag = RENAME_TAGS.get(tag, tag)
        if tag in VOID_TAGS or tag not in ALLOWED_TAGS:
            return
        # Close the most recent matching open tag (and anything left open inside it).
        for idx in range(len(self.open_tags) - 1, -1, -1):
            open_tag = self.open_tags[idx]
            if open_tag == tag or (open_tag is None and tag == 'a'):
                for t in reversed(self.open_tags[idx:]):
                    if t:
                        self.out.append(f'</{t}>')
                del self.open_tags[idx:]
                return

    # -- text ---------------------------------------------------------------
    def handle_data(self, data):
        if not self.drop_depth:
            self.out.append(escape(data, quote=False))

    def result(self):
        for t in reversed(self.open_tags):
            if t:
                self.out.append(f'</{t}>')
        self.open_tags = []
        return ''.join(self.out)


def sanitize_html(value):
    """Return a safe HTML string containing only whitelisted tags."""
    if not value:
        return ''
    cleaner = _Cleaner()
    cleaner.feed(str(value))
    cleaner.close()
    html = cleaner.result().strip()
    # An editor left with only empty markup -> treat as empty.
    if html in ('<br>', '<p></p>', '<p><br></p>'):
        return ''
    return html
