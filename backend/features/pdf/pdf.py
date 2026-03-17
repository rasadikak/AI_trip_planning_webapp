from fastapi import APIRouter
from fpdf import FPDF
from fastapi.responses import StreamingResponse
import io
import os
import re
from pydantic import BaseModel

class PDFRequest(BaseModel):
    text: str

router = APIRouter(prefix='/pdf', tags=['pdf'])

# Path check
emoji_font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoEmoji-Regular.ttf')
print("Emoji font path:", emoji_font_path)
print("Exists:", os.path.exists(emoji_font_path))

emoji_pattern = re.compile(
    "["
    u"\U0001F300-\U0001FFFF"
    u"\U00002700-\U000027BF"
    u"\U0001F900-\U0001F9FF"
    u"\U00002600-\U000026FF"
    "]+", flags=re.UNICODE
)

def write_mixed_line(pdf, line, base_font, base_style, base_size):
    segments = re.split(
        r'([\U0001F300-\U0001FFFF\U00002700-\U000027BF\U0001F900-\U0001F9FF\U00002600-\U000026FF]+)',
        line
    )
    for segment in segments:
        if not segment:
            continue
        if emoji_pattern.search(segment):
            pdf.set_font('NotoEmoji', '', base_size)
        else:
            pdf.set_font(base_font, base_style, base_size)
        pdf.write(8, segment)
    pdf.ln()

def pdf_generate(data: str):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', '', font_path, uni=True)

    font_path2 = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans-Bold.ttf')
    pdf.add_font('DejaVu', 'B', font_path2, uni=True)

    pdf.add_font('NotoEmoji', '', emoji_font_path, uni=True)

    # Title
    pdf.set_font('DejaVu', 'B', 18)
    pdf.cell(0, 10, "AI Generated Travel Plan", 0, 1, "C")
    pdf.ln(5)

    lines = data.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("##"):
            pdf.ln(5)
            write_mixed_line(pdf, line.replace("##", "").strip(), 'DejaVu', 'B', 14)
        elif line.startswith("#"):
            pdf.ln(3)
            write_mixed_line(pdf, line.replace("#", "").strip(), 'DejaVu', 'B', 12)
        else:
            write_mixed_line(pdf, line, 'DejaVu', '', 11)

    pdf_output = pdf.output()
    return io.BytesIO(pdf_output)


@router.post('/')
async def download_pdf(request: PDFRequest):
    print("api loaded")
    pdf_data = pdf_generate(request.text)
    return StreamingResponse(
        pdf_data,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=trip_plan.pdf"}
    )