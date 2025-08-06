"""
Manager Language Handler - Soddalashtirilgan versiya

Bu modul manager uchun til o'zgartirish funksionalligini o'z ichiga oladi.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from keyboards.manager_buttons import get_manager_main_keyboard

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
async def update_user_language(telegram_id: int, language: str):
    """Mock update user language"""
    print(f"Mock: Updating user {telegram_id} language to {language}")

def get_manager_language_router():
    """Get manager language router"""
    from aiogram import Router
    router = Router()

    @router.message(F.text.in_(['🌐 Tilni o\'zgartirish']))
    async def change_manager_language(message: Message, state: FSMContext):
        """Manager language change handler"""
        try:
            await message.delete()
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            current_lang = user.get('language', 'uz')
            
            # Create language selection keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🇺🇿 O'zbekcha" + (" ✅" if current_lang == 'uz' else ""),
                        callback_data="manager_lang_uz"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🇷🇺 Русский" + (" ✅" if current_lang == 'ru' else ""),
                        callback_data="manager_lang_ru"
                    )
                ]
            ])
            
            lang_text = "🌐 Tilni tanlang:\n\nJoriy til: O'zbekcha"
            
            sent_message = await message.answer(
                text=lang_text,
                reply_markup=keyboard
            )
            
            await state.update_data(last_message_id=sent_message.message_id)
            
        except Exception as e:
            print(f"Error in change_manager_language: {str(e)}")
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data.startswith("manager_lang_"))
    async def set_manager_language(callback: CallbackQuery, state: FSMContext):
        """Set manager language"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            selected_lang = callback.data.split('_')[-1]
            
            # Update user language
            await update_user_language(callback.from_user.id, selected_lang)
            
            # Update user object
            user['language'] = selected_lang
            
            # Create success message
            success_text = "✅ Til muvaffaqiyatli o'zgartirildi!\n\n🌐 Til: O'zbekcha"
            
            # Create main menu keyboard
            main_menu_keyboard = get_manager_main_keyboard(selected_lang)
            
            # Edit message with success and main menu
            await callback.message.edit_text(
                text=success_text,
                reply_markup=main_menu_keyboard
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in set_manager_language: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router
