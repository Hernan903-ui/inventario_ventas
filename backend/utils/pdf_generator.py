from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
import matplotlib.pyplot as plt
import logging
from datetime import datetime  # Corrección 1: Importar datetime
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)

def generate_pdf_report(title, headers, data, charts=False):
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph(f"<b>{title}</b>", styles['Title']))
        elements.append(Paragraph(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))

        table_data = [headers] + data
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.grey)
        ]))
        elements.append(table)

        if charts:
            img_buffer = BytesIO()
            generate_chart_image(data, img_buffer)  # Corrección 2: Remover self.
            elements.append(Image(img_buffer, width=400, height=300))

        doc.build(elements)
        return buffer.getvalue()

    except Exception as e:
        logger.error(f"Error generando PDF: {str(e)}")
        raise

def generate_chart_image(data, output_buffer):
    try:
        products = [item[0] for item in data]
        sales = [item[1] for item in data]

        plt.figure(figsize=(10, 6))
        plt.bar(products, sales, color='skyblue')
        plt.title('Productos más vendidos')
        plt.xlabel('Productos')
        plt.ylabel('Ventas')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_buffer, format='png')
        plt.close()
        
    except Exception as e:
        logger.error(f"Error generando gráfico: {str(e)}")
        raise



def generate_pdf(filename, data):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, "Reporte de Ventas")
    y = height - 150
    for item in data:
        c.drawString(100, y, f"Producto: {item['name']}, Cantidad: {item['quantity']}, Total: ${item['total']}")
        y -= 20
    c.save()