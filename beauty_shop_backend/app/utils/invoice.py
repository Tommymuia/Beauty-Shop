from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime
import os

def generate_invoice_pdf(invoice_number: str, amount: float, email: str, items: list):
    os.makedirs("invoices", exist_ok=True)
    
    file_name = f"invoice_{invoice_number}.pdf"
    file_path = os.path.join("invoices", file_name)
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    brand_color = colors.HexColor("#d63384") 

    # Header Bar
    c.setFillColor(brand_color)
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "BEAUTY SHOP LTD")
    
    # Body Info
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 120, "BILL TO:")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 135, f"{email}")
    c.drawRightString(width - 50, height - 120, datetime.now().strftime('%Y-%m-%d'))

    # Table Header
    c.setStrokeColor(brand_color)
    c.line(50, height - 160, width - 50, height - 160)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(60, height - 180, "Item Description")
    c.drawCentredString(width - 180, height - 180, "Qty")
    c.drawRightString(width - 60, height - 180, "Subtotal (KES)")
    c.line(50, height - 190, width - 50, height - 190)

    # DYNAMIC ITEMS LOOP
    c.setFont("Helvetica", 11)
    y_position = height - 215
    
    for item in items:
        if y_position < 100: # Simple page break check
            c.showPage()
            y_position = height - 50
            
        c.drawString(60, y_position, f"{item['name']}")
        c.drawCentredString(width - 180, y_position, f"{item['quantity']}")
        subtotal = item['price'] * item['quantity']
        c.drawRightString(width - 60, y_position, f"{subtotal:,.2f}")
        y_position -= 20

    # Grand Total Box
    total_y = y_position - 40
    c.setFillColor(colors.HexColor("#fdf2f8"))
    c.rect(width - 250, total_y - 15, 200, 40, fill=True, stroke=False)
    c.setFillColor(brand_color)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(width - 240, total_y, "GRAND TOTAL")
    c.drawRightString(width - 60, total_y, f"KES {amount:,.2f}")

    # Footer
    footer_y = 30
    c.setFillColor(brand_color)
    c.setFont("Helvetica", 9)
    c.drawString(50, footer_y + 10, "Thank you for shopping with Beauty Shop Ltd!")
    c.drawString(50, footer_y - 5, "If you have any questions, please contact muiathomas.mt@gmail.com")

    c.save()
    return file_path