"""
Junior Manager Application Viewing - Complete Implementation

This module handles application viewing for junior managers.
"""

from loader import logger
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime
from utils.role_system import get_role_router

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
    """Mock user language"""
    return 'uz'

async def cleanup_user_inline_messages(user_id: int):
    """Mock cleanup function"""
    pass

async def send_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock send and track"""
    return await message_func(text, **kwargs)

async def edit_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock edit and track"""
    return await message_func(text, **kwargs)

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

# Mock keyboard functions
def get_application_list_keyboard(applications: List[Dict], page: int = 1, lang: str = 'uz'):
    """Mock application list keyboard"""
    keyboard_buttons = []
    
    for app in applications:
        status_emoji = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'cancelled': '❌'
        }.get(app.get('status', 'pending'), '⏳')
        
        priority_emoji = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🟠',
            'urgent': '🔴'
        }.get(app.get('priority', 'medium'), '🟡')
        
        button_text = f"{status_emoji} {priority_emoji} #{app['id']} - {app.get('client_name', 'N/A')}"
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"jm_view_app_{app['id']}"
            )
        ])
    
    # Navigation buttons
    keyboard_buttons.append([
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_main"),
        InlineKeyboardButton(text="❌ Yopish", callback_data="jm_close_menu")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

def get_application_action_keyboard(app_id: int, status: str, lang: str = 'uz'):
    """Mock application action keyboard"""
    keyboard_buttons = []
    
    if status != 'cancelled':
        keyboard_buttons.append([
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data=f"jm_cancel_app_{app_id}"
            )
        ])
    
    keyboard_buttons.append([
        InlineKeyboardButton(text="📋 Batafsil", callback_data=f"jm_details_app_{app_id}"),
        InlineKeyboardButton(text="◀️ Orqaga", callback_data="jm_view_applications")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerApplicationStates(StatesGroup):
    viewing_applications = State()
    viewing_application_details = State()

def get_junior_manager_application_viewing_router():
    """Get router for junior manager application viewing handlers"""
    router = get_role_router("junior_manager")

    @router.message(F.text.in_(["📋 Arizalarni ko'rish"]))
    async def view_applications(message: Message, state: FSMContext):
        """View applications list"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            
            # Get applications
            applications = await get_junior_manager_applications(user['id'], limit=50)
            
            if applications:
                text = f"📋 Sizning arizalaringiz ({len(applications)} ta):\n\n"
                
                await edit_and_track(
                    message.answer(
                        text,
                        reply_markup=get_application_list_keyboard(applications, lang=lang)
                    ),
                    message.from_user.id
                )
            else:
                text = """📋 Hozircha arizalar yo'q.

🔌 Yangi ariza yaratishni xohlaysizmi?"""
                
                await message.answer(text)
            
        except Exception as e:
            logger.error(f"Error in view_applications - User ID: {message.from_user.id}, Error: {str(e)}", exc_info=True)
            print(f"Error in view_applications: {e}")
            await message.answer("Xatolik yuz berdi")

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
            applications = await get_junior_manager_applications(user['id'], limit=1000)
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
                    'medium': 'O\'rta',
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
                
                # Create action keyboard
                await callback.message.edit_text(
                    text,
                    reply_markup=get_application_action_keyboard(app_id, application.get('status'), lang=lang)
                )
            else:
                text = "❌ Ariza topilmadi"
                await callback.answer(text, show_alert=True)
            
        except Exception as e:
            logger.error(f"Error in handle_application_view - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            print(f"Error in handle_application_view: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_cancel_app_"))
    async def handle_application_cancellation(callback: CallbackQuery, state: FSMContext):
        """Handle application cancellation"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            app_id = int(callback.data.split("_")[-1])
            
            # Check if application belongs to this junior manager
            applications = await get_junior_manager_applications(user['id'], limit=1000)
            application = next((app for app in applications if app['id'] == app_id), None)
            
            if not application:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            if application.get('status') == 'cancelled':
                text = "❌ Ariza allaqachon bekor qilingan"
                await callback.answer(text, show_alert=True)
                return
            
            # Cancel application
            success = await update_application_status_as_junior_manager(app_id, 'cancelled')
            
            if success:
                text = f"""✅ Ariza #{app_id} muvaffaqiyatli bekor qilindi.

Статус заявки изменен на 'отменена'."""
                
                await callback.message.edit_text(text)
                print(f"Junior Manager {user['id']} cancelled application {app_id}")
            else:
                text = "❌ Arizani bekor qilishda xatolik"
                await callback.answer(text, show_alert=True)
            
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error cancelling application - User ID: {callback.from_user.id}, Error: {str(e)}", exc_info=True)
            print(f"Error cancelling application: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_details_app_"))
    async def handle_application_details_view(callback: CallbackQuery, state: FSMContext):
        """Handle detailed application view"""
        # This is the same as jm_view_app_ but can be extended for more detailed view
        await handle_application_view(callback, state)

    @router.callback_query(F.data.startswith("jm_apps_page_"))
    async def handle_application_pagination(callback: CallbackQuery, state: FSMContext):
        """Handle application list pagination"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            page = int(callback.data.split("_")[-1])
            
            # Get applications for the page
            applications = await get_junior_manager_applications(user['id'], limit=50)
            
            text = f"📋 Sizning arizalaringiz ({len(applications)} ta):\n\n"
            
            await callback.message.edit_text(
                text, 
                reply_markup=get_application_list_keyboard(applications, page=page, lang=lang)
            )
            await callback.answer()
            
        except Exception as e:
            print(f"Error handling pagination: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "jm_close_menu")
    async def handle_close_menu(callback: CallbackQuery, state: FSMContext):
        """Handle menu closing"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz') if user else 'uz'
            
            text = "✅ Menyu yopildi"
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            print(f"Error closing menu: {e}")
            await callback.answer()

    return router 