import io
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

_CJK_FONTS = {
    "zh-cn": "STSong-Light",
    "zh-tw": "MSung-Light",
}


def _register_fonts(language: str) -> tuple[str, str]:
    cid = _CJK_FONTS.get(language)
    if cid:
        pdfmetrics.registerFont(UnicodeCIDFont(cid))
        return cid, cid
    return "Helvetica", "Helvetica-Bold"


def md_to_pdf(md_text: str, language: str = "en") -> bytes:
    normal, bold = _register_fonts(language)

    h1_style = ParagraphStyle("h1", fontName=bold, fontSize=16, spaceAfter=4,
                               textColor=colors.HexColor("#1a1a2e"))
    h2_style = ParagraphStyle("h2", fontName=bold, fontSize=12,
                               spaceBefore=12, spaceAfter=4,
                               textColor=colors.HexColor("#16213e"))
    body_style = ParagraphStyle("body", fontName=normal, fontSize=10,
                                spaceAfter=4, leading=15)
    meta_style = ParagraphStyle("meta", fontName=normal, fontSize=9,
                                textColor=colors.grey, spaceAfter=8)

    story = []
    for line in md_text.split("\n"):
        line = line.rstrip()
        if not line:
            story.append(Spacer(1, 4))
        elif line.startswith("# "):
            story.append(Paragraph(line[2:], h1_style))
            story.append(HRFlowable(width="100%", thickness=1.5,
                                    color=colors.HexColor("#2c5f8a"), spaceAfter=6))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], h2_style))
        elif line.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5,
                                    color=colors.lightgrey, spaceBefore=8, spaceAfter=8))
        elif line.startswith("*") and line.endswith("*") and not line.startswith("**"):
            story.append(Paragraph(line.strip("*"), meta_style))
        else:
            line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"\*(.*?)\*", r"<i>\1</i>", line)
            story.append(Paragraph(line, body_style))

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    doc.build(story)
    return buffer.getvalue()
