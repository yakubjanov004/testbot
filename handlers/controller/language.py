from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_controller_main_keyboard
from states.controller_states import ControllerSettingsStates
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

async def update_user_language(user_id: int, language: str):
    """Mock update user language"""
    print(f"Mock: Updating user {user_id} language to {language}")
    return True

async def get_user_lang(user_id: int) -> str:
    """Mock user language"""
    return 'uz'

# Removed duplicate get_role_router - using centralized version from utils.role_system

def get_controller_language_router():
    """Get controller language router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🌐 Tilni o'zgartirish"]))
    async def show_language_options(message: Message, state: FSMContext):
        """Show language selection as reply keyboard"""
        user_id = message.from_user.id
        
        try:
            lang_kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton("🇺🇿 O'zbekcha")],
                    [KeyboardButton("🔙 Orqaga")],
                ],
                resize_keyboard=True
            )
            await message.answer(
                "Tilni tanlang:",
                reply_markup=lang_kb
            )
            
        except Exception as e:
            print(f"Error in show_language_options: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["🇺🇿 O'zbek tili"]))
    async def set_uzbek_language(message: Message, state: FSMContext):
        """O'zbek tilini o'rnatish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer(
                    "Sizda controller huquqi yo'q.",
                )
                return
            
            success = await update_user_language(user['id'], 'uz')
            
            if success:
                text = """✅ <b>Til muvaffaqiyatli o'zgartirildi!</b>

Hozir siz O'zbek tilidan foydalanmoqdasiz 🇺🇿

Bosh menyuga qaytish uchun tugmani bosing."""
                
                await message.answer(
                    text,
                    reply_markup=get_controller_main_keyboard('uz'),
                    parse_mode='HTML'
                )
                await state.set_state(ControllerSettingsStates.main_menu)
                
                print(f"Controller {user['id']} changed language to Uzbek")
            else:
                text = "❌ Tilni o'zgartirishda xatolik yuz berdi."
                await message.answer(text)
            
        except Exception as e:
            print(f"Error in set_uzbek_language: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["🔙 Orqaga"]))
    async def back_from_language(message: Message, state: FSMContext):
        """Til menyusidan orqaga qaytish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer(
                    "Sizda controller huquqi yo'q.",
                )
                return
            
            lang = user.get('language', 'uz')
            await state.set_state(ControllerSettingsStates.main_menu)
            
            welcome_text = "🎛️ Nazoratchi paneliga xush kelibsiz!"
            
            await message.answer(
                welcome_text,
                reply_markup=get_controller_main_keyboard(lang)
            )
            
        except Exception as e:
            print(f"Error in back_from_language: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    return router
