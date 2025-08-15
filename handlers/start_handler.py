"""
Start Handler - Simplified Implementation

This module handles the /start command and shows appropriate menus
based on user role.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from loader import get_user_role
from utils.user_repository import upsert_user_in_clients
from utils.role_system import show_role_menu
from config import get_admin_regions, is_global_admin
from database.region_config import get_region_codes
from states.admin_states import AdminRegionStates


def _build_region_keyboard(regions: list[str]) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=r.title(), callback_data=f"choose_region:{r}")]
            for r in regions]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_start_router():
    """Get start router with all handlers"""
    router = Router()
    
    @router.message(F.text == "/start")
    async def start_command(message: Message, state: FSMContext):
        """Handle /start command"""
        try:
            user_role = await get_user_role(message.from_user.id)

            # Persist user to clients DB on first start
            is_created, saved = await upsert_user_in_clients({
                "telegram_id": message.from_user.id,
                "username": message.from_user.username,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "language": message.from_user.language_code or "uz",
                "role": user_role,
                "is_bot": message.from_user.is_bot,
            })
            
            # Clear any existing state
            await state.clear()

            # If admin (global or region), set/select region context
            if user_role == 'admin':
                assigned = get_admin_regions(message.from_user.id)
                if len(assigned) == 1:
                    await state.update_data(active_region=assigned[0])
                elif len(assigned) > 1:
                    # Ask to choose region
                    await state.set_state(AdminRegionStates.choosing_region)
                    await message.answer(
                        "Qaysi region uchun ishlamoqchisiz?",
                        reply_markup=_build_region_keyboard(assigned)
                    )
                    return
                else:
                    # Global admin bo‘lishi mumkin; agar region ko‘rsatilmagan bo‘lsa hech narsa qilmamiz
                    pass
            
            # Show welcome message
            created_note = "🆕 Ro'yxatdan o'tdingiz." if is_created else "🔄 Ma'lumotlaringiz yangilandi."
            welcome_text = (
                f"👋 Xush kelibsiz, {message.from_user.first_name}!\n\n"
                f"🤖 Alfa Connect botiga xush kelibsiz!\n"
                f"👤 Sizning rolingiz: {user_role.upper()}\n"
                f"{created_note}\n\n"
                f"Quyidagi menyulardan birini tanlang:"
            )
            
            await message.answer(welcome_text)
            
            # Show appropriate menu based on role
            if user_role == 'client':
                from keyboards.client_buttons import get_main_menu_keyboard
                keyboard = get_main_menu_keyboard('uz')
                await message.answer("Quyidagi menyudan kerakli bo'limni tanlang.", reply_markup=keyboard)
            else:
                await show_role_menu(message, user_role)
            
        except Exception as e:
            #await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            pass
    
    @router.callback_query(F.data.startswith("choose_region:"))
    async def choose_region_callback(callback: CallbackQuery, state: FSMContext):
        try:
            _, region = callback.data.split(":", 1)
            await state.update_data(active_region=region)
            await state.set_state(AdminRegionStates.active_region)
            await callback.answer()
            await callback.message.edit_text(f"Region tanlandi: {region.title()}")
            # After selecting region, open role menu
            await show_role_menu(callback.message, 'admin')
        except Exception:
            await callback.answer("Xatolik", show_alert=True)
    
    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to main menu button"""
        try:
            await callback.answer()
            
            user_role = get_user_role(callback.from_user.id)
            
            # Clear any existing state
            await state.clear()
            
            # Show appropriate menu based on role
            if user_role == 'client':
                from keyboards.client_buttons import get_main_menu_keyboard
                keyboard = get_main_menu_keyboard('uz')
                await callback.message.edit_text(
                    "Quyidagi menyudan kerakli bo'limni tanlang.",
                    reply_markup=keyboard
                )
            else:
                await show_role_menu(callback.message, user_role)
            
        except Exception as e:
            #await callback.message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            pass
    
    return router 