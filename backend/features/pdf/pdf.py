from fastapi import APIRouter, FastAPI, HTTPException
from fpdf import FPDF
from fastapi.responses import StreamingResponse
import io

router= APIRouter(prefix='/pdf', tags=['pdf'])



def pdf_generate(data:str):
    pdf= FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", "b", 18)
    pdf.cell(0, 10, "AI Generated Travel Plan", 0, 1, "C")
    pdf.ln(5)

    lines= data.split("/n")
    for line in lines:
                # headings
        if line.startswith("##"):
            pdf.set_font("Arial", "B", 14)
            pdf.ln(5)
            pdf.cell(0, 10, line.replace("##", ""), ln=True)

        # sub headings
        elif line.startswith("#"):
            pdf.set_font("Arial", "B", 12)
            pdf.ln(3)
            pdf.cell(0, 8, line.replace("#", ""), ln=True)

        else:  #normal text
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 8, line)
    
    pdf_output= pdf.output(dest="S").encode("latin-1")

    return io.BytesIO(pdf_output)

#dest="S" → do NOT save to a file, instead return the PDF as a string.

#.encode("latin-1") → converts that string into bytes (binary data).

@router.get('/')
def download_pdf():
    llm_output = """
# Sri Lanka Trip Plan

## Day 1 – Colombo
Visit Gangaramaya Temple
Walk around Galle Face Green
Try local street food

## Day 2 – Kandy
Visit Temple of the Tooth
Explore Kandy Lake
Watch cultural dance show

## Day 3 – Ella
Hike Little Adam's Peak
Visit Nine Arches Bridge
Enjoy tea plantations
"""
    pdf_file= pdf_generate(llm_output)
    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=trip_plan.pdf"
        }
    )

#"Content-Disposition" ->download the file
#StreamingResponse(...) ->This is a FastAPI response type that sends a file or data stream to the browser.
#BytesIO creates a file-like object in memory.