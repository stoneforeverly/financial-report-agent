import io
import re
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    HRFlowable, Paragraph, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

_CJK_FONTS = {
    "zh-cn": "STSong-Light",
    "zh-tw": "MSung-Light",
}

_ACCENT   = colors.HexColor("#2c5f8a")
_DARK     = colors.HexColor("#1a1a2e")
_MID      = colors.HexColor("#16213e")
_LIGHT_BG = colors.HexColor("#eef4fa")
_GREY     = colors.HexColor("#666666")
_RULE     = colors.HexColor("#dddddd")

_UNICODE_MAP = {
    "\u2014": " - ",
    "\u2013": " - ",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2026": "...",
    "\u00a9": "(c)",
    "\u00ae": "(R)",
    "\u2122": "(TM)",
    "\u2192": "->",
    "\u00b7": "*",
}


def _sanitize(text: str, is_cjk: bool) -> str:
    if not is_cjk:
        for ch, rep in _UNICODE_MAP.items():
            text = text.replace(ch, rep)
    text = escape(text)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    return text


def _register_fonts(language: str) -> tuple[str, str]:
    cid = _CJK_FONTS.get(language)
    if cid:
        pdfmetrics.registerFont(UnicodeCIDFont(cid))
        return cid, cid
    return "Helvetica", "Helvetica-Bold"


def _header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    # 顶部装饰条
    canvas.setFillColor(_ACCENT)
    canvas.rect(0, h - 0.6 * cm, w, 0.6 * cm, fill=1, stroke=0)
    # 页码
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(_GREY)
    canvas.drawRightString(w - 2 * cm, 1 * cm, f"Page {doc.page}")
    # 底部细线
    canvas.setStrokeColor(_RULE)
    canvas.setLineWidth(0.5)
    canvas.line(2 * cm, 1.4 * cm, w - 2 * cm, 1.4 * cm)
    canvas.restoreState()


def _section_header(text: str, normal: str, bold: str) -> Table:
    """H2 带色块背景的节标题"""
    inner = ParagraphStyle("h2i", fontName=bold, fontSize=12,
                           textColor=_DARK, leading=16)
    cell = Paragraph(text, inner)
    t = Table([[cell]], colWidths=[16.2 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), _LIGHT_BG),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBEFORE",    (0, 0), (0, -1), 4, _ACCENT),
    ]))
    return t


def _bullet_para(text: str, normal: str) -> Paragraph:
    style = ParagraphStyle("bullet", fontName=normal, fontSize=10,
                           leftIndent=14, firstLineIndent=0,
                           spaceAfter=3, leading=14,
                           bulletFontName=normal, bulletFontSize=10,
                           bulletIndent=4, bulletText="•")
    return Paragraph(text, style)


def md_to_pdf(md_text: str, language: str = "en") -> bytes:
    normal, bold = _register_fonts(language)
    is_cjk = language in _CJK_FONTS

    h1_style   = ParagraphStyle("h1",   fontName=bold,   fontSize=18, spaceAfter=8,
                                 textColor=_DARK, leading=22)
    body_style = ParagraphStyle("body", fontName=normal, fontSize=10,
                                 spaceAfter=5, leading=15)
    meta_style = ParagraphStyle("meta", fontName=normal, fontSize=9,
                                 textColor=_GREY, spaceAfter=10, leading=13)
    copy_style = ParagraphStyle("copy", fontName=normal, fontSize=8,
                                 textColor=_GREY, alignment=TA_CENTER)

    story = []
    for line in md_text.split("\n"):
        line = line.rstrip()

        if not line:
            story.append(Spacer(1, 5))

        elif line.startswith("# "):
            story.append(Spacer(1, 4))
            story.append(Paragraph(_sanitize(line[2:], is_cjk), h1_style))

        elif line.startswith("## "):
            story.append(Spacer(1, 6))
            story.append(_section_header(_sanitize(line[3:], is_cjk), normal, bold))
            story.append(Spacer(1, 4))

        elif line.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5,
                                    color=_RULE, spaceBefore=8, spaceAfter=8))

        elif line.startswith("*") and line.endswith("*") and not line.startswith("**"):
            story.append(Paragraph(_sanitize(line.strip("*"), is_cjk), meta_style))

        elif re.match(r"^[-*]\s+", line):
            content = re.sub(r"^[-*]\s+", "", line)
            story.append(_bullet_para(_sanitize(content, is_cjk), normal))

        elif re.match(r"^\d+\.\s+", line):
            content = re.sub(r"^\d+\.\s+", "", line)
            story.append(_bullet_para(_sanitize(content, is_cjk), normal))

        elif line.startswith("©") or line.startswith("(c)"):
            story.append(Paragraph(_sanitize(line, is_cjk), copy_style))

        else:
            story.append(Paragraph(_sanitize(line, is_cjk), body_style))

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2.5 * cm, bottomMargin=2 * cm,
    )
    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    return buffer.getvalue()
