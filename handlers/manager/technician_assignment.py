"""
Manager Technician Assignment Handler

This module provides technician assignment functionality for Manager role,
allowing managers to assign technicians to applications and track their work.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_main_keyboard
from states.manager_states import ManagerTechnicianAssignmentStates
from datetime import datetime

def get_manager_technician_assignment_router():
    """Get technician assignment router for manager"""
    from utils.role_system import get_role_router
    router = get_role_router("manager")
    
    @router.message(F.text == "👨‍🔧 Texnik biriktirish")
    async def manager_technician_assignment_main(message: Message, state: FSMContext):
        """Manager technician assignment handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Mock technicians data
            technicians = [
                {
                    'id': 1,
                    'full_name': 'Test Technician 1',
                    'phone_number': '+998901234567',
                    'status': 'available'
                },
                {
                    'id': 2,
                    'full_name': 'Test Technician 2',
                    'phone_number': '+998901234568',
                    'status': 'available'
                },
                {
                    'id': 3,
                    'full_name': 'Test Technician 3',
                    'phone_number': '+998901234569',
                    'status': 'busy'
                }
            ]
            
            if not technicians:
                text = "Hozircha texniklar mavjud emas."
                await message.answer(text)
                return
            
            # Create technician selection keyboard
            buttons = []
            for tech in technicians:
                if tech['status'] == 'available':
                    buttons.append([InlineKeyboardButton(
                        text=f"👨‍🔧 {tech.get('full_name', 'N/A')}",
                        callback_data=f"select_tech_{tech['id']}"
                    )])
            
            buttons.append([InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data="back_to_main_menu"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            text = "👨‍🔧 Texnik tanlang:"
            
            await message.answer(text, reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("select_tech_"))
    async def select_technician(callback: CallbackQuery, state: FSMContext):
        """Select technician for assignment"""
        try:
            technician_id = int(callback.data.replace("select_tech_", ""))
            
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Mock technicians data
            technicians = [
                {
                    'id': 1,
                    'full_name': 'Test Technician 1',
                    'phone_number': '+998901234567',
                    'status': 'available'
                },
                {
                    'id': 2,
                    'full_name': 'Test Technician 2',
                    'phone_number': '+998901234568',
                    'status': 'available'
                },
                {
                    'id': 3,
                    'full_name': 'Test Technician 3',
                    'phone_number': '+998901234569',
                    'status': 'busy'
                }
            ]
            
            # Get technician details
            selected_tech = next((tech for tech in technicians if tech['id'] == technician_id), None)
            
            if not selected_tech:
                await callback.answer("Texnik topilmadi", show_alert=True)
                return
            
            # Mock applications data
            applications = [
                {
                    'id': 'APP-001',
                    'description': 'Internet ulanish muammosi',
                    'status': 'in_progress',
                    'client_name': 'Test Client 1'
                },
                {
                    'id': 'APP-002',
                    'description': 'Televizor signal muammosi',
                    'status': 'in_progress',
                    'client_name': 'Test Client 2'
                },
                {
                    'id': 'APP-003',
                    'description': 'Router sozlash muammosi',
                    'status': 'in_progress',
                    'client_name': 'Test Client 3'
                }
            ]
            
            if not applications:
                text = "Biriktirish uchun arizalar mavjud emas."
                await callback.message.edit_text(
                    text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(
                            text="◀️ Orqaga",
                            callback_data="back_to_main_menu"
                        )
                    ]])
                )
                return
            
            # Create application selection keyboard
            buttons = []
            for app in applications[:10]:  # Limit to 10 applications
                buttons.append([InlineKeyboardButton(
                    text=f"📋 {app['id']} - {app.get('description', 'N/A')[:30]}",
                    callback_data=f"assign_tech_{technician_id}_{app['id']}"
                )])
            
            buttons.append([InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data="back_to_main_menu"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            text = f"👨‍🔧 {selected_tech.get('full_name', 'N/A')} uchun ariza tanlang:"
            
            await callback.message.edit_text(text, reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("assign_tech_"))
    async def assign_technician_to_application(callback: CallbackQuery, state: FSMContext):
        """Assign technician to specific application"""
        try:
            parts = callback.data.replace("assign_tech_", "").split("_")
            technician_id = int(parts[0])
            application_id = parts[1]
            
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Mock technicians data
            technicians = [
                {
                    'id': 1,
                    'full_name': 'Test Technician 1',
                    'phone_number': '+998901234567',
                    'status': 'available'
                },
                {
                    'id': 2,
                    'full_name': 'Test Technician 2',
                    'phone_number': '+998901234568',
                    'status': 'available'
                },
                {
                    'id': 3,
                    'full_name': 'Test Technician 3',
                    'phone_number': '+998901234569',
                    'status': 'busy'
                }
            ]
            
            # Get technician details
            selected_tech = next((tech for tech in technicians if tech['id'] == technician_id), None)
            
            if not selected_tech:
                await callback.answer("Texnik topilmadi", show_alert=True)
                return
            
            # Mock assignment success
            success = True
            
            if success:
                text = (
                    f"✅ Texnik muvaffaqiyatli biriktirildi!\n\n"
                    f"👨‍🔧 Texnik: {selected_tech.get('full_name', 'N/A')}\n"
                    f"📋 Ariza: {application_id}\n"
                    f"📞 Telefon: {selected_tech.get('phone_number', 'N/A')}\n"
                    f"⏰ Biriktirilgan vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                )
                
                # Mock notification to technician
                notification_text = f"Sizga yangi ariza biriktirildi: {application_id}"
                
            else:
                text = "❌ Texnik biriktirishda xatolik yuz berdi."
            
            await callback.message.edit_text(
                text,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(
                        text="◀️ Orqaga",
                        callback_data="back_to_main_menu"
                    )
                ]])
            )
            
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Back to main menu"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            lang = user.get('language', 'uz')
            text = "🏠 Asosiy menyuga qaytdingiz."
            
            await callback.message.edit_text(
                text,
                reply_markup=get_manager_main_keyboard(lang)
            )
            
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router 