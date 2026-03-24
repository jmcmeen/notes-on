"""Download API for notes-on site. Serves individual and bundled notes as MD/HTML/PDF."""

import io
import os
import zipfile
from pathlib import Path

import markdown
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, StreamingResponse
from weasyprint import HTML

app = FastAPI(title="Notes Download API")

NOTES_DIR = Path(os.environ.get("NOTES_DIR", "/app/notes"))

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         max-width: 900px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6;
         color: #1a1a1a; }}
  h1 {{ border-bottom: 2px solid #4051b5; padding-bottom: 0.5rem; }}
  h2 {{ border-bottom: 1px solid #ddd; padding-bottom: 0.3rem; margin-top: 2rem; }}
  pre {{ background: #f5f5f5; border: 1px solid #ddd; border-radius: 6px;
         padding: 1rem; overflow-x: auto; }}
  code {{ font-family: "Fira Code", "Consolas", monospace; font-size: 0.9em; }}
  p code, li code {{ background: #f0f0f0; padding: 0.15em 0.4em; border-radius: 3px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
  th, td {{ border: 1px solid #ddd; padding: 0.5rem 0.75rem; text-align: left; }}
  th {{ background: #f5f5f5; }}
  blockquote {{ border-left: 4px solid #4051b5; margin: 1rem 0; padding: 0.5rem 1rem;
                background: #f8f9ff; }}
  a {{ color: #4051b5; }}
  hr {{ border: none; border-top: 1px solid #ddd; margin: 2rem 0; }}
  @media print {{ body {{ max-width: 100%; margin: 0; }} }}
</style>
</head>
<body>
{content}
</body>
</html>"""

MD_EXTENSIONS = [
    "fenced_code",
    "codehilite",
    "tables",
    "toc",
    "sane_lists",
]


def get_note_path(filename: str) -> Path:
    """Resolve and validate a note file path."""
    if "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    path = NOTES_DIR / filename
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail=f"Note not found: {filename}")
    return path


def render_md_to_html(md_content: str, title: str) -> str:
    """Render markdown content to a standalone HTML page."""
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    html_body = md.convert(md_content)
    return HTML_TEMPLATE.format(title=title, content=html_body)


def render_html_to_pdf(html_content: str) -> bytes:
    """Convert an HTML string to PDF bytes."""
    return HTML(string=html_content).write_pdf()


def note_title(filename: str) -> str:
    """Derive a human-readable title from a filename."""
    return filename.replace(".md", "").replace("_", " ").replace("-", " ").title()


@app.get("/api/notes")
def list_notes():
    """List all available notes."""
    files = sorted(f.name for f in NOTES_DIR.glob("*.md"))
    return {"notes": files, "count": len(files)}


@app.get("/api/download/{filename}")
def download_note(filename: str, format: str = Query("md", pattern="^(md|html|pdf)$")):
    """Download a single note in the specified format."""
    path = get_note_path(filename)
    md_content = path.read_text(encoding="utf-8")
    title = note_title(filename)
    stem = path.stem

    if format == "md":
        return Response(
            content=md_content,
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="{stem}.md"'},
        )

    html_content = render_md_to_html(md_content, title)

    if format == "html":
        return Response(
            content=html_content,
            media_type="text/html",
            headers={"Content-Disposition": f'attachment; filename="{stem}.html"'},
        )

    pdf_bytes = render_html_to_pdf(html_content)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{stem}.pdf"'},
    )


@app.get("/api/download-all")
def download_all(format: str = Query("md", pattern="^(md|html|pdf)$")):
    """Download all notes as a ZIP archive in the specified format."""
    md_files = sorted(NOTES_DIR.glob("*.md"))
    if not md_files:
        raise HTTPException(status_code=404, detail="No notes found")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in md_files:
            md_content = path.read_text(encoding="utf-8")
            stem = path.stem
            title = note_title(path.name)

            if format == "md":
                zf.writestr(f"{stem}.md", md_content)
            elif format == "html":
                html_content = render_md_to_html(md_content, title)
                zf.writestr(f"{stem}.html", html_content)
            elif format == "pdf":
                html_content = render_md_to_html(md_content, title)
                pdf_bytes = render_html_to_pdf(html_content)
                zf.writestr(f"{stem}.pdf", pdf_bytes)

    buf.seek(0)
    ext = format if format != "md" else "md"
    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="notes-on-{ext}-bundle.zip"'},
    )


@app.get("/api/health")
def health():
    return {"status": "ok"}
