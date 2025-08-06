"""
Call Center Supervisor Staff Application Creation Handler - Simplified Implementation

This module handles staff application creation for call center supervisors.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from datetime import datetime
from keyboards.call_center_supervisor_buttons import get_staff_application_keyboard
from states.call_center_supervisor_states import StaffApplicationStates

def get_call_center_supervisor_staff_application_creation_router():
    router = Router()

    @router.message(F.text.in_(["👥 Xodim arizasi yaratish", "👥 Создать заявку сотрудника"]))
    async def start_staff_application(message: Message, state: FSMContext):
        """Start staff application creation"""
        try:
            welcome_text = (
                "👥 **Xodim arizasi yaratish**\n\n"
                "Yangi xodim arizasini yaratish jarayonini boshlaymiz.\n\n"
                "Quyidagi ma'lumotlarni to'ldiring:"
            )
            
            keyboard = get_staff_application_keyboard()
            await message.answer(
                text=welcome_text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
            await state.set_state(StaffApplicationStates.selecting_application_type)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("app_type_"))
    async def select_application_type(callback: CallbackQuery, state: FSMContext):
        """Select application type"""
        try:
            await callback.answer()
            app_type = callback.data.split("_")[-1]
            await state.update_data(application_type=app_type)
            
            type_names = {
                'operator': 'Operator',
                'technician': 'Texnik',
                'supervisor': 'Supervisor',
                'manager': 'Menejer'
            }
            
            text = (
                f"✅ **Ariza turi tanlandi:** {type_names.get(app_type, 'N/A')}\n\n"
                "Endi xodim ma'lumotlarini kiriting.\n\n"
                "📝 **To'liq ism va familiya:**"
            )
            
            await callback.message.edit_text(
                text=text,
                parse_mode="Markdown"
            )
            
            await state.set_state(StaffApplicationStates.entering_full_name)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(StaffApplicationStates.entering_full_name))
    async def get_full_name(message: Message, state: FSMContext):
        """Get full name"""
        try:
            full_name = message.text
            await state.update_data(full_name=full_name)
            
            await message.answer(
                "📱 **Telefon raqamini kiriting:**\n"
                "Masalan: +998901234567"
            )
            
            await state.set_state(StaffApplicationStates.entering_phone)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(StaffApplicationStates.entering_phone))
    async def get_phone(message: Message, state: FSMContext):
        """Get phone number"""
        try:
            phone = message.text
            await state.update_data(phone=phone)
            
            await message.answer(
                "📧 **Email manzilini kiriting:**\n"
                "Masalan: xodim@example.com"
            )
            
            await state.set_state(StaffApplicationStates.entering_email)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(StaffApplicationStates.entering_email))
    async def get_email(message: Message, state: FSMContext):
        """Get email"""
        try:
            email = message.text
            await state.update_data(email=email)
            
            await message.answer(
                "🎓 **Tajriba yillarini kiriting:**\n"
                "Masalan: 3 yil"
            )
            
            await state.set_state(StaffApplicationStates.entering_experience)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(StaffApplicationStates.entering_experience))
    async def get_experience(message: Message, state: FSMContext):
        """Get experience"""
        try:
            experience = message.text
            await state.update_data(experience=experience)
            
            await message.answer(
                "📝 **Qo'shimcha ma'lumotlar:**\n"
                "Xodim haqida qo'shimcha ma'lumotlar (ixtiyoriy)"
            )
            
            await state.set_state(StaffApplicationStates.entering_notes)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(StaffApplicationStates.entering_notes))
    async def get_notes(message: Message, state: FSMContext):
        """Get notes"""
        try:
            notes = message.text
            await state.update_data(notes=notes)
            
            # Show confirmation
            data = await state.get_data()
            
            type_names = {
                'operator': 'Operator',
                'technician': 'Texnik',
                'supervisor': 'Supervisor',
                'manager': 'Menejer'
            }
            
            confirmation_text = (
                f"📋 **Xodim arizasi tasdiqlash**\n\n"
                f"👤 **To'liq ism:** {data.get('full_name', 'N/A')}\n"
                f"📱 **Telefon:** {data.get('phone', 'N/A')}\n"
                f"📧 **Email:** {data.get('email', 'N/A')}\n"
                f"🎓 **Tajriba:** {data.get('experience', 'N/A')}\n"
                f"👥 **Lavozim:** {type_names.get(data.get('application_type', 'N/A'), 'N/A')}\n"
                f"📝 **Izoh:** {data.get('notes', 'Izoh yo\'q')}\n\n"
                f"📅 **Sana:** {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                f"👨‍💼 **Yaratuvchi:** {message.from_user.full_name}\n\n"
                f"Arizani tasdiqlaysizmi?"
            )
            
            keyboard = [
                [
                    InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_staff_app"),
                    InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_staff_app")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await message.answer(
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            
            await state.set_state(StaffApplicationStates.confirming)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "confirm_staff_app")
    async def confirm_staff_application(callback: CallbackQuery, state: FSMContext):
        """Confirm staff application"""
        try:
            await callback.answer()
            
            data = await state.get_data()
            app_id = f"STAFF_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            success_text = (
                f"✅ **Xodim arizasi qabul qilindi!**\n\n"
                f"🆔 **Ariza ID:** {app_id}\n"
                f"👤 **Xodim:** {data.get('full_name', 'N/A')}\n"
                f"📅 **Sana:** {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                f"Ariza muvaffaqiyatli yaratildi va guruhga yuborildi."
            )
            
            await callback.message.edit_text(
                text=success_text,
                parse_mode="Markdown"
            )
            
            await state.clear()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "cancel_staff_app")
    async def cancel_staff_application(callback: CallbackQuery, state: FSMContext):
        """Cancel staff application"""
        try:
            await callback.answer()
            
            await callback.message.edit_text(
                "❌ **Ariza bekor qilindi**\n\n"
                "Xodim arizasi yaratish bekor qilindi."
            )
            
            await state.clear()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
