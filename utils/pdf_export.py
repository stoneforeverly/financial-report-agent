import io
import markdown as md_lib
from xhtml2pdf import pisa

_CSS = """
body {
    font-family: Helvetica, Arial, sans-serif;
    margin: 48px;
    color: #222;
    line-height: 1.7;
    font-size: 11px;
}
h1 {
    color: #1a1a2e;
    border-bottom: 2px solid #2c5f8a;
    padding-bottom: 6px;
    font-size: 18px;
}
h2 {
    color: #16213e;
    margin-top: 24px;
    font-size: 13px;
    border-left: 4px solid #2c5f8a;
    padding-left: 7px;
}
em { color: #666; font-size: 10px; }
p  { margin: 5px 0; }
hr { border-top: 1px solid #ddd; margin: 16px 0; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; }
th, td { border: 1px solid #ddd; padding: 5px 8px; text-align: left; }
th { background-color: #f0f4f8; font-weight: bold; }
"""


def md_to_pdf(md_text: str) -> bytes:
    html_body = md_lib.markdown(md_text, extensions=["tables", "fenced_code"])
    html = (
        "<!DOCTYPE html><html><head>"
        '<meta charset="utf-8">'
        f"<style>{_CSS}</style>"
        f"</head><body>{html_body}</body></html>"
    )
    buffer = io.BytesIO()
    result = pisa.CreatePDF(html, dest=buffer)
    if result.err:
        raise RuntimeError(f"PDF generation failed (error code {result.err})")
    return buffer.getvalue()
