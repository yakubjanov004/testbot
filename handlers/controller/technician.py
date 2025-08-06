"""
Controller Technician Management - Simplified Implementation

This module handles controller technician management functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.controller_buttons import get_technician_keyboard, get_controller_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_technicians():
    """Mock get technicians"""
    return [
        {
            'id': 1,
            'full_name': 'Aziz Karimov',
            'phone': '+998901234567',
            'email': 'aziz@example.com',
            'status': 'active',
            'specialization': 'Internet va TV',
            'experience': '3 yil',
            'rating': 4.5,
            'completed_orders': 45,
            'active_orders': 2,
            'created_at': datetime.now()
        },
        {
            'id': 2,
            'full_name': 'Malika Toshmatova',
            'phone': '+998901234568',
            'email': 'malika@example.com',
            'status': 'active',
            'specialization': 'Elektrik ishlar',
            'experience': '5 yil',
            'rating': 4.8,
            'completed_orders': 78,
            'active_orders': 1,
            'created_at': datetime.now()
        },
        {
            'id': 3,
            'full_name': 'Jahongir Azimov',
            'phone': '+998901234569',
            'email': 'jahongir@example.com',
            'status': 'inactive',
            'specialization': 'Kabel ishlari',
            'experience': '2 yil',
            'rating': 4.2,
            'completed_orders': 23,
            'active_orders': 0,
            'created_at': datetime.now()
        }
    ]

async def get_technician_performance(technician_id: int):
    """Mock get technician performance"""
    return {
        'total_orders': 45,
        'completed_orders': 42,
        'cancelled_orders': 3,
        'avg_rating': 4.5,
        'avg_completion_time': '2.3 soat',
        'customer_satisfaction': 92,
        'monthly_stats': {
            'january': 8,
            'february': 12,
            'march': 15,
            'april': 10
        }
    }

def get_technician_router():
    """Router for technician management functionality"""
    router = Router()

    @router.message(F.text.in_(["👨‍🔧 Texniklar boshqaruvi", "👨‍🔧 Управление техниками"]))
    async def view_technician_management(message: Message, state: FSMContext):
        """Controller view technician management handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            
            technician_text = (
                "👨‍🔧 <b>Texniklar boshqaruvi - To'liq ma'lumot</b>\n\n"
                "📋 <b>Mavjud texniklar:</b>\n"
                "• Internet va TV texniklari\n"
                "• Elektrik texniklari\n"
                "• Kabel texniklari\n"
                "• Umumiy texniklar\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "👨‍🔧 <b>Управление техниками - Полная информация</b>\n\n"
                "📋 <b>Существующие техники:</b>\n"
                "• Техники интернета и ТВ\n"
                "• Электрики\n"
                "• Кабельщики\n"
                "• Общие техники\n\n"
                "Выберите один из разделов ниже:"
            )
            
            sent_message = await message.answer(
                text=technician_text,
                reply_markup=get_technician_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_technicians")
    async def view_technicians(callback: CallbackQuery, state: FSMContext):
        """View technicians list"""
        try:
            await callback.answer()
            
            # Get technicians
            technicians = await get_technicians()
            
            if not technicians:
                no_technicians_text = (
                    "📭 Texniklar mavjud emas."
                    if callback.from_user.language_code == 'uz' else
                    "📭 Техники не найдены."
                )
                
                await callback.message.edit_text(
                    text=no_technicians_text,
                    reply_markup=get_controller_back_keyboard('uz')
                )
                return
            
            # Show first technician
            await show_technician_details(callback, technicians[0], technicians, 0)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    async def show_technician_details(callback, technician, technicians, index):
        """Show technician details with navigation"""
        try:
            # Format status
            status_emoji = {
                'active': '🟢',
                'inactive': '🔴',
                'busy': '🟡',
                'offline': '⚫'
            }.get(technician['status'], '⚪')
            
            status_text = {
                'active': 'Faol',
                'inactive': 'Faol emas',
                'busy': 'Band',
                'offline': 'Offline'
            }.get(technician['status'], 'Noma\'lum')
            
            # Format date
            created_date = technician['created_at'].strftime('%d.%m.%Y')
            
            # To'liq ma'lumot
            text = (
                f"👨‍🔧 <b>Texnik ma'lumotlari - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Texnik ID:</b> {technician['id']}\n"
                f"👤 <b>To'liq ism:</b> {technician['full_name']}\n"
                f"📞 <b>Telefon:</b> {technician['phone']}\n"
                f"📧 <b>Email:</b> {technician['email']}\n"
                f"🔧 <b>Ixtisoslik:</b> {technician['specialization']}\n"
                f"⏰ <b>Tajriba:</b> {technician['experience']}\n"
                f"⭐ <b>Reyting:</b> {technician['rating']}/5.0\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"📊 <b>Bajarilgan buyurtmalar:</b> {technician['completed_orders']}\n"
                f"📋 <b>Faol buyurtmalar:</b> {technician['active_orders']}\n"
                f"📅 <b>Qo'shilgan:</b> {created_date}\n\n"
                f"📊 <b>Texnik #{index + 1} / {len(technicians)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_technicians_navigation_keyboard(index, len(technicians))
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "technician_prev")
    async def show_previous_technician(callback: CallbackQuery, state: FSMContext):
        """Show previous technician"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_technician_index', 0)
            
            technicians = await get_technicians()
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_technician_index=new_index)
                await show_technician_details(callback, technicians[new_index], technicians, new_index)
            else:
                await callback.answer("Bu birinchi texnik")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "technician_next")
    async def show_next_technician(callback: CallbackQuery, state: FSMContext):
        """Show next technician"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_technician_index', 0)
            
            technicians = await get_technicians()
            
            if current_index < len(technicians) - 1:
                new_index = current_index + 1
                await state.update_data(current_technician_index=new_index)
                await show_technician_details(callback, technicians[new_index], technicians, new_index)
            else:
                await callback.answer("Bu oxirgi texnik")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "view_technician_performance")
    async def view_technician_performance(callback: CallbackQuery, state: FSMContext):
        """View technician performance"""
        try:
            await callback.answer()
            
            # Get current technician from state
            current_index = await state.get_data()
            current_index = current_index.get('current_technician_index', 0)
            
            technicians = await get_technicians()
            
            if current_index >= len(technicians):
                await callback.answer("Texnik topilmadi")
                return
            
            selected_technician = technicians[current_index]
            
            # Get performance data
            performance = await get_technician_performance(selected_technician['id'])
            
            performance_text = (
                f"📊 <b>Texnik samaradorligi - To'liq ma'lumot</b>\n\n"
                f"👤 <b>Texnik:</b> {selected_technician['full_name']}\n"
                f"📋 <b>Ixtisoslik:</b> {selected_technician['specialization']}\n\n"
                f"📈 <b>Umumiy ko'rsatkichlar:</b>\n"
                f"• Jami buyurtmalar: {performance['total_orders']}\n"
                f"• Bajarilgan: {performance['completed_orders']}\n"
                f"• Bekor qilingan: {performance['cancelled_orders']}\n"
                f"• O'rtacha reyting: {performance['avg_rating']}/5.0\n"
                f"• O'rtacha bajarish vaqti: {performance['avg_completion_time']}\n"
                f"• Mijoz mamnuniyati: {performance['customer_satisfaction']}%\n\n"
                f"📅 <b>Oylik statistika:</b>\n"
                f"• Yanvar: {performance['monthly_stats']['january']}\n"
                f"• Fevral: {performance['monthly_stats']['february']}\n"
                f"• Mart: {performance['monthly_stats']['march']}\n"
                f"• Aprel: {performance['monthly_stats']['april']}"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_technician")]
            ])
            
            await callback.message.edit_text(performance_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_technician")
    async def back_to_technician(callback: CallbackQuery, state: FSMContext):
        """Back to technician menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            technician_text = (
                "👨‍🔧 <b>Texniklar boshqaruvi - To'liq ma'lumot</b>\n\n"
                "📋 <b>Mavjud texniklar:</b>\n"
                "• Internet va TV texniklari\n"
                "• Elektrik texniklari\n"
                "• Kabel texniklari\n"
                "• Umumiy texniklar\n\n"
                "Quyidagi bo'limlardan birini tanlang:"
                if lang == 'uz' else
                "👨‍🔧 <b>Управление техниками - Полная информация</b>\n\n"
                "📋 <b>Существующие техники:</b>\n"
                "• Техники интернета и ТВ\n"
                "• Электрики\n"
                "• Кабельщики\n"
                "• Общие техники\n\n"
                "Выберите один из разделов ниже:"
            )
            
            await callback.message.edit_text(
                text=technician_text,
                reply_markup=get_technician_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router

def get_technicians_navigation_keyboard(current_index: int, total_technicians: int):
    """Create navigation keyboard for technicians"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="technician_prev"
        ))
    
    # Next button
    if current_index < total_technicians - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="technician_next"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Performance button
    keyboard.append([InlineKeyboardButton(text="📊 Samaradorlik", callback_data="view_technician_performance")])
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
