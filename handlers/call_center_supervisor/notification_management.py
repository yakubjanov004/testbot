"""
Call Center Supervisor Notification Management Handler - Simplified Implementation

This module handles notification management functionality for call center supervisors,
including sending messages, announcements, and managing notifications.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from states.call_center_supervisor_states import CallCenterSupervisorStates

def get_call_center_supervisor_notification_management_router():
    """Get router for call center supervisor notification management handlers - Simplified Implementation"""
    router = Router()

    @router.message(F.text.in_(["📢 E'lon yuborish"]))
    async def handle_send_announcement(message: Message, state: FSMContext):
        """Handle sending announcements"""
        try:
            text = """
📢 E'lon yuborish

Jamoa uchun e'lon matnini yozing:
            """
            
            await message.answer(text)
            await state.set_state(CallCenterSupervisorStates.main_menu)
            await state.update_data(action="send_announcement")
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text.in_(["💬 Jamoa xabari"]))
    async def handle_team_message(message: Message, state: FSMContext):
        """Handle sending team messages"""
        try:
            text = """
💬 Jamoa xabari

Jamoa a'zolariga yubormoqchi bo'lgan xabaringizni yozing:
            """
            
            await message.answer(text)
            await state.set_state(CallCenterSupervisorStates.main_menu)
            await state.update_data(action="send_team_message")
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text.in_(["👤 Shaxsiy xabar"]))
    async def handle_individual_message(message: Message, state: FSMContext):
        """Handle sending individual messages"""
        try:
            # Mock staff list
            staff_list = [
                {
                    'id': 1,
                    'full_name': 'Operator 1',
                    'role': 'call_center_operator'
                },
                {
                    'id': 2,
                    'full_name': 'Operator 2',
                    'role': 'call_center_operator'
                }
            ]
            
            if not staff_list:
                await message.answer("❌ Xodimlar topilmadi.")
                return
            
            text = """
👤 Shaxsiy xabar yuborish

Xabar yubormoqchi bo'lgan xodimni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"👤 {staff['full_name']} ({staff['role']})", callback_data=f"ccs_select_staff_msg_{staff['id']}")]
                for staff in staff_list[:8]
            ] + [
                [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ccs_cancel_individual_message")]
            ])
            
            await message.answer(text, reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text.in_(["🚨 Shoshilinch ogohlantirish"]))
    async def handle_urgent_alert(message: Message, state: FSMContext):
        """Handle sending urgent alerts"""
        try:
            text = """
🚨 Shoshilinch ogohlantirish

⚠️ Bu xabar barcha xodimlarga shoshilinch ravishda yuboriladi.

Ogohlantirish matnini yozing:
            """
            
            await message.answer(text)
            await state.set_state(CallCenterSupervisorStates.main_menu)
            await state.update_data(action="send_urgent_alert")
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("ccs_notification_"))
    async def handle_notification_callbacks(callback: CallbackQuery, state: FSMContext):
        """Handle notification management callbacks"""
        try:
            data = callback.data
            
            if data == "ccs_new_notifications":
                await _show_new_notifications(callback)
            elif data == "ccs_send_staff_message":
                await _show_staff_selection_for_message(callback)
            elif data == "ccs_broadcast_message":
                await _show_broadcast_message_form(callback)
            elif data == "ccs_send_warning":
                await _show_warning_message_form(callback)
            elif data == "ccs_notifications_history":
                await _show_notifications_history(callback)
            else:
                await callback.answer("❌ Noma'lum buyruq", show_alert=True)
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ccs_select_staff_msg_"))
    async def handle_staff_selection_for_message(callback: CallbackQuery, state: FSMContext):
        """Handle staff selection for individual message"""
        try:
            staff_id = int(callback.data.split("_")[-1])
            
            # Mock staff info
            staff_list = [
                {
                    'id': 1,
                    'full_name': 'Operator 1',
                    'role': 'call_center_operator'
                },
                {
                    'id': 2,
                    'full_name': 'Operator 2',
                    'role': 'call_center_operator'
                }
            ]
            
            selected_staff = next((s for s in staff_list if s['id'] == staff_id), None)
            
            if not selected_staff:
                await callback.answer("❌ Xodim topilmadi", show_alert=True)
                return
            
            text = f"""
👤 {selected_staff['full_name']} ga xabar yuborish

Xabar matnini yozing:
            """
            
            await callback.message.edit_text(text)
            await state.set_state(CallCenterSupervisorStates.main_menu)
            await state.update_data(action="send_individual_message", target_staff_id=staff_id)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router


# Helper functions for notification management
async def _show_new_notifications(callback: CallbackQuery):
    """Show new notifications"""
    try:
        # Mock notifications data
        notifications = [
            {
                'id': 1,
                'type': 'order_escalated',
                'order_id': '12345678',
                'client_name': 'Test Client',
                'created_at': datetime.now()
            },
            {
                'id': 2,
                'type': 'staff_performance_warning',
                'order_id': '87654321',
                'client_name': 'Another Client',
                'created_at': datetime.now()
            }
        ]
        
        if not notifications:
            text = "📭 Yangi bildirishnomalar yo'q."
            await callback.message.edit_text(text, reply_markup=get_notification_management_keyboard())
            return
        
        text = f"🔔 Yangi bildirishnomalar ({len(notifications)}):\n\n"
        
        for notification in notifications[:5]:
            type_emoji = "⬆️" if notification['type'] == 'order_escalated' else "⏰"
            text += f"""
{type_emoji} {notification['type'].replace('_', ' ').title()}
   📋 #{notification['order_id']}
   👤 {notification.get('client_name', 'N/A')}
   📅 {notification['created_at'].strftime('%d.%m %H:%M')}
            """
        
        await callback.message.edit_text(text, reply_markup=get_notification_management_keyboard())
        await callback.answer()
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


async def _show_staff_selection_for_message(callback: CallbackQuery):
    """Show staff selection for messaging"""
    try:
        # Mock staff list
        staff_list = [
            {
                'id': 1,
                'full_name': 'Operator 1',
                'role': 'call_center_operator'
            },
            {
                'id': 2,
                'full_name': 'Operator 2',
                'role': 'call_center_operator'
            }
        ]
        
        if not staff_list:
            await callback.message.edit_text("❌ Xodimlar topilmadi.")
            return
        
        text = """
👥 Xodim tanlash

Xabar yubormoqchi bo'lgan xodimni tanlang:
        """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"👤 {staff['full_name']} ({staff['role']})", callback_data=f"ccs_select_staff_msg_{staff['id']}")]
            for staff in staff_list[:8]
        ] + [
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ccs_cancel_staff_selection")]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


async def _show_broadcast_message_form(callback: CallbackQuery):
    """Show broadcast message form"""
    try:
        text = """
📢 Ommaviy xabar yuborish

⚠️ Bu xabar barcha nazorat ostidagi xodimlarga yuboriladi.

Xabar matnini yozing:
        """
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


async def _show_warning_message_form(callback: CallbackQuery):
    """Show warning message form"""
    try:
        text = """
⚠️ Ogohlantirish yuborish

🚨 Bu shoshilinch ogohlantirish xabari.

Ogohlantirish matnini yozing:
        """
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


async def _show_notifications_history(callback: CallbackQuery):
    """Show notifications history"""
    try:
        # Mock notifications history
        text = """
📋 Bildirishnomalar tarixi

Oxirgi bildirishnomalar:

📅 Bugun:
• 09:30 - Yangi buyurtma eskalatsiyasi
• 11:15 - Xodim samaradorlik ogohlantirishsi
• 14:20 - Tizim yangilanish xabari

📅 Kecha:
• 16:45 - Haftalik hisobot tayyor
• 18:00 - Ish kuni yakunlandi

Batafsil tarix uchun hisobot so'rang.
        """
        
        await callback.message.edit_text(text, reply_markup=get_notification_management_keyboard())
        await callback.answer()
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


def get_notification_management_keyboard():
    """Get notification management keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Yangi bildirishnomalar", callback_data="ccs_new_notifications")],
        [InlineKeyboardButton(text="👥 Xodimga xabar", callback_data="ccs_send_staff_message")],
        [InlineKeyboardButton(text="📢 Ommaviy xabar", callback_data="ccs_broadcast_message")],
        [InlineKeyboardButton(text="⚠️ Ogohlantirish", callback_data="ccs_send_warning")],
        [InlineKeyboardButton(text="📋 Tarix", callback_data="ccs_notifications_history")]
    ])