"""
Manager Filters Handler - Soddalashtirilgan versiya

Bu modul manager uchun arizalarni filtrlash funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta

from keyboards.manager_buttons import (
    get_manager_filter_reply_keyboard,
    get_status_filter_inline_keyboard,
    get_date_filter_inline_keyboard,
    get_tech_filter_inline_keyboard,
    get_filter_results_keyboard,
    get_manager_main_keyboard
)
from states.manager_states import ManagerFilterStates

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

# Mock database functions
async def get_filtered_applications(db, **kwargs):
    """Mock get filtered applications"""
    from datetime import datetime
    return {
        'applications': [
            {
                'id': 'req_001_2024_01_15',
                'status': 'in_progress',
                'user_name': 'Aziz Karimov',
                'description': 'Internet ulanish arizasi',
                'created_at': datetime.now(),
                'technician_id': 1
            },
            {
                'id': 'req_002_2024_01_16',
                'status': 'new',
                'user_name': 'Malika Toshmatova',
                'description': 'TV signal muammosi',
                'created_at': datetime.now(),
                'technician_id': None
            },
            {
                'id': 'req_003_2024_01_17',
                'status': 'completed',
                'user_name': 'Jahongir Azimov',
                'description': 'Qo\'ng\'iroq markazi arizasi',
                'created_at': datetime.now(),
                'technician_id': 2
            }
        ],
        'total_pages': 1,
        'total': 3
    }

def get_manager_filters_router():
    """Get complete filters router for manager"""
    router = Router()
    
    @router.message(F.text.in_(["🔍 Filtrlar"]))
    async def manager_filters_main(message: Message, state: FSMContext):
        """Manager filters handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            
            if not user or user['role'] != 'manager':
                await message.answer("Sizda menejer huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            print(f"Manager {user['id']} accessed filters")
            
            # Clear any existing filter state
            await state.clear()
            await state.set_state(ManagerFilterStates.selecting_filter_type)
            
            filters_text = (
                f"🔍 <b>Arizalarni filtrlash</b>\n\n"
                f"Qanday filtr turini tanlaysiz?\n\n"
                f"🟢 Status bo'yicha - yangi, jarayonda, bajarilgan\n"
                f"📅 Sana bo'yicha - bugun, kecha, hafta, oy\n"
                f"👨‍🔧 Texnik biriktirilganligi bo'yicha\n\n"
                f"Filtr turini tanlang:"
            )
            
            # Use send_and_track for inline cleanup
            await message.answer(
                filters_text,
                parse_mode='HTML',
                reply_markup=get_manager_filter_reply_keyboard(lang)
            )
            
        except Exception as e:
            print(f"Error in manager_filters_main: {e}")
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)
    
    @router.message(F.text.in_(["🟢 Status bo'yicha"]))
    async def filter_by_status(message: Message, state: FSMContext):
        """Filter applications by status"""
        try:
            print(f"Status filter button clicked by user {message.from_user.id}")
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                print(f"User {message.from_user.id} not authorized for status filter")
                return
            
            lang = user.get('language', 'uz')
            await state.set_state(ManagerFilterStates.selecting_status)
            
            status_text = (
                f"🟢 <b>Status bo'yicha filtrlash</b>\n\n"
                f"Qaysi statusdagi arizalarni ko'rishni xohlaysiz?\n\n"
                f"🆕 Yangi - hali boshlanmagan arizalar\n"
                f"⏳ Jarayonda - hozir bajarilayotgan arizalar\n"
                f"✅ Yakunlangan - muvaffaqiyatli bajarilgan\n"
                f"❌ Bekor qilingan - bekor qilingan arizalar\n"
                f"📋 Barchasi - barcha arizalar\n\n"
                f"Statusni tanlang:"
            )
            
            # Use send_and_track for inline cleanup
            await message.answer(
                status_text,
                parse_mode='HTML',
                reply_markup=get_status_filter_inline_keyboard(lang)
            )
            
        except Exception as e:
            print(f"Error in filter_by_status: {e}")
    
    @router.callback_query(F.data.startswith("filter_status_"))
    async def handle_status_filter(callback: CallbackQuery, state: FSMContext):
        """Handle status filter selection"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            status = callback.data.split("_")[-1]  # new, in_progress, completed, cancelled, all
            
            # Store filter in state
            await state.update_data(filter_type='status', filter_value=status)
            
            # Get filtered applications
            if status == 'all':
                result = await get_filtered_applications(None, page=1, limit=10)
            else:
                result = await get_filtered_applications(None, statuses=[status], page=1, limit=10)
            
            applications = result.get('applications', [])
            total_pages = result.get('total_pages', 1)
            total_count = result.get('total', 0)
            
            if not applications:
                no_apps_text = (
                    f"📭 Tanlangan status bo'yicha arizalar topilmadi.\n\n"
                    f"Status: {get_status_text(status, lang)}\n\n"
                    f"Boshqa filtr tanlang yoki keyinroq qaytib ko'ring."
                )
                
                # Use edit_and_track for inline cleanup
                await callback.message.edit_text(
                    no_apps_text,
                    reply_markup=get_back_to_filters_keyboard(lang)
                )
                
                await callback.answer()
                return
            
            # Show filtered results
            await show_filtered_results(callback, applications, total_count, total_pages, 1, lang, f"Status: {get_status_text(status, lang)}")
            
        except Exception as e:
            print(f"Error in handle_status_filter: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.message(F.text.in_(["📅 Sana bo'yicha"]))
    async def filter_by_date(message: Message, state: FSMContext):
        """Filter applications by date"""
        try:
            print(f"Date filter button clicked by user {message.from_user.id}")
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                print(f"User {message.from_user.id} not authorized for date filter")
                return
            
            lang = user.get('language', 'uz')
            await state.set_state(ManagerFilterStates.selecting_date)
            
            date_text = (
                f"📅 <b>Sana bo'yicha filtrlash</b>\n\n"
                f"Qaysi vaqt oralig'idagi arizalarni ko'rishni xohlaysiz?\n\n"
                f"📅 Bugun - bugun yaratilgan arizalar\n"
                f"🗓️ Kecha - kecha yaratilgan arizalar\n"
                f"📆 Bu hafta - oxirgi 7 kun ichida\n"
                f"🗓️ Bu oy - oxirgi 30 kun ichida\n\n"
                f"Vaqt oralig'ini tanlang:"
            )
            
            await message.answer(
                date_text,
                parse_mode='HTML',
                reply_markup=get_date_filter_inline_keyboard(lang)
            )
            
        except Exception as e:
            print(f"Error in filter_by_date: {e}")
    
    @router.callback_query(F.data.startswith("filter_date_"))
    async def handle_date_filter(callback: CallbackQuery, state: FSMContext):
        """Handle date filter selection"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            date_filter = callback.data.split("_")[-1]  # today, yesterday, week, month
            
            # Calculate date range
            today = date.today()
            if date_filter == 'today':
                date_from = today.strftime('%Y-%m-%d')
                date_to = today.strftime('%Y-%m-%d')
            elif date_filter == 'yesterday':
                yesterday = today - timedelta(days=1)
                date_from = yesterday.strftime('%Y-%m-%d')
                date_to = yesterday.strftime('%Y-%m-%d')
            elif date_filter == 'week':
                week_ago = today - timedelta(days=7)
                date_from = week_ago.strftime('%Y-%m-%d')
                date_to = today.strftime('%Y-%m-%d')
            elif date_filter == 'month':
                month_ago = today - timedelta(days=30)
                date_from = month_ago.strftime('%Y-%m-%d')
                date_to = today.strftime('%Y-%m-%d')
            else:
                await callback.answer("Noto'g'ri sana filtri", show_alert=True)
                return
            
            # Store filter in state
            await state.update_data(filter_type='date', filter_value=date_filter, date_from=date_from, date_to=date_to)
            
            # Get filtered applications
            result = await get_filtered_applications(
                None, 
                date_from=date_from, 
                date_to=date_to, 
                page=1, 
                limit=10
            )
            
            applications = result.get('applications', [])
            total_pages = result.get('total_pages', 1)
            total_count = result.get('total', 0)
            
            if not applications:
                no_apps_text = (
                    f"📭 Tanlangan sana oralig'ida arizalar topilmadi.\n\n"
                    f"Sana: {get_date_text(date_filter, lang)}\n\n"
                    f"Boshqa filtr tanlang yoki keyinroq qaytib ko'ring."
                )
                
                await callback.message.edit_text(
                    no_apps_text,
                    reply_markup=get_back_to_filters_keyboard(lang)
                )
                await callback.answer()
                return
            
            # Show filtered results
            await show_filtered_results(callback, applications, total_count, total_pages, 1, lang, f"Sana: {get_date_text(date_filter, lang)}")
            
        except Exception as e:
            print(f"Error in handle_date_filter: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.message(F.text.in_(["👨‍🔧 Texnik biriktirilganligi bo'yicha"]))
    async def filter_by_technician(message: Message, state: FSMContext):
        """Filter applications by technician assignment"""
        try:
            print(f"Technician filter button clicked by user {message.from_user.id}")
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                print(f"User {message.from_user.id} not authorized for technician filter")
                return
            
            lang = user.get('language', 'uz')
            await state.set_state(ManagerFilterStates.selecting_technician)
            
            tech_text = (
                f"👨‍🔧 <b>Texnik biriktirilganligi bo'yicha filtrlash</b>\n\n"
                f"Qaysi turdagi arizalarni ko'rishni xohlaysiz?\n\n"
                f"👨‍🔧 Biriktirilgan - texnikka biriktirilgan arizalar\n"
                f"🚫 Biriktirilmagan - hali texnik biriktirilmagan arizalar\n\n"
                f"Turni tanlang:"
            )
            
            await message.answer(
                tech_text,
                parse_mode='HTML',
                reply_markup=get_tech_filter_inline_keyboard(lang)
            )
            
        except Exception as e:
            print(f"Error in filter_by_technician: {e}")
    
    @router.callback_query(F.data.startswith("filter_tech_"))
    async def handle_technician_filter(callback: CallbackQuery, state: FSMContext):
        """Handle technician filter selection"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            tech_filter = callback.data.split("_")[-1]  # assigned, unassigned
            
            # Store filter in state
            await state.update_data(filter_type='technician', filter_value=tech_filter)
            
            # Get filtered applications
            if tech_filter == 'assigned':
                result = await get_filtered_applications(None, assigned_only=True, page=1, limit=10)
            else:  # unassigned
                result = await get_filtered_applications(None, technician_id=0, page=1, limit=10)
            
            applications = result.get('applications', [])
            total_pages = result.get('total_pages', 1)
            total_count = result.get('total', 0)
            
            if not applications:
                no_apps_text = (
                    f"📭 Tanlangan filtr bo'yicha arizalar topilmadi.\n\n"
                    f"Filtr: {get_tech_text(tech_filter, lang)}\n\n"
                    f"Boshqa filtr tanlang yoki keyinroq qaytib ko'ring."
                )
                
                await callback.message.edit_text(
                    no_apps_text,
                    reply_markup=get_back_to_filters_keyboard(lang)
                )
                await callback.answer()
                return
            
            # Show filtered results
            await show_filtered_results(callback, applications, total_count, total_pages, 1, lang, f"Texnik: {get_tech_text(tech_filter, lang)}")
            
        except Exception as e:
            print(f"Error in handle_technician_filter: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("filter_page_"))
    async def handle_filter_pagination(callback: CallbackQuery, state: FSMContext):
        """Handle pagination for filtered results"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            page = int(callback.data.split("_")[-1])
            
            # Get filter data from state
            data = await state.get_data()
            filter_type = data.get('filter_type')
            filter_value = data.get('filter_value')
            
            # Apply filter based on type
            if filter_type == 'status':
                if filter_value == 'all':
                    result = await get_filtered_applications(None, page=page, limit=10)
                else:
                    result = await get_filtered_applications(None, statuses=[filter_value], page=page, limit=10)
            elif filter_type == 'date':
                date_from = data.get('date_from')
                date_to = data.get('date_to')
                result = await get_filtered_applications(None, date_from=date_from, date_to=date_to, page=page, limit=10)
            elif filter_type == 'technician':
                if filter_value == 'assigned':
                    result = await get_filtered_applications(None, assigned_only=True, page=page, limit=10)
                else:
                    result = await get_filtered_applications(None, technician_id=0, page=page, limit=10)
            else:
                await callback.answer("Filtr ma'lumotlari topilmadi", show_alert=True)
                return
            
            applications = result.get('applications', [])
            total_pages = result.get('total_pages', 1)
            total_count = result.get('total', 0)
            
            # Show updated results
            filter_description = get_filter_description(filter_type, filter_value, lang)
            await show_filtered_results(callback, applications, total_count, total_pages, page, lang, filter_description)
            
        except Exception as e:
            print(f"Error in handle_filter_pagination: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "filter_clear")
    async def clear_filters(callback: CallbackQuery, state: FSMContext):
        """Clear all filters and return to main filters menu"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Clear filter state
            await state.clear()
            await state.set_state(ManagerFilterStates.selecting_filter_type)
            
            clear_text = (
                f"🔄 <b>Filtrlar tozalandi</b>\n\n"
                f"Barcha filtrlar bekor qilindi.\n"
                f"Yangi filtr tanlashingiz mumkin."
            )
            
            await callback.message.edit_text(
                clear_text,
                parse_mode='HTML',
                reply_markup=get_manager_filter_reply_keyboard(lang)
            )
            await callback.answer("✅ Filtrlar tozalandi")
            
        except Exception as e:
            print(f"Error in clear_filters: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.message(F.text.in_(["◀️ Orqaga"]))
    async def back_to_main_menu(message: Message, state: FSMContext):
        """Return to main menu"""
        try:
            print(f"Back to main menu button clicked by user {message.from_user.id}")
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                print(f"User {message.from_user.id} not authorized for back to main menu")
                return
            
            lang = user.get('language', 'uz')
            await state.clear()
            
            main_menu_text = "🏠 Asosiy menyu"
            
            await message.answer(
                main_menu_text,
                reply_markup=get_manager_main_keyboard(lang)
            )
            
        except Exception as e:
            print(f"Error in back_to_main_menu: {e}")
    
    @router.callback_query(F.data == "back_to_filters")
    async def back_to_filters_callback(callback: CallbackQuery, state: FSMContext):
        """Return to filters menu"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            await state.clear()
            await state.set_state(ManagerFilterStates.selecting_filter_type)
            
            filters_text = (
                f"🔍 <b>Arizalarni filtrlash</b>\n\n"
                f"Qanday filtr turini tanlaysiz?\n\n"
                f"🟢 Status bo'yicha - yangi, jarayonda, bajarilgan\n"
                f"📅 Sana bo'yicha - bugun, kecha, hafta, oy\n"
                f"👨‍🔧 Texnik biriktirilganligi bo'yicha\n\n"
                f"Filtr turini tanlang:"
            )
            
            # Send new message with reply keyboard instead of editing
            await callback.message.answer(
                filters_text,
                parse_mode='HTML',
                reply_markup=get_manager_filter_reply_keyboard(lang)
            )
            await callback.answer()
            
        except Exception as e:
            print(f"Error in back_to_filters_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu_callback(callback: CallbackQuery, state: FSMContext):
        """Return to main menu from callback"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            await state.clear()
            
            main_menu_text = "🏠 Asosiy menyu"
            
            # Send new message with reply keyboard instead of editing
            await callback.message.answer(
                main_menu_text,
                reply_markup=get_manager_main_keyboard(lang)
            )
            await callback.answer()
            
        except Exception as e:
            print(f"Error in back_to_main_menu_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    return router


# Helper functions
async def show_filtered_results(callback: CallbackQuery, applications: List[Dict], total_count: int, 
                              total_pages: int, current_page: int, lang: str, filter_description: str):
    """Show filtered applications results"""
    try:
        results_text = (
            f"🔍 <b>Filtr natijalari</b>\n\n"
            f"📊 {filter_description}\n"
            f"📋 Jami topildi: {total_count} ta\n"
            f"📄 Sahifa: {current_page}/{total_pages}\n\n"
        )
        
        # Add applications to text
        for i, app in enumerate(applications, 1):
            status_emoji = {
                'new': '🆕',
                'in_progress': '⏳',
                'completed': '✅',
                'cancelled': '❌'
            }.get(app.get('status', 'new'), '📋')
            
            results_text += (
                f"{status_emoji} <b>ID:</b> {app.get('id', 'N/A')}\n"
                f"👤 <b>Mijoz:</b> {app.get('user_name', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {app.get('description', 'Mavjud emas')[:50]}...\n"
                f"📅 <b>Sana:</b> {app.get('created_at', 'N/A')}\n\n"
            )
        
        # Create pagination keyboard
        has_prev = current_page > 1
        has_next = current_page < total_pages
        
        keyboard = get_filter_results_keyboard(current_page, total_pages, has_next, has_prev, lang)
        
        await callback.message.edit_text(
            results_text,
            parse_mode='HTML',
            reply_markup=keyboard
        )
        await callback.answer()
        
    except Exception as e:
        print(f"Error in show_filtered_results: {e}")
        await callback.answer("Xatolik yuz berdi", show_alert=True)


def get_status_text(status: str, lang: str) -> str:
    """Get status text in specified language"""
    status_texts = {
        'new': 'Yangi',
        'in_progress': 'Jarayonda',
        'completed': 'Yakunlangan',
        'cancelled': 'Bekor qilingan',
        'all': 'Barchasi'
    }
    return status_texts.get(status, status)


def get_date_text(date_filter: str, lang: str) -> str:
    """Get date filter text in specified language"""
    date_texts = {
        'today': 'Bugun',
        'yesterday': 'Kecha',
        'week': 'Bu hafta',
        'month': 'Bu oy'
    }
    return date_texts.get(date_filter, date_filter)


def get_tech_text(tech_filter: str, lang: str) -> str:
    """Get technician filter text in specified language"""
    tech_texts = {
        'assigned': 'Biriktirilgan',
        'unassigned': 'Biriktirilmagan'
    }
    return tech_texts.get(tech_filter, tech_filter)


def get_filter_description(filter_type: str, filter_value: str, lang: str) -> str:
    """Get filter description text"""
    if filter_type == 'status':
        return f"Status: {get_status_text(filter_value, lang)}"
    elif filter_type == 'date':
        return f"Sana: {get_date_text(filter_value, lang)}"
    elif filter_type == 'technician':
        return f"Texnik: {get_tech_text(filter_value, lang)}"
    else:
        return "Filtr"


def get_back_to_filters_keyboard(lang: str):
    """Get back to filters keyboard"""
    back_text = "🔙 Filtrlarga qaytish"
    main_menu_text = "🏠 Asosiy menyu"
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back_text, callback_data="back_to_filters")],
        [InlineKeyboardButton(text=main_menu_text, callback_data="back_to_main_menu")]
    ])