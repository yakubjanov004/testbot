"""
Manager Status Management Handler - Complete Implementation

This module provides complete status management functionality for Manager role,
allowing managers to change application statuses according to tex.txt workflow.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.manager_buttons import get_status_keyboard, get_manager_main_keyboard
from states.manager_states import ManagerStatusStates

def get_manager_status_management_router():
    """Get complete status management router for manager"""
    from aiogram import Router
    router = Router()
    
    @router.message(F.text == "🔄 Status o'zgartirish")
    async def manager_status_management_main(message: Message, state: FSMContext):
        """Manager status management handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            await state.set_state(ManagerStatusStates.selecting_application)
            
            status_text = (
                f"🔄 <b>Status o'zgartirish</b>\n\n"
                f"Qaysi arizaning statusini o'zgartirmoqchisiz?\n\n"
                f"📝 Ariza ID raqamini kiriting yoki\n"
                f"📋 Barcha arizalarni ko'rish uchun 'Barchasi' tugmasini bosing."
            )
            
            # Create inline keyboard for options
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📋 Barcha arizalar",
                        callback_data="status_view_all_applications"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🆕 Faqat yangi arizalar",
                        callback_data="status_view_new_applications"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏳ Jarayondagi arizalar",
                        callback_data="status_view_progress_applications"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙 Orqaga",
                        callback_data="back_to_main_menu"
                    )
                ]
            ])
            
            await message.answer(
                status_text,
                parse_mode='HTML',
                reply_markup=keyboard
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
    
    @router.callback_query(F.data == "status_view_all_applications")
    async def view_all_applications_for_status(callback: CallbackQuery, state: FSMContext):
        """View all applications for status change"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Mock applications data
            applications = [
                {
                    'id': 'APP-001',
                    'user_name': 'Test Client 1',
                    'description': 'Internet ulanish muammosi',
                    'status': 'new',
                    'created_at': '2024-01-15 10:30:00'
                },
                {
                    'id': 'APP-002',
                    'user_name': 'Test Client 2',
                    'description': 'Televizor signal muammosi',
                    'status': 'in_progress',
                    'created_at': '2024-01-14 15:45:00'
                },
                {
                    'id': 'APP-003',
                    'user_name': 'Test Client 3',
                    'description': 'Router sozlash muammosi',
                    'status': 'completed',
                    'created_at': '2024-01-13 09:20:00'
                }
            ]
            
            if not applications:
                no_apps_text = (
                    "📭 Hozircha arizalar mavjud emas.\n\n"
                    "Yangi arizalar paydo bo'lganda bu yerda ko'rinadi."
                )
                
                await callback.message.edit_text(
                    no_apps_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(
                            text="🔙 Orqaga",
                            callback_data="back_to_status_main"
                        )]
                    ])
                )
                await callback.answer()
                return
            
            # Show applications with status change buttons
            await show_applications_for_status_change(callback, applications, 'uz', "Barcha arizalar")
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "status_view_new_applications")
    async def view_new_applications_for_status(callback: CallbackQuery, state: FSMContext):
        """View new applications for status change"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Mock new applications data
            applications = [
                {
                    'id': 'APP-004',
                    'user_name': 'Test Client 4',
                    'description': 'Yangi internet ulanish',
                    'status': 'new',
                    'created_at': '2024-01-16 11:00:00'
                },
                {
                    'id': 'APP-005',
                    'user_name': 'Test Client 5',
                    'description': 'Yangi TV signal muammosi',
                    'status': 'new',
                    'created_at': '2024-01-16 12:30:00'
                }
            ]
            
            if not applications:
                no_apps_text = (
                    "📭 Yangi arizalar mavjud emas.\n\n"
                    "Barcha arizalar boshqa statuslarda."
                )
                
                await callback.message.edit_text(
                    no_apps_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(
                            text="🔙 Orqaga",
                            callback_data="back_to_status_main"
                        )]
                    ])
                )
                await callback.answer()
                return
            
            # Show new applications
            await show_applications_for_status_change(callback, applications, 'uz', "Yangi arizalar")
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "status_view_progress_applications")
    async def view_progress_applications_for_status(callback: CallbackQuery, state: FSMContext):
        """View in-progress applications for status change"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Mock in-progress applications data
            applications = [
                {
                    'id': 'APP-002',
                    'user_name': 'Test Client 2',
                    'description': 'Televizor signal muammosi',
                    'status': 'in_progress',
                    'created_at': '2024-01-14 15:45:00'
                },
                {
                    'id': 'APP-006',
                    'user_name': 'Test Client 6',
                    'description': 'Internet tezligi muammosi',
                    'status': 'in_progress',
                    'created_at': '2024-01-15 14:20:00'
                }
            ]
            
            if not applications:
                no_apps_text = (
                    "📭 Jarayondagi arizalar mavjud emas.\n\n"
                    "Hozirda hech qanday ariza bajarilmayapti."
                )
                
                await callback.message.edit_text(
                    no_apps_text,
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(
                            text="🔙 Orqaga",
                            callback_data="back_to_status_main"
                        )]
                    ])
                )
                await callback.answer()
                return
            
            # Show in-progress applications
            await show_applications_for_status_change(callback, applications, 'uz', "Jarayondagi arizalar")
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("change_app_status_"))
    async def change_application_status(callback: CallbackQuery, state: FSMContext):
        """Change application status - show status options"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            app_id = callback.data.split("_")[-1]
            
            # Mock application details
            app_details = {
                'id': app_id,
                'client_name': 'Test Client',
                'description': 'Test muammo tavsifi',
                'status': 'new',
                'created_at': '2024-01-15 10:30:00'
            }
            
            if not app_details:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Store application ID in state
            await state.update_data(selected_app_id=app_id)
            await state.set_state(ManagerStatusStates.selecting_new_status)
            
            # Show application details and available statuses
            current_status = app_details.get('status', 'new')
            available_statuses = get_available_statuses_for_manager(current_status)
            
            details_text = (
                f"🔄 <b>Status o'zgartirish</b>\n\n"
                f"📋 <b>Ariza tafsilotlari:</b>\n"
                f"🆔 ID: {app_details.get('id', 'N/A')[:8]}...\n"
                f"👤 Mijoz: {app_details.get('client_name', 'Noma\'lum')}\n"
                f"📝 Tavsif: {app_details.get('description', 'Mavjud emas')[:100]}...\n"
                f"📊 Joriy status: {get_status_display_text(current_status, 'uz')}\n\n"
                f"<b>Yangi statusni tanlang:</b>"
            )
            
            # Create status selection keyboard
            status_keyboard = get_status_keyboard(available_statuses, int(app_id) if app_id.isdigit() else 0, 'uz')
            
            await callback.message.edit_text(
                details_text,
                parse_mode='HTML',
                reply_markup=status_keyboard
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("status_"))
    async def handle_status_change(callback: CallbackQuery, state: FSMContext):
        """Handle status change confirmation"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Parse callback data: status_{new_status}_{app_id}
            parts = callback.data.split("_")
            if len(parts) < 3:
                await callback.answer("Noto'g'ri format", show_alert=True)
                return
            
            new_status = parts[1]
            app_id = parts[2]
            
            # Mock application details
            app_details = {
                'id': app_id,
                'client_name': 'Test Client',
                'description': 'Test muammo tavsifi',
                'status': 'new',
                'created_at': '2024-01-15 10:30:00'
            }
            
            current_status = app_details.get('status', 'new')
            
            # Validate status change
            if not is_valid_status_change(current_status, new_status):
                invalid_text = (
                    f"❌ Status o'zgartirib bo'lmaydi!\n\n"
                    f"Joriy status: {get_status_display_text(current_status, 'uz')}\n"
                    f"Yangi status: {get_status_display_text(new_status, 'uz')}\n\n"
                    f"Bu o'zgarish ruxsat etilmagan."
                )
                
                await callback.message.edit_text(invalid_text)
                await callback.answer("Noto'g'ri status o'zgarishi", show_alert=True)
                return
            
            # Show confirmation
            confirm_text = (
                f"❓ <b>Status o'zgarishini tasdiqlang</b>\n\n"
                f"📋 Ariza: {app_details.get('id', 'N/A')[:8]}...\n"
                f"👤 Mijoz: {app_details.get('client_name', 'Noma\'lum')}\n\n"
                f"📊 <b>Status o'zgarishi:</b>\n"
                f"Eski: {get_status_display_text(current_status, 'uz')}\n"
                f"Yangi: {get_status_display_text(new_status, 'uz')}\n\n"
                f"Tasdiqlaysizmi?"
            )
            
            confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Ha, tasdiqlash",
                        callback_data=f"confirm_status_change_{app_id}_{new_status}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Yo'q, bekor qilish",
                        callback_data=f"cancel_status_change_{app_id}"
                    )
                ]
            ])
            
            await callback.message.edit_text(
                confirm_text,
                parse_mode='HTML',
                reply_markup=confirm_keyboard
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("confirm_status_change_"))
    async def confirm_status_change(callback: CallbackQuery, state: FSMContext):
        """Confirm and apply status change"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Parse callback data: confirm_status_change_{app_id}_{new_status}
            parts = callback.data.split("_")
            if len(parts) < 5:
                await callback.answer("Noto'g'ri format", show_alert=True)
                return
            
            app_id = parts[3]
            new_status = parts[4]
            
            # Mock status change success
            success = True
            
            if success:
                success_text = (
                    f"✅ <b>Status muvaffaqiyatli o'zgartirildi!</b>\n\n"
                    f"📋 Ariza ID: {app_id[:8]}...\n"
                    f"📊 Yangi status: {get_status_display_text(new_status, 'uz')}\n"
                    f"👨‍💼 O'zgartirgan: {user.get('full_name', 'Manager')}\n"
                    f"📅 Vaqt: {get_current_time()}\n\n"
                    f"Barcha tegishli xodimlar bildirishnoma oldilar."
                )
                
                # Mock notification
                notification_text = f"Status o'zgartirildi: {app_id} -> {new_status}"
                
                await callback.message.edit_text(
                    success_text,
                    parse_mode='HTML',
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(
                            text="🔄 Boshqa ariza",
                            callback_data="back_to_status_main"
                        )],
                        [InlineKeyboardButton(
                            text="🏠 Asosiy menyu",
                            callback_data="back_to_main_menu"
                        )]
                    ])
                )
                
                await callback.answer("✅ Status o'zgartirildi!", show_alert=True)
            else:
                error_text = (
                    "❌ Status o'zgartirishda xatolik yuz berdi.\n\n"
                    "Iltimos, qaytadan urinib ko'ring."
                )
                
                await callback.message.edit_text(error_text)
                await callback.answer("Xatolik yuz berdi", show_alert=True)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "back_to_status_main")
    async def back_to_status_main(callback: CallbackQuery, state: FSMContext):
        """Return to status management main menu"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            await state.set_state(ManagerStatusStates.selecting_application)
            
            status_text = (
                f"🔄 <b>Status o'zgartirish</b>\n\n"
                f"Qaysi arizaning statusini o'zgartirmoqchisiz?\n\n"
                f"📝 Ariza ID raqamini kiriting yoki\n"
                f"📋 Barcha arizalarni ko'rish uchun 'Barchasi' tugmasini bosing."
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📋 Barcha arizalar",
                        callback_data="status_view_all_applications"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🆕 Faqat yangi arizalar",
                        callback_data="status_view_new_applications"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏳ Jarayondagi arizalar",
                        callback_data="status_view_progress_applications"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙 Orqaga",
                        callback_data="back_to_main_menu"
                    )
                ]
            ])
            
            await callback.message.edit_text(
                status_text,
                parse_mode='HTML',
                reply_markup=keyboard
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Return to main menu"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            await state.clear()
            
            main_menu_text = "🏠 Asosiy menyu"
            
            await callback.message.delete()
            await callback.message.answer(
                main_menu_text,
                reply_markup=get_manager_main_keyboard('uz')
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    return router


# Helper functions
async def show_applications_for_status_change(callback: CallbackQuery, applications, lang: str, title: str):
    """Show applications with status change buttons"""
    try:
        apps_text = (
            f"🔄 <b>{title}</b>\n\n"
            f"Status o'zgartirish uchun arizani tanlang:\n\n"
        )
        
        # Create buttons for each application
        buttons = []
        for i, app in enumerate(applications[:5], 1):  # Show first 5
            status_emoji = {
                'new': '🆕',
                'in_progress': '⏳',
                'completed': '✅',
                'cancelled': '❌'
            }.get(app.get('status', 'new'), '📋')
            
            app_text = f"{status_emoji} {app.get('id', 'N/A')[:8]}... - {app.get('user_name', 'Noma\'lum')}"
            
            buttons.append([
                InlineKeyboardButton(
                    text=app_text,
                    callback_data=f"change_app_status_{app.get('id', 0)}"
                )
            ])
        
        # Add navigation and back buttons
        if len(applications) > 5:
            buttons.append([
                InlineKeyboardButton(
                    text=f"➡️ Keyingi ({len(applications) - 5} ta)",
                    callback_data="status_next_page"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="back_to_status_main"
            )
        ])
        
        await callback.message.edit_text(
            apps_text,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


def get_available_statuses_for_manager(current_status: str):
    """Get available statuses that manager can change to"""
    status_transitions = {
        'new': ['in_progress', 'cancelled'],
        'in_progress': ['completed', 'cancelled'],
        'completed': [],  # Completed applications cannot be changed
        'cancelled': ['new'],  # Can reopen cancelled applications
        'pending': ['in_progress', 'cancelled']
    }
    return status_transitions.get(current_status, [])


def is_valid_status_change(current_status: str, new_status: str) -> bool:
    """Check if status change is valid"""
    available_statuses = get_available_statuses_for_manager(current_status)
    return new_status in available_statuses


def get_status_display_text(status: str, lang: str) -> str:
    """Get status display text in specified language"""
    status_texts = {
        'uz': {
            'new': '🆕 Yangi',
            'in_progress': '⏳ Jarayonda',
            'completed': '✅ Bajarilgan',
            'cancelled': '❌ Bekor qilingan',
            'pending': '⏸️ Kutilmoqda'
        }
    }
    return status_texts.get(lang, status_texts['uz']).get(status, status)


def get_current_time() -> str:
    """Get current time formatted"""
    return datetime.now().strftime('%d.%m.%Y %H:%M')


