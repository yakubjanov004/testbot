"""
Junior Manager Details Input Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun tafsilotlarni kiritish funksionalligini o'z ichiga oladi.
Junior managerlarga mijozlarni chaqirgandan keyin tafsilotlarni kiritish imkonini beradi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
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

async def send_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock send and track"""
    return await message_func(text, **kwargs)

async def edit_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock edit and track"""
    return await message_func(text, **kwargs)

async def cleanup_user_inline_messages(user_id: int):
    """Mock cleanup function"""
    pass

# Using get_role_router from utils.role_system

async def get_service_request_details_for_junior_manager(app_id: int):
    """Mock get service request details"""
    return {
        'id': app_id,
        'client_name': 'Aziz Karimov',
        'client_phone': '+998901234567',
        'client_address': 'Tashkent, Chorsu',
        'description': 'Internet ulanish arizasi',
        'status': 'assigned_to_junior_manager',
        'created_at': datetime.now()
    }

async def add_application_notes(app_id: int, user_id: int, notes: str):
    """Mock add application notes"""
    return True

async def forward_application_to_controller(app_id: int, junior_manager_id: int):
    """Mock forward application to controller"""
    return True

# Mock keyboard functions
def get_back_to_inbox_keyboard(lang: str = 'uz'):
    """Mock back to inbox keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 Inbox-ga qaytish", callback_data="jm_back_to_inbox"),
            InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="jm_main_menu")
        ]
    ])

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerDetailsInputStates(StatesGroup):
    entering_details = State()
    confirming_details = State()

def get_junior_manager_details_input_router():
    """Get router for junior manager details input handlers"""
    router = get_role_router("junior_manager")

    @router.callback_query(F.data.startswith("jm_details_input_"))
    async def handle_details_input_start(callback: CallbackQuery, state: FSMContext):
        """Handle starting details input process"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            app_id = int(callback.data.split("_")[-1])
            
            # Get application details
            app_details = await get_service_request_details_for_junior_manager(app_id)
            if not app_details:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Store application ID in state
            await state.update_data(application_id=app_id)
            await state.set_state(JuniorManagerDetailsInputStates.entering_details)
            
            # Show details input prompt
            text = f"""📝 Ariza #{app_id} uchun tafsilotlarni kiriting:

👤 Mijoz: {app_details.get('client_name', 'N/A')}
📱 Telefon: {app_details.get('client_phone', 'N/A')}

📝 Qo'ng'iroq natijasida aniqlangan ma'lumotlarni yozing:
• Mijozning talablari
• Qo'shimcha ma'lumotlar
• Muhim eslatmalar

Xabar yuboring yoki 'Bekor qilish' tugmasini bosing:"""
            
            # Create keyboard
            keyboard = _create_details_input_keyboard(app_id, lang)
            
            await edit_and_track(
                callback.message.edit_text(
                    text,
                    reply_markup=keyboard
                ),
                callback.from_user.id
            )
            
        except Exception as e:
            print(f"Error in handle_details_input_start: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(JuniorManagerDetailsInputStates.entering_details)
    async def handle_details_input_message(message: Message, state: FSMContext):
        """Handle details input message"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return

            lang = user.get('language', 'uz')
            
            # Get application ID from state
            data = await state.get_data()
            app_id = data.get('application_id')
            
            if not app_id:
                await message.answer("Xatolik: ariza ID topilmadi")
                await state.clear()
                return
            
            # Get application details
            app_details = await get_service_request_details_for_junior_manager(app_id)
            if not app_details:
                await message.answer("Ariza topilmadi")
                await state.clear()
                return
            
            # Add notes to application
            details_text = message.text
            success = await add_application_notes(app_id, user['id'], details_text)
            
            if success:
                # Show success message
                text = f"""✅ Tafsilotlar qo'shildi!

📋 Ariza: #{app_id}
👤 Mijoz: {app_details.get('client_name', 'N/A')}
📱 Telefon: {app_details.get('client_phone', 'N/A')}

📝 Qo'shilgan tafsilotlar:
{details_text}

Endi arizani controller-ga yuborishingiz mumkin."""
                
                # Create keyboard with forward option
                keyboard = _create_details_confirmation_keyboard(app_id, lang)
                
                await send_and_track(
                    message.answer(text, reply_markup=keyboard),
                    message.from_user.id
                )
                
                # Clear state
                await state.clear()
                
            else:
                await message.answer("❌ Tafsilotlarni qo'shishda xatolik yuz berdi")
            
        except Exception as e:
            print(f"Error in handle_details_input_message: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("jm_details_"))
    async def handle_details_actions(callback: CallbackQuery, state: FSMContext):
        """Handle details action buttons"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            action = callback.data.split("_")[-1]
            app_id = int(callback.data.split("_")[-2])
            
            if action == "cancel":
                await _handle_details_cancel(callback, state, lang)
            elif action == "forward":
                await _handle_details_forward(callback, app_id, user['id'], lang)
            else:
                await callback.answer("Noto'g'ri amal", show_alert=True)
            
        except Exception as e:
            print(f"Error in handle_details_actions: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _handle_details_cancel(callback: CallbackQuery, state: FSMContext, lang: str):
        """Handle details input cancellation"""
        try:
            # Clear state
            await state.clear()
            
            text = "❌ Tafsilotlarni kiritish bekor qilindi"
            
            # Create back to inbox keyboard
            await edit_and_track(
                callback.message.edit_text(
                    text,
                    reply_markup=get_back_to_inbox_keyboard(lang=lang)
                ),
                callback.from_user.id
            )
            
            await callback.answer("❌ Bekor qilindi", show_alert=True)
            
        except Exception as e:
            print(f"Error in _handle_details_cancel: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _handle_details_forward(callback: CallbackQuery, app_id: int, junior_manager_id: int, lang: str):
        """Handle forwarding application after details input"""
        try:
            # Get application details
            app_details = await get_service_request_details_for_junior_manager(app_id)
            if not app_details:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Forward application to controller
            success = await forward_application_to_controller(app_id, junior_manager_id)
            
            if success:
                text = f"""✅ Ariza controller-ga yuborildi!

📋 Ariza: #{app_id}
👤 Mijoz: {app_details.get('client_name', 'N/A')}
📱 Telefon: {app_details.get('client_phone', 'N/A')}

🔄 Ariza endi controller inbox-ida ko'rinadi.
📝 Tafsilotlar ham qo'shildi."""
                
                # Create back to inbox keyboard
                await edit_and_track(
                    callback.message.edit_text(
                        text,
                        reply_markup=get_back_to_inbox_keyboard(lang=lang)
                    ),
                    callback.from_user.id
                )
                
                await callback.answer("✅ Yuborildi", show_alert=True)
                
            else:
                await callback.answer("❌ Yuborishda xatolik", show_alert=True)
            
        except Exception as e:
            print(f"Error in _handle_details_forward: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    def _create_details_input_keyboard(app_id: int, lang: str) -> InlineKeyboardMarkup:
        """Create keyboard for details input"""
        keyboard = [
            [InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data=f"jm_details_cancel_{app_id}"
            )]
        ]
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def _create_details_confirmation_keyboard(app_id: int, lang: str) -> InlineKeyboardMarkup:
        """Create keyboard for details confirmation"""
        keyboard = [
            [InlineKeyboardButton(
                text="📤 Controller-ga yuborish",
                callback_data=f"jm_details_forward_{app_id}"
            )],
            [InlineKeyboardButton(
                text="🔙 Inbox-ga qaytish",
                callback_data="jm_inbox_back"
            )]
        ]
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    return router 