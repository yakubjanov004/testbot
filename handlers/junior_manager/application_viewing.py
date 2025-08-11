"""
Junior Manager Application Viewing - Complete Implementation

This module handles application viewing for junior managers.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime
from filters.role_filter import RoleFilter
from keyboards.junior_manager_buttons import (
    get_application_list_keyboard,
    get_application_action_keyboard
)

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

# Using get_role_router from utils.role_system

async def get_junior_manager_applications(user_id: int, limit: int = 50):
    """Mock junior manager applications"""
    return [
        {
            'id': 1,
            'client_name': 'Aziz Karimov',
            'client_phone': '+998901234567',
            'client_address': 'Tashkent, Chorsu',
            'priority': 'medium',
            'status': 'pending',
            'details': 'Internet ulanish arizasi',
            'created_at': datetime.now()
        },
        {
            'id': 2,
            'client_name': 'Malika Toshmatova',
            'client_phone': '+998901234568',
            'client_address': 'Tashkent, Yunusabad',
            'priority': 'high',
            'status': 'in_progress',
            'details': 'TV signal muammosi',
            'created_at': datetime.now()
        },
        {
            'id': 3,
            'client_name': 'Jamshid Mirzayev',
            'client_phone': '+998901234569',
            'client_address': 'Samarkand, Registon',
            'priority': 'urgent',
            'status': 'completed',
            'details': 'Telefon xizmati',
            'created_at': datetime.now()
        }
    ]

async def update_application_status_as_junior_manager(app_id: int, status: str):
    """Mock update application status"""
    return True

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerApplicationStates(StatesGroup):
    viewing_applications = State()
    viewing_application_details = State()

def get_junior_manager_application_viewing_router():
    """Get router for junior manager application viewing handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("junior_manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📋 Zayavkalarni ko'rish", "📋 Arizalarni ko'rish"]))
    async def view_applications(message: Message, state: FSMContext):
        """View applications list"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            
            # Get applications
            applications = await get_junior_manager_applications(user['id'], limit=50)
            await state.update_data(jm_apps=applications)
            
            if applications:
                text = f"📋 Sizning arizalaringiz ({len(applications)} ta):\n\n"
                await message.answer(
                    text,
                    reply_markup=get_application_list_keyboard(applications, page=0, lang=lang)
                )
            else:
                text = """📋 Hozircha arizalar yo'q.

🔌 Yangi ariza yaratishni xohlaysizmi?"""
                await message.answer(text)
            
        except Exception as e:
            print(f"Error in view_applications: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("jm_apps_page_"))
    async def paginate_applications(callback: CallbackQuery, state: FSMContext):
        """Handle applications pagination"""
        try:
            await callback.answer()
            data = await state.get_data()
            applications = data.get('jm_apps') or []
            page_str = callback.data.split('_')[-1]
            page = int(page_str) if page_str.isdigit() else 0
            text = f"📋 Sizning arizalaringiz ({len(applications)} ta):\n\n"
            await callback.message.edit_reply_markup(
                reply_markup=get_application_list_keyboard(applications, page=page, lang='uz')
            )
        except Exception as e:
            print(f"Error in paginate_applications: {e}")

    @router.callback_query(F.data.startswith("jm_view_app_"))
    async def handle_application_view(callback: CallbackQuery, state: FSMContext):
        """Handle application view details"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            app_id = int(callback.data.split("_")[-1])
            
            # Get application details
            data = await state.get_data()
            applications = data.get('jm_apps') or await get_junior_manager_applications(user['id'], limit=1000)
            application = next((app for app in applications if app['id'] == app_id), None)
            
            if application:
                status_text = {
                    'pending': 'Kutilmoqda',
                    'in_progress': 'Jarayonda',
                    'completed': 'Bajarildi',
                    'cancelled': 'Bekor qilindi'
                }.get(application.get('status', 'pending'), application.get('status', 'pending'))
                
                priority_text = {
                    'low': 'Past',
                    'medium': "O'rta",
                    'high': 'Yuqori',
                    'urgent': 'Shoshilinch'
                }.get(application.get('priority', 'medium'), application.get('priority', 'medium'))
                
                text = f"""📋 Ariza #{app_id} ma'lumotlari:

👤 Mijoz: {application.get('client_name', 'N/A')}
📱 Telefon: {application.get('client_phone', 'N/A')}
📍 Manzil: {application.get('client_address', 'N/A')}
⚡ Ustuvorlik: {priority_text}
📊 Holat: {status_text}
📝 Tafsilotlar: {application.get('details', 'N/A')}
📅 Yaratilgan: {application.get('created_at', 'N/A')}"""
                await callback.message.edit_text(
                    text,
                    reply_markup=get_application_action_keyboard(app_id, application.get('status'), lang=lang)
                )
            else:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
            
        except Exception as e:
            print(f"Error in handle_application_view: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_details_app_"))
    async def handle_application_details(callback: CallbackQuery, state: FSMContext):
        """Handle explicit details request button"""
        await handle_application_view(callback, state)

    @router.callback_query(F.data.startswith("jm_cancel_app_"))
    async def handle_application_cancellation(callback: CallbackQuery, state: FSMContext):
        """Handle application cancellation"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            app_id = int(callback.data.split("_")[-1])
            
            # Check if application belongs to this junior manager
            data = await state.get_data()
            applications = data.get('jm_apps') or await get_junior_manager_applications(user['id'], limit=1000)
            application = next((app for app in applications if app['id'] == app_id), None)
            
            if not application:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            if application.get('status') == 'cancelled':
                await callback.answer("❌ Ariza allaqachon bekor qilingan", show_alert=True)
                return
            
            # Cancel application (mock)
            success = await update_application_status_as_junior_manager(app_id, 'cancelled')
            
            if success:
                await callback.message.edit_text(f"✅ Ariza #{app_id} bekor qilindi.")
            else:
                await callback.answer("❌ Arizani bekor qilishda xatolik", show_alert=True)
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error cancelling application: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "jm_close_menu")
    async def close_applications_menu(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
        except Exception:
            pass

    @router.callback_query(F.data == "jm_track_all")
    async def back_to_applications(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            data = await state.get_data()
            applications = data.get('jm_apps') or []
            await callback.message.edit_text(
                text=f"📋 Sizning arizalaringiz ({len(applications)} ta):\n\n"
            )
            await callback.message.edit_reply_markup(
                reply_markup=get_application_list_keyboard(applications, page=0, lang='uz')
            )
        except Exception as e:
            print(f"Error in back_to_applications: {e}")

    return router 