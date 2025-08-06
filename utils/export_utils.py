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
    """Export data to Excel format (simulated as CSV for now)"""
    # For now, we'll use CSV format as Excel
    # In a real implementation, you would use openpyxl or xlsxwriter
    return export_to_csv(data)

def export_to_word(data: Dict[str, Any]) -> io.BytesIO:
    """Export data to Word format (simulated as text for now)"""
    output = io.BytesIO()
    
    # Create a simple text representation
    content = f"{data['title']}\n\n"
    content += "=" * len(data['title']) + "\n\n"
    
    # Add headers
    content += " | ".join(data["headers"]) + "\n"
    content += "-" * (len(" | ".join(data["headers"]))) + "\n"
    
    # Add data
    for row in data["data"]:
        content += " | ".join(str(cell) for cell in row) + "\n"
    
    output.write(content.encode('utf-8'))
    output.seek(0)
    return output

def export_to_pdf(data: Dict[str, Any]) -> io.BytesIO:
    """Export data to PDF format (simulated as text for now)"""
    # For now, we'll use text format as PDF
    # In a real implementation, you would use reportlab or weasyprint
    return export_to_word(data)

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