from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import controllers_main_menu
from states.controller_states import ControllerMainMenuStates
from utils.reply_utils import (
    send_or_edit_message,
    answer_callback_query,
    reply_with_error,
    clear_message_state
)

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

async def get_system_statistics():
    """Mock system statistics"""
    return {
        'total_orders': 150,
        'completed_orders': 120,
        'pending_orders': 30,
        'active_clients': 85,
        'active_technicians': 12,
        'revenue_today': 2500000,
        'avg_completion_time': 2.5
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

# Removed duplicate get_role_router - using centralized version from utils.role_system

def get_controller_main_menu_router():
    """Get controller main menu router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["🎛️ Controller", "🎛️ Nazoratchi"]))
    async def controllers_start(message: Message, state: FSMContext):
        """Controllers panel asosiy menyu"""
        user_id = message.from_user.id
        
        try:
            await clear_message_state(state)
            await state.clear()
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                return await reply_with_error(message, state, "Sizda ruxsat yo'q.")
                
            await state.set_state(ControllerMainMenuStates.main_menu)
            lang = user.get('language', 'uz')
            stats = await get_system_statistics()
            
            welcome_text = (
                "🎛️ <b>Nazoratchi paneli</b>\n\n"
                "📊 <b>Tizim holati:</b>\n"
                f"• Jami buyurtmalar: {stats.get('total_orders', 0)}\n"
                f"• Bajarilgan: {stats.get('completed_orders', 0)}\n"
                f"• Kutilayotgan: {stats.get('pending_orders', 0)}\n"
                f"• Faol mijozlar: {stats.get('active_clients', 0)}\n"
                f"• Faol texniklar: {stats.get('active_technicians', 0)}\n\n"
                "Kerakli bo'limni tanlang:"
            )
            
            await send_or_edit_message(
                message, 
                welcome_text, 
                state, 
                reply_markup=controllers_main_menu(lang), 
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in controllers_start: {str(e)}")
            await reply_with_error(message, state, "Xatolik yuz berdi")

    @router.message(F.text.in_(["🏠 Bosh menyu"]))
    async def back_to_main_menu(message: Message, state: FSMContext):
        """Bosh menyuga qaytish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                return await reply_with_error(message, state, "Sizda controller huquqi yo'q.")
                
            await controllers_start(message, state)
            
        except Exception as e:
            print(f"Error in back_to_main_menu: {str(e)}")
            await reply_with_error(message, state, "Xatolik yuz berdi")

    @router.callback_query(F.data == "controllers_back")
    async def controllers_back_handler(callback: CallbackQuery, state: FSMContext):
        """Handle controllers back button"""
        try:
            await answer_callback_query(callback)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            stats = await get_system_statistics()
            
            welcome_text = (
                "🎛️ <b>Nazoratchi paneli</b>\n\n"
                "📊 <b>Tizim holati:</b>\n"
                f"• Jami buyurtmalar: {stats.get('total_orders', 0)}\n"
                f"• Bajarilgan: {stats.get('completed_orders', 0)}\n"
                f"• Kutilayotgan: {stats.get('pending_orders', 0)}\n"
                f"• Faol mijozlar: {stats.get('active_clients', 0)}\n"
                f"• Faol texniklar: {stats.get('active_technicians', 0)}\n\n"
                "Kerakli bo'limni tanlang:"
            )
            
            await send_or_edit_message(
                callback, 
                welcome_text, 
                state, 
                reply_markup=controllers_main_menu(lang), 
                parse_mode='HTML'
            )
            await state.set_state(ControllerMainMenuStates.main_menu)
            
        except Exception as e:
            await reply_with_error(callback, state, "❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_controller_main")
    async def back_to_controller_main_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to controller main menu button"""
        try:
            await answer_callback_query(callback)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            stats = await get_system_statistics()
            
            welcome_text = (
                "🎛️ <b>Nazoratchi paneli</b>\n\n"
                "📊 <b>Tizim holati:</b>\n"
                f"• Jami buyurtmalar: {stats.get('total_orders', 0)}\n"
                f"• Bajarilgan: {stats.get('completed_orders', 0)}\n"
                f"• Kutilayotgan: {stats.get('pending_orders', 0)}\n"
                f"• Faol mijozlar: {stats.get('active_clients', 0)}\n"
                f"• Faol texniklar: {stats.get('active_technicians', 0)}\n\n"
                "Kerakli bo'limni tanlang:"
            )
            
            await send_or_edit_message(
                callback, 
                welcome_text, 
                state, 
                reply_markup=controllers_main_menu(lang), 
                parse_mode='HTML'
            )
            await state.set_state(ControllerMainMenuStates.main_menu)
            
        except Exception as e:
            await reply_with_error(callback, state, "❌ Xatolik yuz berdi")

    return router
