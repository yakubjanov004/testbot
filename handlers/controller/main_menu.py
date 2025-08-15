from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_controller_main_keyboard
from states.controller_states import ControllerMainMenuStates
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
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🎛️ Controller", "🎛️ Nazoratchi"]))
    async def controllers_start(message: Message, state: FSMContext):
        """Controllers panel asosiy menyu"""
        user_id = message.from_user.id
        
        try:
            await state.clear()
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                text = "Sizda ruxsat yo'q."
                await message.answer(text)
                return
                
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
            
            await message.answer(welcome_text, reply_markup=get_controller_main_keyboard(lang), parse_mode='HTML')
            
        except Exception as e:
            print(f"Error in controllers_start: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["🏠 Bosh menyu"]))
    async def back_to_main_menu(message: Message, state: FSMContext):
        """Bosh menyuga qaytish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
                
            await controllers_start(message, state)
            
        except Exception as e:
            print(f"Error in back_to_main_menu: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data == "controllers_back")
    async def controllers_back_handler(callback: CallbackQuery, state: FSMContext):
        """Handle controllers back button"""
        try:
            await callback.answer()
            
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
            
            await callback.message.edit_text(welcome_text, reply_markup=get_controller_main_keyboard(lang), parse_mode='HTML')
            await state.set_state(ControllerMainMenuStates.main_menu)
            
        except Exception as e:
            await callback.message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "back_to_controller_main")
    async def back_to_controller_main_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to controller main menu button"""
        try:
            await callback.answer()
            
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
            
            await callback.message.edit_text(welcome_text, reply_markup=get_controller_main_keyboard(lang), parse_mode='HTML')
            await state.set_state(ControllerMainMenuStates.main_menu)
            
        except Exception as e:
            await callback.message.answer("❌ Xatolik yuz berdi")

    return router
