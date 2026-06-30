# TagsBikez — Blog Module

A new **`apps.blog`** app was added that matches the BLOGS listing page and the
inner article page in your screenshots. It follows the exact conventions already
used by `events`, `careers`, `gallery`, etc. (models live in their own app, the
REST layer lives in `apps/api/`). **No existing endpoint or model was changed** —
everything is additive.

---

## 1. What was added / touched

**New files**
```
apps/blog/__init__.py
apps/blog/apps.py
apps/blog/models.py
apps/blog/admin.py
apps/blog/migrations/0001_initial.py
```

**Edited (additive only — existing code untouched)**
```
config/settings.py        + 'apps.blog' in INSTALLED_APPS, + Jazzmin icon
config/urls.py            + blog links in the api_root index
apps/api/serializers.py   + 3 blog serializers (+ import)
apps/api/filters.py       + BlogPostFilter (+ import)
apps/api/views.py         + 3 blog views (+ imports)
apps/api/urls.py          + 3 blog routes (+ import)
```

---

## 2. Install / run

```bash
pip install -r requirements.txt        # unchanged deps
python manage.py migrate               # applies blog.0001_initial
python manage.py runserver
```

Open the admin → **Blog → Blog Posts → Add**. Create a post, tick **is_popular**
for the sidebar, hit save. The API is live immediately.

---

## 3. Data model — `BlogPost`

| Field                | Used on screen                                   |
|----------------------|--------------------------------------------------|
| `title`              | card heading, hero title, breadcrumb             |
| `slug`               | URL (auto-generated, unique)                     |
| `author`             | "Admin" by-line                                  |
| `featured_image`     | card image, sidebar thumb, detail image          |
| `excerpt`            | card preview line                                |
| `intro`              | lead paragraph on the detail page                |
| `highlight`          | the big **RED** sub-heading                      |
| `body_image`         | image beside the body text (optional)            |
| `body_image_caption` | "1/3 Scenic riding route captured"               |
| `body`               | **the HTML inner-page body** (accepts raw HTML)  |
| `meta_description`   | `<meta>` / link preview                          |
| `is_popular`         | drives the POPULAR sidebar                       |
| `published_date`     | "Mar 05, 2026"                                   |
| `display_order`      | manual ordering tie-breaker                      |
| `is_active`          | hide/show without deleting                       |

`read_time_minutes`, `previous_post`, `next_post` are **computed automatically**
— editors never set them.

---

## 4. API reference (all under `/api/`)

### `GET /api/blog/` — listing grid (paginated)
Query params: `?is_popular=true` · `?author=admin` · `?title=hunter` ·
`?search=hunter` (title/excerpt/body) · `?ordering=-published_date` ·
`?page=1&page_size=12`

```json
{
  "count": 6,
  "next": "http://.../api/blog/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Hunter 350: The New Rebel on the Streets",
      "slug": "hunter-350-the-new-rebel-on-the-streets",
      "author": "Admin",
      "excerpt": "Compact, punchy, and incredibly fun.",
      "featured_image_url": "http://.../media/blog/featured/hunter.jpg",
      "published_date": "2026-03-05",
      "is_popular": true,
      "display_order": 0
    }
  ]
}
```

### `GET /api/blog/popular/` — POPULAR sidebar (NOT paginated)
Returns the same card shape as above, filtered to `is_popular=true`, as a plain
array.

### `GET /api/blog/<slug>/` — inner / detail page
```json
{
  "id": 1,
  "title": "Hunter 350: The New Rebel on the Streets",
  "slug": "hunter-350-the-new-rebel-on-the-streets",
  "author": "Admin",
  "published_date": "2026-03-05",
  "featured_image_url": "http://.../media/blog/featured/hunter.jpg",
  "excerpt": "Compact, punchy, and incredibly fun.",
  "intro": "Royal Enfield took the motorcycle world by storm ...",
  "highlight": "Find out why the Hunter 350 is capturing the hearts of young riders.",
  "body_image_url": "http://.../media/blog/body/route.jpg",
  "body_image_caption": "1/3 Scenic riding route captured",
  "body": "<p>Its compact wheelbase and 17-inch wheels ...</p><h3>Future Legend</h3><p>...</p>",
  "meta_description": "The new rebel on the streets.",
  "read_time_minutes": 3,
  "is_popular": true,
  "display_order": 0,
  "is_active": true,
  "previous_post": { "id": 2, "title": "Meteor 350: City Cruising Perfected", "slug": "meteor-350-city-cruising-perfected", "featured_image_url": "..." },
  "next_post":     { "id": 3, "title": "Understanding RE Tripper Navigation", "slug": "understanding-re-tripper-navigation", "featured_image_url": "..." },
  "created_at": "...",
  "updated_at": "..."
}
```
A missing slug returns your standard wrapped error:
`{ "success": false, "error": { "detail": "No BlogPost matches the given query." } }`

---

## 5. Front-end: rendering the inner-page **HTML body area**

The `body` field is raw HTML. Render it as HTML (don't escape it).

**React**
```jsx
function BlogDetail({ post }) {
  return (
    <article>
      <h1>{post.title}</h1>
      <p className="byline">{post.author} - {formatDate(post.published_date)}</p>

      {post.intro && <p className="lead">{post.intro}</p>}
      {post.highlight && <h2 className="highlight-red">{post.highlight}</h2>}

      <div className="body-grid">
        {post.body_image_url && (
          <figure>
            <img src={post.body_image_url} alt={post.title} />
            <figcaption>{post.body_image_caption}</figcaption>
          </figure>
        )}
        {/* the HTML body area */}
        <div
          className="post-body"
          dangerouslySetInnerHTML={{ __html: post.body }}
        />
      </div>

      <nav className="prev-next">
        {post.previous_post && (
          <a href={`/blogs/${post.previous_post.slug}`}>
            PREVIOUS · {post.previous_post.title}
          </a>
        )}
        {post.next_post && (
          <a href={`/blogs/${post.next_post.slug}`}>
            NEXT · {post.next_post.title}
          </a>
        )}
      </nav>
    </article>
  );
}
```

**Vue**
```vue
<div class="post-body" v-html="post.body"></div>
```

**Listing + sidebar**
```js
const grid    = await fetch('/api/blog/').then(r => r.json());        // .results
const popular = await fetch('/api/blog/popular/').then(r => r.json()); // array
```

> **Security note:** `body` is admin-authored, so raw HTML is safe here. If you
> ever open authoring to untrusted users, sanitise on input (e.g. `bleach`) or on
> output (e.g. `DOMPurify`) before injecting it.

---

## 6. Notes
- `previous_post` = the **newer** neighbour, `next_post` = the **older** one,
  matching the PREVIOUS/NEXT layout in the screenshot. Both follow the same
  active-post ordering as the listing.
- Ordering is `-published_date, display_order, -id`. Pin a post by lowering its
  `display_order`.
- Slug is auto-built from the title and de-duplicated (`-2`, `-3`, …) so two
  posts with the same title won't collide.
