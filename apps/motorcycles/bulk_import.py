"""
apps/motorcycles/bulk_import.py

Bulk-import MotorcycleProduct rows from an Excel (.xlsx) or CSV file.
Existing code is NOT modified — this file is additive only.

Expected columns (case-insensitive, order flexible):
  category_name | name | description | engine_cc | power | torque |
  emi_starts_at | coming_soon | display_order | is_active
"""

import csv
import io
import traceback

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods

from apps.categories.models import ProductCategory
from .models import MotorcycleProduct


# ── helpers ───────────────────────────────────────────────────────────────────

REQUIRED_COLS = {"name", "category_name", "description"}

BOOL_TRUE  = {"1", "true", "yes", "y", "on"}
BOOL_FALSE = {"0", "false", "no", "n", "off", ""}


def _parse_bool(value: str, default: bool = False) -> bool:
    v = str(value).strip().lower()
    if v in BOOL_TRUE:
        return True
    if v in BOOL_FALSE:
        return False
    return default


def _normalise_header(h: str) -> str:
    return h.strip().lower().replace(" ", "_").replace("-", "_")


def _read_rows_csv(file_bytes: bytes) -> list[dict]:
    text    = file_bytes.decode("utf-8-sig", errors="replace")
    reader  = csv.DictReader(io.StringIO(text))
    headers = [_normalise_header(h) for h in (reader.fieldnames or [])]
    rows    = []
    for row in reader:
        rows.append({_normalise_header(k): v for k, v in row.items()})
    return rows, headers


def _read_rows_excel(file_bytes: bytes) -> list[dict]:
    """Pure-stdlib fallback + openpyxl if available."""
    try:
        import openpyxl
    except ImportError:
        raise ImportError(
            "openpyxl is not installed. "
            "Run: pip install openpyxl  — or upload a CSV file instead."
        )
    wb   = openpyxl.load_workbook(io.BytesIO(file_bytes), read_only=True, data_only=True)
    ws   = wb.active
    rows_iter = iter(ws.iter_rows(values_only=True))
    raw_headers = next(rows_iter, None)
    if raw_headers is None:
        return [], []
    headers = [_normalise_header(str(h or "")) for h in raw_headers]
    rows    = []
    for raw in rows_iter:
        row = {headers[i]: str(raw[i] if raw[i] is not None else "").strip()
               for i in range(min(len(headers), len(raw)))}
        rows.append(row)
    return rows, headers


# ── main import logic ─────────────────────────────────────────────────────────

def _import_rows(rows: list[dict]) -> dict:
    created  = 0
    updated  = 0
    skipped  = 0
    errors   = []

    for idx, row in enumerate(rows, start=2):          # row 2 = first data row
        name          = row.get("name", "").strip()
        category_name = row.get("category_name", "").strip()
        description   = row.get("description", "").strip()

        if not name:
            errors.append(f"Row {idx}: 'name' is empty — skipped.")
            skipped += 1
            continue
        if not category_name:
            errors.append(f"Row {idx} ({name!r}): 'category_name' is empty — skipped.")
            skipped += 1
            continue

        # Resolve or create category
        try:
            category = ProductCategory.objects.get(name__iexact=category_name)
        except ProductCategory.DoesNotExist:
            category = ProductCategory.objects.create(
                name=category_name,
                slug=slugify(category_name),
            )

        slug = slugify(name)

        defaults = dict(
            category      = category,
            description   = description,
            engine_cc     = row.get("engine_cc", "").strip(),
            power         = row.get("power", "").strip(),
            torque        = row.get("torque", "").strip(),
            emi_starts_at = row.get("emi_starts_at", "").strip(),
            coming_soon   = _parse_bool(row.get("coming_soon", ""), False),
            is_active     = _parse_bool(row.get("is_active", "1"), True),
        )
        raw_order = row.get("display_order", "").strip()
        if raw_order.isdigit():
            defaults["display_order"] = int(raw_order)

        try:
            obj, was_created = MotorcycleProduct.objects.update_or_create(
                slug=slug,
                defaults={**defaults, "name": name},
            )
            if was_created:
                created += 1
            else:
                updated += 1
        except Exception as exc:
            errors.append(f"Row {idx} ({name!r}): {exc}")
            skipped += 1

    return {"created": created, "updated": updated, "skipped": skipped, "errors": errors}


# ── template (inline, no extra template files needed) ─────────────────────────

_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Bulk Import — Motorcycle Products</title>
<style>
  body { font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
         background:#f5f5f5; color:#333; margin:0; }
  .wrap { max-width:860px; margin:40px auto; background:#fff;
          border-radius:8px; padding:36px 44px; box-shadow:0 2px 12px rgba(0,0,0,.08); }
  h1   { font-size:1.5rem; margin-bottom:4px; }
  .breadcrumb { font-size:.85rem; color:#666; margin-bottom:28px; }
  .breadcrumb a { color:#417690; text-decoration:none; }
  label  { display:block; font-weight:600; margin-bottom:8px; }
  input[type=file] { display:block; padding:8px; border:1px solid #ccc;
                     border-radius:4px; width:100%; max-width:400px; }
  .btn-primary {
    margin-top:20px; padding:10px 28px; background:#417690; color:#fff;
    border:none; border-radius:4px; font-size:1rem; cursor:pointer;
  }
  .btn-primary:hover { background:#2b5068; }
  .btn-secondary {
    margin-top:20px; padding:10px 20px; background:#6c757d; color:#fff;
    border:none; border-radius:4px; font-size:1rem; cursor:pointer;
    text-decoration:none; display:inline-block; margin-left:12px;
  }
  .alert { padding:14px 18px; border-radius:4px; margin-bottom:20px; }
  .alert-success { background:#d4edda; color:#155724; border:1px solid #c3e6cb; }
  .alert-warning { background:#fff3cd; color:#856404; border:1px solid #ffeeba; }
  .alert-error   { background:#f8d7da; color:#721c24; border:1px solid #f5c6cb; }
  .result-table { width:100%; border-collapse:collapse; margin-top:10px; }
  .result-table td { padding:8px 12px; border:1px solid #dee2e6; }
  .result-table tr:first-child td { background:#f8f9fa; font-weight:700; }
  pre { background:#f4f4f4; padding:14px; border-radius:4px;
        font-size:.82rem; max-height:260px; overflow:auto; }
  .hint { font-size:.82rem; color:#555; margin-top:20px; background:#f9f9f9;
          border:1px solid #e0e0e0; border-radius:4px; padding:14px 18px; }
  .hint code { background:#eee; padding:1px 4px; border-radius:3px; font-size:.82rem; }
  .dl-link { display:inline-block; margin-top:8px; color:#417690; font-size:.85rem; }
</style>
</head>
<body>
<div class="wrap">

  <div class="breadcrumb">
    <a href="/admin/">Home</a> &rsaquo;
    <a href="/admin/motorcycles/motorcycleproduct/">Motorcycle Products</a> &rsaquo;
    Bulk Import
  </div>

  <h1>📥 Bulk Import — Motorcycle Products</h1>

  {% if result %}
    <div class="alert alert-{{ result.level }}">
      <strong>{{ result.headline }}</strong>
    </div>
    <table class="result-table">
      <tr><td>✅ Created</td><td>{{ result.created }}</td></tr>
      <tr><td>🔄 Updated</td><td>{{ result.updated }}</td></tr>
      <tr><td>⚠️ Skipped</td><td>{{ result.skipped }}</td></tr>
    </table>
    {% if result.errors %}
      <p style="margin-top:16px;font-weight:600;">Row errors:</p>
      <pre>{% for e in result.errors %}{{ e }}
{% endfor %}</pre>
    {% endif %}
    <a href="/admin/motorcycles/motorcycleproduct/" class="btn-secondary">← Back to list</a>
    <br><br><hr>
  {% endif %}

  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <label for="import_file">Select Excel (.xlsx) or CSV file:</label>
    <input type="file" id="import_file" name="import_file"
           accept=".xlsx,.csv,.xls" required>
    <button type="submit" class="btn-primary">🚀 Import Now</button>
    <a href="/admin/motorcycles/motorcycleproduct/" class="btn-secondary">Cancel</a>
  </form>

  <div class="hint">
    <strong>📋 Required columns</strong> (header row, case-insensitive):
    <br><br>
    <code>category_name</code> &nbsp;|&nbsp;
    <code>name</code> &nbsp;|&nbsp;
    <code>description</code> &nbsp;|&nbsp;
    <code>engine_cc</code> &nbsp;|&nbsp;
    <code>power</code> &nbsp;|&nbsp;
    <code>torque</code> &nbsp;|&nbsp;
    <code>emi_starts_at</code> &nbsp;|&nbsp;
    <code>coming_soon</code> &nbsp;|&nbsp;
    <code>display_order</code> &nbsp;|&nbsp;
    <code>is_active</code>
    <br><br>
    • Only <code>name</code>, <code>category_name</code>, <code>description</code> are required.<br>
    • Boolean columns accept: <code>1 / 0</code>, <code>true / false</code>, <code>yes / no</code>.<br>
    • Rows are matched by <strong>slug</strong> (derived from <code>name</code>); existing rows are <em>updated</em>.<br>
    • Unknown categories are <strong>auto-created</strong>.<br>
    • Images / brochures cannot be imported via spreadsheet — upload them per-product after import.<br><br>
    <a class="dl-link" href="?download_template=1">⬇ Download sample template (.csv)</a>
  </div>
</div>
</body>
</html>
"""


# ── views ─────────────────────────────────────────────────────────────────────

@staff_member_required
@require_http_methods(["GET", "POST"])
def bulk_import_view(request):

    # ── sample template download ───────────────────────────────────────────
    if request.method == "GET" and request.GET.get("download_template"):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="motorcycle_import_template.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "category_name", "name", "description",
            "engine_cc", "power", "torque",
            "emi_starts_at", "coming_soon", "display_order", "is_active",
        ])
        writer.writerow([
            "Street", "Demo Bike 125",
            "A great entry-level motorcycle with a peppy engine.",
            "124cc", "10.7 bhp", "10.6 Nm",
            "₹2,999/month", "0", "1", "1",
        ])
        return response

    result_ctx = None

    if request.method == "POST":
        upload = request.FILES.get("import_file")
        if not upload:
            messages.error(request, "No file was uploaded.")
            return redirect(request.path)

        fname = upload.name.lower()
        raw   = upload.read()

        try:
            if fname.endswith(".csv"):
                rows, headers = _read_rows_csv(raw)
            elif fname.endswith((".xlsx", ".xls")):
                rows, headers = _read_rows_excel(raw)
            else:
                messages.error(request, "Unsupported file type. Please upload .xlsx or .csv")
                return redirect(request.path)
        except ImportError as exc:
            result_ctx = {
                "level":    "error",
                "headline": str(exc),
                "created":  0, "updated": 0, "skipped": 0,
                "errors":   [],
            }
            from django.template import Template, Context, RequestContext
            t = Template("{% load i18n %}" + _TEMPLATE.replace("{% block extrastyle %}{{ block.super }}{% endblock %}", ""))
            # fall through to render below
        except Exception as exc:
            result_ctx = {
                "level":    "error",
                "headline": f"Could not parse file: {exc}",
                "created":  0, "updated": 0, "skipped": 0,
                "errors":   [traceback.format_exc()],
            }

        if result_ctx is None:
            # Validate headers
            missing = REQUIRED_COLS - set(headers)
            if missing:
                result_ctx = {
                    "level":    "error",
                    "headline": f"Missing required column(s): {', '.join(sorted(missing))}",
                    "created":  0, "updated": 0, "skipped": 0,
                    "errors":   [],
                }
            else:
                res = _import_rows(rows)
                level = "success" if not res["errors"] else "warning"
                headline = (
                    f"Import complete — {res['created']} created, "
                    f"{res['updated']} updated, {res['skipped']} skipped."
                )
                result_ctx = {**res, "level": level, "headline": headline}

    from django.template import Template, RequestContext
    t = Template(_TEMPLATE)
    ctx = RequestContext(request, {"result": result_ctx})
    return HttpResponse(t.render(ctx))