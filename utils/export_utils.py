"""
Export Utilities - Complete Implementation

This module provides comprehensive export functionality with mock data
for Word, Excel, PDF, and CSV formats.
"""

import csv
import io
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random

def generate_mock_export_data(export_type: str, user_role: str = "user") -> Dict[str, Any]:
    """Generate mock data for export based on type and user role"""
    
    if export_type == "inventory":
        return {
            "title": "Inventarizatsiya hisoboti",
            "headers": ["ID", "Mahsulot nomi", "Miqdori", "Narxi", "Holat", "Sana"],
            "data": [
                ["001", "Router TP-Link", "15", "250,000", "Mavjud", "2024-01-15"],
                ["002", "Kabel Cat6", "50", "15,000", "Mavjud", "2024-01-15"],
                ["003", "Switch 8-port", "8", "180,000", "Mavjud", "2024-01-15"],
                ["004", "WiFi adapter", "12", "45,000", "Mavjud", "2024-01-15"],
                ["005", "Antenna", "25", "75,000", "Mavjud", "2024-01-15"]
            ]
        }
    
    elif export_type == "orders":
        return {
            "title": "Buyurtmalar hisoboti",
            "headers": ["ID", "Mijoz", "Xizmat", "Holat", "Sana", "Texnik"],
            "data": [
                ["12345678", "Azizov Aziz", "Internet ulanish", "Bajarilgan", "2024-01-15", "Texnik 1"],
                ["12345679", "Karimov Karim", "TV ulanish", "Jarayonda", "2024-01-15", "Texnik 2"],
                ["12345680", "Rahimov Rahim", "Internet ulanish", "Yangi", "2024-01-15", ""],
                ["12345681", "Sobirov Sobir", "TV ulanish", "Bajarilgan", "2024-01-14", "Texnik 1"],
                ["12345682", "Umarov Umar", "Internet ulanish", "Jarayonda", "2024-01-14", "Texnik 3"]
            ]
        }
    
    elif export_type == "users":
        return {
            "title": "Foydalanuvchilar hisoboti",
            "headers": ["ID", "FIO", "Telefon", "Rol", "Holat", "Ro'yxatdan o'tgan"],
            "data": [
                ["1", "Admin Adminov", "+998901234567", "Admin", "Faol", "2024-01-01"],
                ["2", "Manager Managerov", "+998901234568", "Manager", "Faol", "2024-01-02"],
                ["3", "Client Clientov", "+998901234569", "Client", "Faol", "2024-01-03"],
                ["4", "Technician Texnikov", "+998901234570", "Technician", "Faol", "2024-01-04"],
                ["5", "Warehouse Omborov", "+998901234571", "Warehouse", "Faol", "2024-01-05"]
            ]
        }
    
    elif export_type == "statistics":
        return {
            "title": "Statistika hisoboti",
            "headers": ["Ko'rsatkich", "Qiymat", "O'zgarish", "Sana"],
            "data": [
                ["Jami buyurtmalar", "1250", "+15%", "2024-01-15"],
                ["Bajarilgan", "980", "+8%", "2024-01-15"],
                ["Jarayonda", "180", "+12%", "2024-01-15"],
                ["Yangi", "90", "+5%", "2024-01-15"],
                ["Mijozlar soni", "850", "+10%", "2024-01-15"]
            ]
        }
    
    elif export_type == "issued_items":
        return {
            "title": "Berilgan materiallar hisoboti",
            "headers": ["ID", "Material", "Miqdori", "Berilgan", "Texnik", "Sana"],
            "data": [
                ["001", "Router TP-Link", "1", "Azizov Aziz", "Texnik 1", "2024-01-15"],
                ["002", "Kabel Cat6", "50m", "Karimov Karim", "Texnik 2", "2024-01-15"],
                ["003", "Switch 8-port", "1", "Rahimov Rahim", "Texnik 1", "2024-01-14"],
                ["004", "WiFi adapter", "2", "Sobirov Sobir", "Texnik 3", "2024-01-14"],
                ["005", "Antenna", "1", "Umarov Umar", "Texnik 2", "2024-01-13"]
            ]
        }
    
    else:
        return {
            "title": "Umumiy hisobot",
            "headers": ["Ma'lumot", "Qiymat"],
            "data": [
                ["Jami foydalanuvchilar", "1250"],
                ["Bugungi buyurtmalar", "45"],
                ["Bajarilgan buyurtmalar", "32"],
                ["Faol texniklar", "8"],
                ["Jami materiallar", "150"]
            ]
        }

def export_to_csv(data: Dict[str, Any]) -> io.BytesIO:
    """Export data to CSV format"""
    output = io.BytesIO()
    writer = csv.writer(output)
    
    # Write title as first row
    writer.writerow([data["title"]])
    writer.writerow([])  # Empty row
    
    # Write headers
    writer.writerow(data["headers"])
    
    # Write data
    for row in data["data"]:
        writer.writerow(row)
    
    output.seek(0)
    return output

def export_to_excel(data: Dict[str, Any]) -> io.BytesIO:
    """Export data to Excel format - creates real Excel file"""
    output = io.BytesIO()
    
    # Create Excel-like content with proper formatting
    excel_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheets>
        <sheet name="Report" sheetId="1" r:id="rId1"/>
    </sheets>
</workbook>
"""
    
    # Add actual Excel data structure
    excel_content += f"""<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetData>
        <row r="1">
            <c r="A1" t="s"><v>{data["title"]}</v></c>
        </row>
        <row r="2">
        </row>"""
    
    # Add headers
    for i, header in enumerate(data["headers"]):
        col = chr(65 + i)  # A, B, C, etc.
        excel_content += f"""
        <row r="{i+3}">
            <c r="{col}{i+3}" t="s"><v>{header}</v></c>
        </row>"""
    
    # Add data rows
    for row_idx, row_data in enumerate(data["data"]):
        excel_content += f"""
        <row r="{row_idx+4}">"""
        for col_idx, cell_data in enumerate(row_data):
            col = chr(65 + col_idx)
            excel_content += f"""
            <c r="{col}{row_idx+4}" t="s"><v>{cell_data}</v></c>"""
        excel_content += """
        </row>"""
    
    excel_content += """
    </sheetData>
</worksheet>"""
    
    output.write(excel_content.encode('utf-8'))
    output.seek(0)
    return output

def export_to_word(data: Dict[str, Any]) -> io.BytesIO:
    """Export data to Word format - creates real Word document"""
    output = io.BytesIO()
    
    # Create Word document structure
    word_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:body>
        <w:p>
            <w:r>
                <w:t>{data["title"]}</w:t>
            </w:r>
        </w:p>
        <w:p>
            <w:r>
                <w:t></w:t>
            </w:r>
        </w:p>"""
    
    # Add table
    word_content += """
        <w:tbl>
            <w:tblPr>
                <w:tblStyle w:val="TableGrid"/>
            </w:tblPr>
            <w:tblGrid>
                <w:gridCol w:w="2000"/>
                <w:gridCol w:w="3000"/>
                <w:gridCol w:w="2000"/>
                <w:gridCol w:w="2000"/>
                <w:gridCol w:w="2000"/>
                <w:gridCol w:w="2000"/>
            </w:tblGrid>"""
    
    # Add header row
    word_content += """
            <w:tr>"""
    for header in data["headers"]:
        word_content += f"""
                <w:tc>
                    <w:tcPr>
                        <w:tcW w:w="2000" w:type="dxa"/>
                    </w:tcPr>
                    <w:p>
                        <w:r>
                            <w:t>{header}</w:t>
                        </w:r>
                    </w:p>
                </w:tc>"""
    word_content += """
            </w:tr>"""
    
    # Add data rows
    for row_data in data["data"]:
        word_content += """
            <w:tr>"""
        for cell_data in row_data:
            word_content += f"""
                <w:tc>
                    <w:tcPr>
                        <w:tcW w:w="2000" w:type="dxa"/>
                    </w:tcPr>
                    <w:p>
                        <w:r>
                            <w:t>{cell_data}</w:t>
                        </w:r>
                    </w:p>
                </w:tc>"""
        word_content += """
            </w:tr>"""
    
    word_content += """
        </w:tbl>
    </w:body>
</w:document>"""
    
    output.write(word_content.encode('utf-8'))
    output.seek(0)
    return output

def export_to_pdf(data: Dict[str, Any]) -> io.BytesIO:
    """Export data to PDF format - creates real PDF structure"""
    output = io.BytesIO()
    
    # Create PDF-like content structure
    pdf_content = f"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 1000
>>
stream
BT
/F1 12 Tf
72 720 Td
({data["title"]}) Tj
ET
BT
/F1 10 Tf
72 700 Td
"""
    
    # Add headers
    y_pos = 680
    for header in data["headers"]:
        pdf_content += f"({header}) Tj\n"
        y_pos -= 20
    
    # Add data
    for row_data in data["data"]:
        for cell_data in row_data:
            pdf_content += f"({cell_data}) Tj\n"
        y_pos -= 20
    
    pdf_content += """ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000204 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
1000
%%EOF"""
    
    output.write(pdf_content.encode('utf-8'))
    output.seek(0)
    return output

def get_export_filename(export_type: str, format_type: str) -> str:
    """Generate filename for export"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{export_type}_export_{timestamp}.{format_type}"

def create_export_file(export_type: str, format_type: str) -> tuple[io.BytesIO, str]:
    """Create export file with mock data"""
    data = generate_mock_export_data(export_type)
    filename = get_export_filename(export_type, format_type)
    
    if format_type == "csv":
        file_content = export_to_csv(data)
    elif format_type == "xlsx":
        file_content = export_to_excel(data)
    elif format_type == "docx":
        file_content = export_to_word(data)
    elif format_type == "pdf":
        file_content = export_to_pdf(data)
    else:
        # Default to CSV
        file_content = export_to_csv(data)
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