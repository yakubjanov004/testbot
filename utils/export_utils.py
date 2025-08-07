"""
Export Utilities - Real Export Implementation with Proper Libraries

This module provides comprehensive export functionality using:
- openpyxl for Excel files
- python-docx for Word documents
- reportlab for PDF files
- csv for CSV files
"""

import csv
import io
from datetime import datetime
from typing import Dict, List, Any, Tuple
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Import our warehouse data generator
from utils.warehouse_data import (
    generate_inventory_data,
    generate_issued_items_data,
    generate_orders_data,
    generate_statistics_data,
    get_export_headers
)

def format_number(value: Any) -> str:
    """Format numbers with thousand separators"""
    if isinstance(value, (int, float)):
        return f"{value:,}".replace(",", " ")
    return str(value)

def export_to_csv(export_type: str) -> io.BytesIO:
    """Export data to CSV format"""
    output = io.BytesIO()
    wrapper = io.TextIOWrapper(output, encoding='utf-8-sig', newline='')
    writer = csv.writer(wrapper)
    
    # Get data based on export type
    if export_type == "inventory":
        data = generate_inventory_data()
        headers = get_export_headers("inventory")
        title = "Ombor inventarizatsiya hisoboti"
    elif export_type == "issued_items":
        data = generate_issued_items_data()
        headers = get_export_headers("issued_items")
        title = "Berilgan materiallar hisoboti"
    elif export_type == "orders":
        data = generate_orders_data()
        headers = get_export_headers("orders")
        title = "Buyurtmalar hisoboti"
    else:  # statistics
        stats = generate_statistics_data()
        headers = get_export_headers("statistics")
        title = "Ombor statistika hisoboti"
        data = []
        # Convert statistics to table format
        for key, value in stats["general_stats"].items():
            data.append([
                key.replace("_", " ").title(),
                format_number(value),
                "+15%",
                "Oxirgi 30 kun ichida"
            ])
    
    # Write title and date
    writer.writerow([title])
    writer.writerow([f"Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}"])
    writer.writerow([])  # Empty row
    
    # Write headers
    writer.writerow(headers)
    
    # Write data
    if export_type == "inventory":
        for item in data:
            writer.writerow([
                item["id"], item["name"], item["category"], item["unit"],
                item["initial_quantity"], item["current_quantity"], item["reserved_quantity"],
                format_number(item["unit_price"]), format_number(item["total_value"]),
                item["min_stock"], item["location"], item["last_updated"], item["status"]
            ])
    elif export_type == "issued_items":
        for item in data:
            writer.writerow([
                item["id"], item["order_id"], item["item_name"], item["category"],
                item["quantity"], format_number(item["unit_price"]), format_number(item["total_price"]),
                item["technician"], item["client_name"], item["client_address"],
                item["service_type"], item["issued_date"], item["issued_time"],
                item["return_status"], item["notes"]
            ])
    elif export_type == "orders":
        for order in data:
            writer.writerow([
                order["id"], order["client_name"], order["phone"], order["address"],
                order["service_type"], order["status"], order["priority"],
                order["created_date"], order["created_time"], order["scheduled_date"],
                order["scheduled_time"], order["technician"], order["completion_date"],
                order["materials_used"], format_number(order["total_cost"]),
                order["payment_status"], order["notes"]
            ])
    else:  # statistics
        for row in data:
            writer.writerow(row)
    
    wrapper.flush()
    wrapper.detach()
    output.seek(0)
    return output

def export_to_excel(export_type: str) -> io.BytesIO:
    """Export data to Excel format using openpyxl"""
    wb = Workbook()
    ws = wb.active
    
    # Get data based on export type
    if export_type == "inventory":
        data = generate_inventory_data()
        headers = get_export_headers("inventory")
        ws.title = "Inventarizatsiya"
        title = "Ombor inventarizatsiya hisoboti"
    elif export_type == "issued_items":
        data = generate_issued_items_data()
        headers = get_export_headers("issued_items")
        ws.title = "Berilgan materiallar"
        title = "Berilgan materiallar hisoboti"
    elif export_type == "orders":
        data = generate_orders_data()
        headers = get_export_headers("orders")
        ws.title = "Buyurtmalar"
        title = "Buyurtmalar hisoboti"
    else:  # statistics
        stats = generate_statistics_data()
        headers = get_export_headers("statistics")
        ws.title = "Statistika"
        title = "Ombor statistika hisoboti"
        data = []
        for key, value in stats["general_stats"].items():
            data.append({
                "metric": key.replace("_", " ").title(),
                "value": format_number(value),
                "change": "+15%",
                "description": "Oxirgi 30 kun ichida"
            })
    
    # Style definitions
    title_font = Font(name='Arial', size=16, bold=True)
    header_font = Font(name='Arial', size=12, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Add title
    ws.merge_cells(f'A1:{get_column_letter(len(headers))}1')
    ws['A1'] = title
    ws['A1'].font = title_font
    ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
    
    # Add date
    ws.merge_cells(f'A2:{get_column_letter(len(headers))}2')
    ws['A2'] = f"Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    ws['A2'].alignment = Alignment(horizontal="center", vertical="center")
    
    # Add headers
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border
    
    # Add data
    row_idx = 5
    if export_type == "inventory":
        for item in data:
            ws.append([
                item["id"], item["name"], item["category"], item["unit"],
                item["initial_quantity"], item["current_quantity"], item["reserved_quantity"],
                item["unit_price"], item["total_value"], item["min_stock"],
                item["location"], item["last_updated"], item["status"]
            ])
            # Apply borders to the last row
            for col_idx in range(1, len(headers) + 1):
                ws.cell(row=row_idx, column=col_idx).border = border
            row_idx += 1
    elif export_type == "issued_items":
        for item in data:
            ws.append([
                item["id"], item["order_id"], item["item_name"], item["category"],
                item["quantity"], item["unit_price"], item["total_price"],
                item["technician"], item["client_name"], item["client_address"],
                item["service_type"], item["issued_date"], item["issued_time"],
                item["return_status"], item["notes"]
            ])
            for col_idx in range(1, len(headers) + 1):
                ws.cell(row=row_idx, column=col_idx).border = border
            row_idx += 1
    elif export_type == "orders":
        for order in data:
            ws.append([
                order["id"], order["client_name"], order["phone"], order["address"],
                order["service_type"], order["status"], order["priority"],
                order["created_date"], order["created_time"], order["scheduled_date"],
                order["scheduled_time"], order["technician"], order["completion_date"],
                order["materials_used"], order["total_cost"],
                order["payment_status"], order["notes"]
            ])
            for col_idx in range(1, len(headers) + 1):
                ws.cell(row=row_idx, column=col_idx).border = border
            row_idx += 1
    else:  # statistics
        for item in data:
            ws.append([
                item["metric"], item["value"], item["change"], item["description"]
            ])
            for col_idx in range(1, len(headers) + 1):
                ws.cell(row=row_idx, column=col_idx).border = border
            row_idx += 1
    
    # Auto-adjust column widths
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Save to BytesIO
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output

def export_to_word(export_type: str) -> io.BytesIO:
    """Export data to Word format using python-docx"""
    doc = Document()
    
    # Get data based on export type
    if export_type == "inventory":
        data = generate_inventory_data()
        headers = get_export_headers("inventory")
        title = "Ombor inventarizatsiya hisoboti"
    elif export_type == "issued_items":
        data = generate_issued_items_data()
        headers = get_export_headers("issued_items")
        title = "Berilgan materiallar hisoboti"
    elif export_type == "orders":
        data = generate_orders_data()
        headers = get_export_headers("orders")
        title = "Buyurtmalar hisoboti"
    else:  # statistics
        stats = generate_statistics_data()
        headers = get_export_headers("statistics")
        title = "Ombor statistika hisoboti"
        data = []
        for key, value in stats["general_stats"].items():
            data.append({
                "metric": key.replace("_", " ").title(),
                "value": format_number(value),
                "change": "+15%",
                "description": "Oxirgi 30 kun ichida"
            })
    
    # Add title
    title_para = doc.add_paragraph()
    title_run = title_para.add_run(title)
    title_run.font.size = Pt(18)
    title_run.font.bold = True
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add date
    date_para = doc.add_paragraph()
    date_run = date_para.add_run(f"Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    date_run.font.size = Pt(12)
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()  # Empty line
    
    # Create table
    if export_type in ["inventory", "issued_items", "orders"]:
        # For large datasets, create a simplified table
        table = doc.add_table(rows=1, cols=len(headers))
        table.style = 'Light Grid Accent 1'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Add headers
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            hdr_cells[i].text = header
            # Make header bold
            for paragraph in hdr_cells[i].paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
        
        # Add data (limit to first 20 rows for Word document)
        data_to_show = data[:20]
        
        if export_type == "inventory":
            for item in data_to_show:
                row_cells = table.add_row().cells
                values = [
                    item["id"], item["name"], item["category"], item["unit"],
                    str(item["initial_quantity"]), str(item["current_quantity"]), 
                    str(item["reserved_quantity"]), format_number(item["unit_price"]), 
                    format_number(item["total_value"]), str(item["min_stock"]),
                    item["location"], item["last_updated"], item["status"]
                ]
                for i, value in enumerate(values):
                    row_cells[i].text = value
        elif export_type == "issued_items":
            for item in data_to_show:
                row_cells = table.add_row().cells
                values = [
                    item["id"], item["order_id"], item["item_name"], item["category"],
                    item["quantity"], format_number(item["unit_price"]), 
                    format_number(item["total_price"]), item["technician"], 
                    item["client_name"], item["client_address"], item["service_type"], 
                    item["issued_date"], item["issued_time"], item["return_status"], 
                    item["notes"]
                ]
                for i, value in enumerate(values):
                    row_cells[i].text = value
        elif export_type == "orders":
            for order in data_to_show:
                row_cells = table.add_row().cells
                values = [
                    order["id"], order["client_name"], order["phone"], order["address"],
                    order["service_type"], order["status"], order["priority"],
                    order["created_date"], order["created_time"], order["scheduled_date"],
                    order["scheduled_time"], order["technician"], order["completion_date"],
                    order["materials_used"], format_number(order["total_cost"]),
                    order["payment_status"], order["notes"]
                ]
                for i, value in enumerate(values):
                    row_cells[i].text = value
    else:  # statistics
        table = doc.add_table(rows=1, cols=len(headers))
        table.style = 'Light Grid Accent 1'
        
        # Add headers
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            hdr_cells[i].text = header
            for paragraph in hdr_cells[i].paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
        
        # Add data
        for item in data:
            row_cells = table.add_row().cells
            row_cells[0].text = item["metric"]
            row_cells[1].text = item["value"]
            row_cells[2].text = item["change"]
            row_cells[3].text = item["description"]
    
    # Add note if data was truncated
    if export_type in ["inventory", "issued_items", "orders"] and len(data) > 20:
        note_para = doc.add_paragraph()
        note_para.add_run(f"\nIzoh: Jami {len(data)} ta yozuvdan 20 tasi ko'rsatildi.")
        note_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Save to BytesIO
    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return output

def export_to_pdf(export_type: str) -> io.BytesIO:
    """Export data to PDF format using reportlab"""
    output = io.BytesIO()
    
    # Get data based on export type
    if export_type == "inventory":
        data = generate_inventory_data()
        headers = get_export_headers("inventory")
        title = "Ombor inventarizatsiya hisoboti"
        page_size = landscape(A4)
    elif export_type == "issued_items":
        data = generate_issued_items_data()
        headers = get_export_headers("issued_items")
        title = "Berilgan materiallar hisoboti"
        page_size = landscape(A4)
    elif export_type == "orders":
        data = generate_orders_data()
        headers = get_export_headers("orders")
        title = "Buyurtmalar hisoboti"
        page_size = landscape(A4)
    else:  # statistics
        stats = generate_statistics_data()
        headers = get_export_headers("statistics")
        title = "Ombor statistika hisoboti"
        page_size = A4
        data = []
        for key, value in stats["general_stats"].items():
            data.append([
                key.replace("_", " ").title(),
                format_number(value),
                "+15%",
                "Oxirgi 30 kun ichida"
            ])
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output,
        pagesize=page_size,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Add title
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(f"Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.5 * inch))
    
    # Prepare table data
    table_data = [headers]
    
    if export_type == "inventory":
        for item in data[:30]:  # Limit to 30 rows for PDF
            table_data.append([
                item["id"], item["name"][:20], item["category"], item["unit"],
                str(item["initial_quantity"]), str(item["current_quantity"]), 
                str(item["reserved_quantity"]), format_number(item["unit_price"]), 
                format_number(item["total_value"]), str(item["min_stock"]),
                item["location"], item["last_updated"], item["status"]
            ])
    elif export_type == "issued_items":
        for item in data[:30]:
            table_data.append([
                item["id"], item["order_id"], item["item_name"][:20], item["category"],
                item["quantity"], format_number(item["unit_price"]), 
                format_number(item["total_price"]), item["technician"], 
                item["client_name"][:15], item["client_address"][:20], 
                item["service_type"][:15], item["issued_date"], item["issued_time"],
                item["return_status"], item["notes"][:10]
            ])
    elif export_type == "orders":
        for order in data[:30]:
            table_data.append([
                order["id"], order["client_name"][:15], order["phone"], 
                order["address"][:20], order["service_type"][:15], order["status"], 
                order["priority"], order["created_date"], order["created_time"], 
                order["scheduled_date"], order["scheduled_time"], order["technician"], 
                order["completion_date"], order["materials_used"][:15], 
                format_number(order["total_cost"]), order["payment_status"], 
                order["notes"][:10]
            ])
    else:  # statistics
        table_data.extend(data)
    
    # Create table
    t = Table(table_data)
    
    # Add style to table
    table_style = TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # Data style
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # Alternate row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ])
    
    t.setStyle(table_style)
    elements.append(t)
    
    # Add note if data was truncated
    if len(data) > 30:
        elements.append(Spacer(1, 0.2 * inch))
        note = Paragraph(
            f"Izoh: Jami {len(data)} ta yozuvdan 30 tasi ko'rsatildi.",
            styles['Normal']
        )
        elements.append(note)
    
    # Build PDF
    doc.build(elements)
    output.seek(0)
    return output

def get_export_filename(export_type: str, format_type: str) -> str:
    """Generate filename for export"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    type_names = {
        "inventory": "inventarizatsiya",
        "issued_items": "berilgan_materiallar",
        "orders": "buyurtmalar",
        "statistics": "statistika"
    }
    export_name = type_names.get(export_type, export_type)
    return f"ombor_{export_name}_{timestamp}.{format_type}"

def create_export_file(export_type: str, format_type: str) -> Tuple[io.BytesIO, str]:
    """Create export file with real data using appropriate libraries"""
    filename = get_export_filename(export_type, format_type)
    
    if format_type == "csv":
        file_content = export_to_csv(export_type)
    elif format_type == "xlsx":
        file_content = export_to_excel(export_type)
    elif format_type == "docx":
        file_content = export_to_word(export_type)
    elif format_type == "pdf":
        file_content = export_to_pdf(export_type)
    else:
        # Default to CSV
        file_content = export_to_csv(export_type)
        filename = filename.replace(f".{format_type}", ".csv")
    
    return file_content, filename

def get_available_export_types(user_role: str) -> List[str]:
    """Get available export types based on user role"""
    if user_role == "warehouse":
        return ["inventory", "issued_items", "orders", "statistics"]
    elif user_role == "admin":
        return ["users", "orders", "statistics", "inventory"]
    elif user_role == "manager":
        return ["orders", "statistics", "users"]
    elif user_role == "call_center_supervisor":
        return ["orders", "statistics", "users"]
    else:
        return ["orders", "statistics"]

def get_available_export_formats() -> List[str]:
    """Get available export formats"""
    return ["csv", "xlsx", "docx", "pdf"]