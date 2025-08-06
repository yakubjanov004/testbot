"""
Manager Notifications Handler - Soddalashtirilgan versiya

Bu modul manager uchun xabarnomalar funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional

from keyboards.manager_buttons import get_manager_main_keyboard, get_notifications_keyboard
from states.manager_states import ManagerNotificationStates

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
async def get_users_by_role(role: str):
    """Mock get users by role"""
    if role == 'staff':
        return [
            {
                'id': 2,
                'full_name': 'Ahmad Toshmatov',
                'role': 'staff',
                'phone_number': '+998901234568'
            },
            {
                'id': 3,
                'full_name': 'Malika Karimova',
                'role': 'staff',
                'phone_number': '+998901234569'
            }
        ]
    elif role == 'technician':
        return [
            {
                'id': 4,
                'full_name': 'Umar Azimov',
                'role': 'technician',
                'phone_number': '+998901234570'
            }
        ]
    elif role == 'junior_manager':
        return [
            {
                'id': 5,
                'full_name': 'Jahongir Karimov',
                'role': 'junior_manager',
                'phone_number': '+998901234571'
            }
        ]
    return []

# Mock notification system
class MockNotificationSystem:
    """Mock notification system"""
    async def send_notification(self, user_id: int, message_type: str, title: str, message: str):
        """Mock send notification"""
        print(f"Mock: Sending notification to user {user_id}: {title} - {message}")
        return True

# Global mock instance
notification_system = MockNotificationSystem()

def get_manager_notifications_router():
    """Get notifications router for manager"""
    router = Router()
    
    @router.message(F.text.in_(["📢 Xabarnomalar"]))
    async def manager_notifications_main(message: Message, state: FSMContext):
        """Manager notifications handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            
            if not user or user['role'] != 'manager':
                error_text = "Sizda menejer huquqi yo'q."
                await message.answer(error_text)
                return
            
            lang = user.get('language', 'uz')
            print(f"Manager {user['id']} accessed notifications")
            
            text = (
                "📢 Xabarnomalar bo'limiga xush kelibsiz!\n\n"
                "Quyidagi funksiyalardan birini tanlang:"
            )
            
            # Use send_and_track for inline cleanup
            await message.answer(
                text=text,
                reply_markup=get_notifications_keyboard(lang)
            )
            
        except Exception as e:
            print(f"Error in manager_notifications_main: {str(e)}")
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data == "send_staff_notification")
    async def send_staff_notification(callback: CallbackQuery, state: FSMContext):
        """Send notification to staff"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get staff members
            staff_members = await get_users_by_role('staff')
            staff_members.extend(await get_users_by_role('technician'))
            staff_members.extend(await get_users_by_role('junior_manager'))
            
            if not staff_members:
                text = "Hozircha xodimlar mavjud emas."
                await callback.message.edit_text(
                    text=text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(
                            text="◀️ Orqaga",
                            callback_data="back_to_notifications"
                        )
                    ]])
                )
                return
            
            # Create staff selection keyboard
            buttons = []
            for staff in staff_members[:10]:  # Limit to 10 staff members
                buttons.append([InlineKeyboardButton(
                    text=f"👤 {staff.get('full_name', 'N/A')} ({staff.get('role', 'N/A')})",
                    callback_data=f"select_staff_{staff['id']}"
                )])
            
            buttons.append([InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data="back_to_notifications"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            text = "👤 Xabarnoma yuborish uchun xodim tanlang:"
            
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in send_staff_notification: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("select_staff_"))
    async def select_staff_for_notification(callback: CallbackQuery, state: FSMContext):
        """Select staff member for notification"""
        try:
            staff_id = int(callback.data.replace("select_staff_", ""))
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get staff details
            staff_members = await get_users_by_role('staff')
            staff_members.extend(await get_users_by_role('technician'))
            staff_members.extend(await get_users_by_role('junior_manager'))
            
            selected_staff = next((staff for staff in staff_members if staff['id'] == staff_id), None)
            
            if not selected_staff:
                await callback.answer("Xodim topilmadi", show_alert=True)
                return
            
            # Store selected staff ID in state
            await state.update_data(selected_staff_id=staff_id)
            await state.set_state(ManagerNotificationStates.sending_notification_message)
            
            text = f"📝 {selected_staff.get('full_name', 'N/A')} uchun xabarnoma matnini kiriting:"
            
            await callback.message.edit_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(
                        text="❌ Bekor qilish",
                        callback_data="cancel_notification"
                    )
                ]])
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in select_staff_for_notification: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(ManagerNotificationStates.sending_notification_message)
    async def handle_notification_message(message: Message, state: FSMContext):
        """Handle notification message input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get selected staff ID from state
            data = await state.get_data()
            staff_id = data.get('selected_staff_id')
            
            if not staff_id:
                await message.answer("Xatolik: Xodim tanlanmagan")
                await state.clear()
                return
            
            # Get staff details
            staff_members = await get_users_by_role('staff')
            staff_members.extend(await get_users_by_role('technician'))
            staff_members.extend(await get_users_by_role('junior_manager'))
            
            selected_staff = next((staff for staff in staff_members if staff['id'] == staff_id), None)
            
            if not selected_staff:
                await message.answer("Xodim topilmadi")
                await state.clear()
                return
            
            # Send notification
            success = await notification_system.send_notification(
                user_id=staff_id,
                message_type="manager_notification",
                title="Menejer xabarnomasi",
                message=message.text
            )
            
            if success:
                text = (
                    f"✅ Xabarnoma muvaffaqiyatli yuborildi!\n\n"
                    f"👤 Kimga: {selected_staff.get('full_name', 'N/A')}\n"
                    f"📝 Xabar: {message.text[:50]}..."
                )
            else:
                text = "❌ Xabarnoma yuborishda xatolik yuz berdi."
            
            await message.answer(text)
            await state.clear()
            
        except Exception as e:
            print(f"Error in handle_notification_message: {str(e)}")
            await message.answer("Xatolik yuz berdi")
            await state.clear()

    @router.callback_query(F.data == "send_broadcast_notification")
    async def send_broadcast_notification(callback: CallbackQuery, state: FSMContext):
        """Send broadcast notification to all staff"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Set state for broadcast message
            await state.set_state(ManagerNotificationStates.sending_notification_message)
            await state.update_data(broadcast=True)
            
            text = "📢 Barcha xodimlarga yuboriladigan xabarnoma matnini kiriting:"
            
            await callback.message.edit_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(
                        text="❌ Bekor qilish",
                        callback_data="cancel_notification"
                    )
                ]])
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in send_broadcast_notification: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "cancel_notification")
    async def cancel_notification(callback: CallbackQuery, state: FSMContext):
        """Cancel notification sending"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            await state.clear()
            
            text = "❌ Xabarnoma yuborish bekor qilindi."
            
            await callback.message.edit_text(
                text=text,
                reply_markup=get_notifications_keyboard(lang)
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in cancel_notification: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_notifications")
    async def back_to_notifications(callback: CallbackQuery, state: FSMContext):
        """Back to notifications menu"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            text = "📢 Xabarnomalar bo'limiga qaytdingiz."
            
            await callback.message.edit_text(
                text=text,
                reply_markup=get_notifications_keyboard(lang)
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in back_to_notifications: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Back to main menu"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            text = "🏠 Asosiy menyuga qaytdingiz."
            
            await callback.message.edit_text(
                text=text,
                reply_markup=get_manager_main_keyboard(lang)
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in back_to_main_menu: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router 