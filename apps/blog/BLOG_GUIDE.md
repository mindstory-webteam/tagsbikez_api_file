# TagsBikez — Blog Module (matches `blogsData`)

The `apps.blog` app now mirrors your front-end `blogsData` shape. **No HTML body.**
Each post has a `content` array of plain-text paragraphs, plus
`slug, title, excerpt, author, date, popular, image`.

## Models
- **BlogPost** — `title, slug (auto), excerpt, author, image, popular, published_date, display_order, is_active`
- **BlogParagraph** — `post (FK), text, display_order` → serialized into the flat `content: [...]` array.

In admin: open a Blog Post and add paragraphs in the **Content Paragraphs** inline
(one row per paragraph, `display_order` controls order).

## Endpoints (all under `/api/`)
| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/api/blog/` | listing grid (paginated). `?popular=true` `?author=` `?title=` `?search=` `?ordering=-published_date` `?page=1&page_size=12` |
| GET | `/api/blog/popular/` | POPULAR sidebar (array, not paginated) |
| GET | `/api/blog/<slug>/` | inner page (adds `content[]`, `previous_post`, `next_post`) |

### Card JSON (list + popular)
```json
{
  "id": 1,
  "slug": "meteor-350-city-cruising-perfected",
  "title": "Meteor 350: City Cruising Perfected",
  "excerpt": "Navigate the urban jungle with ease.",
  "author": "Admin",
  "date": "Mar 08, 2026",
  "popular": true,
  "image": "http://.../media/blog/images/meteor.jpg",
  "display_order": 0
}
```

### Detail JSON (`/api/blog/<slug>/`)
```json
{
  "slug": "hunter-350-the-new-rebel",
  "title": "Hunter 350: The New Rebel on the Streets",
  "excerpt": "Compact, punchy, and incredibly fun.",
  "content": [
    "Royal Enfield took the motorcycle world by storm ...",
    "Its compact wheelbase and 17-inch wheels ...",
    "It's the perfect canvas for young riders."
  ],
  "author": "Admin",
  "date": "Mar 05, 2026",
  "popular": false,
  "image": "http://.../media/blog/images/hunter.jpg",
  "previous_post": { "slug": "...", "title": "...", "image": "..." },
  "next_post":     { "slug": "...", "title": "...", "image": "..." }
}
```

The detail shape is a drop-in for your `getPostBySlug(slug)` object — just render
`post.content.map(p => <p>{p}</p>)` (no `dangerouslySetInnerHTML` needed).

## Front-end swap
Replace the static import with a fetch:
```js
// list page
const { results } = await fetch('/api/blog/').then(r => r.json());
const popular     = await fetch('/api/blog/popular/').then(r => r.json());

// detail page (was getPostBySlug)
const post = await fetch(`/api/blog/${slug}/`).then(r => r.json());
```
`img.himalayan450` etc. becomes `post.image` (an absolute URL from the API).

## Install / migrate

**If you already ran `migrate` once with the earlier blog version**, reset the app
first (there is no real blog data yet), then apply the new schema:

```bash
source venv/bin/activate
python manage.py migrate blog zero      # drops the old blog tables (run with your CURRENT files, before copying new ones)
# ...now copy the new apps/blog files + updated apps/api files over...
python manage.py migrate                # applies the new blog.0001_initial
```

**If you have NOT migrated blog yet**, just:
```bash
python manage.py migrate
```

Then create/manage posts in admin → **Blog → Blog Posts**.
