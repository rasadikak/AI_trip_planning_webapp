from fastapi import APIRouter, FastAPI, HTTPException
from fpdf import FPDF
from fastapi.responses import StreamingResponse
import io
import os
import requests

router= APIRouter(prefix='/pdf', tags=['pdf'])



def pdf_generate(data:str):
 
    pdf= FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', '', font_path, uni=True)
    font_path2 = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans-Bold.ttf')
    pdf.add_font('DejaVu', 'B', font_path2, uni=True)

    pdf.set_font('DejaVu', 'B', 18)
    pdf.cell(0, 10, "AI Generated Travel Plan", 0, 1, "C")
    pdf.ln(5)

    lines= data.split("\n")
    for line in lines:
        line = line.strip()  # remove extra spaces
        if not line:  # skip empty lines
            continue # headings
        if line.startswith("##"):
            pdf.set_font('DejaVu', "B", 14)
            pdf.ln(5)
            pdf.cell(pdf.epw, 10, line.replace("##", "").strip(), new_x="LMARGIN", new_y="NEXT")

        # sub headings
        elif line.startswith("#"):
            pdf.set_font('DejaVu', "B", 12)
            pdf.ln(3)
            pdf.cell(pdf.epw, 8, line.replace("#", "").strip(), new_x="LMARGIN", new_y="NEXT")

        else:  #normal text
            pdf.set_font('DejaVu', "", 11)
            pdf.multi_cell(pdf.epw, 8, line, new_x="LMARGIN", new_y="NEXT")
    
    pdf_output = pdf.output() 
    return io.BytesIO(pdf_output)
 
   
#dest="S" → do NOT save to a file, instead return the PDF as a string.

#.encode("utf-8") → converts that string into bytes (binary data).

@router.get('/')
def download_pdf():
    llm_output = requests.get("http://localhost:8000/planner_api/").text

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