from fastapi import APIRouter, FastAPI, HTTPException
from fpdf import FPDF


pdf= FPDF()
router= APIRouter(prefix='/pdf', tags=['pdf'])


@router.post('/')
def pdf(data:str):
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "Travel Plan", ln=True)
    pdf.ln(5)

    
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, data)

    pdf.ln(5)
    pdf.outputs("trip_planner.pdf")
    