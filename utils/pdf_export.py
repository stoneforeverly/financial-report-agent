import markdown as md_lib


_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC&family=Noto+Sans+TC&display=swap');

body {
    font-family: 'Noto Sans SC', 'Noto Sans TC', Arial, sans-serif;
    margin: 48px;
    color: #222;
    line-height: 1.7;
    font-size: 13px;
}
h1 {
    color: #1a1a2e;
    border-bottom: 2px solid #2c5f8a;
    padding-bottom: 8px;
    font-size: 20px;
}
h2 {
    color: #16213e;
    margin-top: 28px;
    font-size: 15px;
    border-left: 4px solid #2c5f8a;
    padding-left: 8px;
}
em { color: #666; font-size: 12px; }
p { margin: 8px 0; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th, td { border: 1px solid #ddd; padding: 6px 10px; text-align: left; }
th { background-color: #f0f4f8; font-weight: bold; }
hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }
"""


def md_to_pdf(md_text: str) -> bytes:
    html_body = md_lib.markdown(md_text, extensions=["tables", "fenced_code"])
    html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<style>{_CSS}</style>
</head><body>{html_body}</body></html>"""

    from weasyprint import HTML
    return HTML(string=html).write_pdf()
