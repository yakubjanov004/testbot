"""
Controller Technician Management Handler
Manages technician management for controller
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_technician_keyboard, get_controller_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime
from handlers.technician import get_technician_router
from filters.role_filter import RoleFilter

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

async def get_user_lang(user_id: int):
    """Mock get user language"""
    return 'uz'

async def get_technicians():
    """Mock get technicians"""
    return [
        {
            'id': 1,
            'full_name': 'Aziz Karimov',
            'role': 'technician',
            'status': 'active',
            'phone': '+998901234567',
            'email': 'aziz@example.com',
            'specialization': 'Internet xizmati',
            'active_orders': 3,
            'completed_today': 2,
            'avg_rating': 4.8,
            'experience_years': 3
        },
        {
            'id': 2,
            'full_name': 'Malika Yusupova',
            'role': 'technician',
            'status': 'active',
            'phone': '+998901234568',
            'email': 'malika@example.com',
            'specialization': 'TV xizmati',
            'active_orders': 1,
            'completed_today': 3,
            'avg_rating': 4.6,
            'experience_years': 2
        },
        {
            'id': 3,
            'full_name': 'Bekzod Toirov',
            'role': 'technician',
            'status': 'inactive',
            'phone': '+998901234569',
            'email': 'bekzod@example.com',
            'specialization': 'Texnik xizmat',
            'active_orders': 0,
            'completed_today': 1,
            'avg_rating': 4.4,
            'experience_years': 1
        }
    ]

async def get_technician_performance(technician_id: int):
    """Mock get technician performance"""
    return {
        'total_orders': 45,
        'completed_orders': 42,
        'active_orders': 3,
        'avg_completion_time': '2.1 soat',
        'customer_satisfaction': 4.7,
        'response_time': '15 daqiqa',
        'success_rate': 93,
        'monthly_performance': {
            'january': 85,
            'february': 88,
            'march': 92,
            'april': 90
        }
    }

def get_controller_technician_management_router():
    """Get controller technician management router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["👨‍🔧 Texniklar boshqaruvi", "👨‍🔧 Управление техниками"]))
    async def view_technician_management(message: Message, state: FSMContext):
        """Handle technician management view"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            technicians = await get_technicians()
            
            if not technicians:
                no_technicians_text = "👨‍🔧 Hozircha texniklar mavjud emas."
                await message.answer(no_technicians_text)
                return
            
            # Calculate statistics
            total_technicians = len(technicians)
            active_technicians = len([t for t in technicians if t['status'] == 'active'])
            total_active_orders = sum(t['active_orders'] for t in technicians)
            total_completed_today = sum(t['completed_today'] for t in technicians)
            
            management_text = (
                "👨‍🔧 <b>Texniklar boshqaruvi</b>\n\n"
                "📊 <b>Umumiy statistika:</b>\n"
                f"• Jami texniklar: {total_technicians}\n"
                f"• Faol texniklar: {active_technicians}\n"
                f"• Faol buyurtmalar: {total_active_orders}\n"
                f"• Bugun bajarilgan: {total_completed_today}\n\n"
                "Kerakli bo'limni tanlang:"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="👥 Texniklarni ko'rish", callback_data="view_technicians"),
                    InlineKeyboardButton(text="📊 Faoliyat baholash", callback_data="view_technician_performance")
                ],
                [
                    InlineKeyboardButton(text="➕ Yangi texnik", callback_data="add_technician"),
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_technician")
                ]
            ])
            
            await message.answer(
                management_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in view_technician_management: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

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
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifacontrollere", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_controller_technician_router():
    """Get controller technician router - alias for get_technician_router"""
    return get_technician_router()
