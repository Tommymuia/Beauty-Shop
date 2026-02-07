from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Any

class PDFService:
    def __init__(self):  # FIXED
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#1f2937')
        )
    
    def generate_invoice(self, order_data: Dict[str, Any]) -> BytesIO:
        """Generate PDF invoice for an order"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch)
        
        story = []
        
        # Header
        story.append(Paragraph("Bloom Beauty", self.title_style))  # FIXED: P aragraph → Paragraph
        story.append(Paragraph("Invoice", self.styles['Heading2']))
        story.append(Spacer(1, 20))
        
        # Order details
        order_info = [
            ['Order ID:', order_data.get('id', 'N/A')],
            ['Date:', datetime.now().strftime('%Y-%m-%d')],  # FIXED: datet ime → datetime
            ['Status:', order_data.get('status', 'N/A')],
            ['Customer:', order_data.get('customer_name', 'N/A')],
            ['Email:', order_data.get('customer_email', 'N/A')]  # FIXED: order_data. get → order_data.get
        ]
        
        order_table = Table(order_info, colWidths=[2*inch, 3*inch])
        order_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # FIXED
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(order_table)  # FIXED: story. append → story.append
        story.append(Spacer(1, 30))
        
        # Items table
        story.append(Paragraph("Order Items", self.styles['Heading3']))
        story.append(Spacer(1, 10))
        
        items_data = [['Product', 'Quantity', 'Unit Price', 'Total']]
        
        for item in order_data.get('items', []):  # FIXED: for  item → for item
            items_data.append([
                item.get('name', 'N/A'),
                str(item.get('quantity', 0)),
                f"Kshs. {item.get('price', 0):,.2f}",  # FIXED
                f"Kshs. {item.get('total_price', 0):,.2f}"
            ])
        
        items_data.append(['', '', 'Total:', f"Kshs. {order_data.get('total_amount', 0):,.2f}"])
        
        items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # FIXED: colors.gr ey → colors.grey
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # FIXED: FO NTSIZE → FONTSIZE
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # FIXED
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 30))  # FIXED: stor y → story
        
        story.append(Paragraph("Thank you for your business!", self.styles['Normal']))
        story.append(Paragraph("Bloom Beauty - Your trusted beauty partner", self.styles['Italic']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_order_report(self, orders_data: List[Dict[str, Any]]) -> BytesIO:
        """Generate PDF report for multiple orders"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch)
        
        story = []
        
        story.append(Paragraph("Bloom Beauty", self.title_style))
        story.append(Paragraph("Orders Report", self.styles['Heading2']))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", self.styles['Normal']))
        story.append(Spacer(1, 30))
        
        total_orders = len(orders_data)
        total_revenue = sum(order.get('total_amount', 0) for order in orders_data)  # FIXED
        
        summary_data = [
            ['Total Orders:', str(total_orders)],
            ['Total Revenue:', f"Kshs. {total_revenue:,.2f}"],
            ['Average Order Value:', f"Kshs. {total_revenue/total_orders if total_orders > 0 else 0:,.2f}"]  # FIXED
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),  # FIXED: FON TNAME → FONTNAME
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 30))
        
        story.append(Paragraph("Order Details", self.styles['Heading3']))
        story.append(Spacer(1, 10))
        
        orders_table_data = [['Order ID', 'Customer', 'Date', 'Status', 'Amount']]
        
        for order in orders_data:
            orders_table_data.append([
                order.get('id', 'N/A'),
                order.get('customer_name', 'N/A'),
                order.get('date', 'N/A'),
                order.get('status', 'N/A'),  # FIXED: s tatus → status
                f"Kshs. {order.get('total_amount', 0):,.2f}"
            ])
        
        orders_table = Table(orders_table_data, colWidths=[1.2*inch, 2*inch, 1.5*inch, 1*inch, 1.3*inch])
        orders_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # FIXED
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # FIXED: He lvetica-Bold → Helvetica-Bold
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  # FIXED
        ]))
        
        story.append(orders_table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer

pdf_service = PDFService()