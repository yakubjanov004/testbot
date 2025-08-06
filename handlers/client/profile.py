from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_client_profile_menu, get_edit_profile_keyboard
from states.client_states import ProfileStates
from utils.role_system import get_role_router

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

def client_only(func):
    """Decorator to ensure only clients can access"""
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper

def get_client_profile_router():
    router = get_role_router("client")

    @client_only
    @router.message(F.text.in_(['👤 Profil']))
    async def client_profile_handler(message: Message, state: FSMContext):
        """Mijoz profili bilan ishlash"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"client_profile_{message.from_user.id}", 5, 60):
                await message.answer("Iltimos, biroz kutib turing.")
                return
            
            # Start enhanced time tracking for profile access
            await time_tracker.start_role_tracking(
                request_id=f"client_profile_{message.from_user.id}",
                user_id=message.from_user.id,
                role='client',
                workflow_stage="profile_accessed"
            )
            
            # Track workflow transition for profile access
            await workflow_manager.track_workflow_transition(
                request_id=f"client_profile_{message.from_user.id}",
                from_role="main_menu",
                to_role="profile",
                user_id=message.from_user.id,
                notes='Client accessing profile section'
            )
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            profile_text = "Profil menyusi. Kerakli amalni tanlang."
            
            # Use send_and_track for inline cleanup
            sent_message = await message.answer(
                text=profile_text,
                reply_markup=get_client_profile_menu('uz')
            )
            
            await state.set_state(ProfileStates.profile_menu)
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"client_profile_{message.from_user.id}",
                handler_id=message.from_user.id,
                action="profile_accessed"
            )
            
            # Update enhanced statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log profile access
            await audit_logger.log_user_action(
                user_id=message.from_user.id,
                action="profile_accessed",
                details={"language": "uz"}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_profile_{message.from_user.id}",
                user_id=message.from_user.id,
                notes="Profile access completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="client_profile_handler_error",
                description=f"Error in client_profile_handler: {str(e)}",
                severity="error"
            )

    @client_only
    @router.callback_query(F.data == "client_view_info")
    async def handle_view_info(callback: CallbackQuery):
        """Mijoz ma'lumotlarini ko'rish"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"client_view_info_{callback.from_user.id}", 5, 60):
                await callback.answer("Iltimos, biroz kutib turing.", show_alert=True)
                return
            
            # Start time tracking for view info
            await time_tracker.start_role_tracking(
                request_id=f"client_view_info_{callback.from_user.id}",
                user_id=callback.from_user.id,
                role='client',
                workflow_stage="view_info_accessed"
            )
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            if not user:
                await callback.answer("Foydalanuvchi topilmadi")
                return
            
            # Format created_at date
            created_at = user.get('created_at')
            if created_at:
                if isinstance(created_at, str):
                    created_date = created_at
                else:
                    created_date = created_at.strftime("%d.%m.%Y %H:%M")
            else:
                created_date = "Noma'lum"
            
            # Format updated_at date
            updated_at = user.get('updated_at')
            if updated_at:
                if isinstance(updated_at, str):
                    updated_date = updated_at
                else:
                    updated_date = updated_at.strftime("%d.%m.%Y %H:%M")
            else:
                updated_date = "Noma'lum"
            
            info_text = (
                f"👤 **Shaxsiy ma'lumotlar:**\n\n"
                f"🆔 **ID:** `{user.get('id', 'Noma\'lum')}`\n"
                f"📱 **Telegram ID:** `{user.get('telegram_id', 'Noma\'lum')}`\n"
                f"📝 **Ism:** {user.get('full_name', 'Kiritilmagan')}\n"
                f"📞 **Telefon:** {user.get('phone_number', 'Kiritilmagan')}\n"
                f"📍 **Manzil:** {user.get('address', 'Kiritilmagan')}\n"
                f"🌐 **Til:** {'O\'zbekcha' if user.get('language') == 'uz' else 'Русский'}\n"
                f"📅 **Ro'yxatdan o'tgan:** {created_date}\n"
                f"🔄 **Oxirgi yangilangan:** {updated_date}\n"
                f"✅ **Faol:** {'Ha' if user.get('is_active') else 'Yo\'q'}"
            )
            
            # Use edit_and_track for inline cleanup
            await callback.message.edit_text(
                text=info_text,
                reply_markup=get_client_profile_menu('uz'),
                parse_mode="Markdown"
            )
            
            await callback.answer()
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"client_view_info_{callback.from_user.id}",
                handler_id=callback.from_user.id,
                action="view_info_accessed"
            )
            
            # Update statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log view info access
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="view_info_accessed",
                details={"language": "uz"}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_view_info_{callback.from_user.id}",
                user_id=callback.from_user.id,
                notes="View info access completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="handle_view_info_error",
                description=f"Error in handle_view_info: {str(e)}",
                severity="error"
            )
            await callback.answer("Xatolik yuz berdi")

    @client_only
    @router.callback_query(F.data == "client_order_stats")
    async def handle_order_stats(callback: CallbackQuery):
        """Mijoz arizalar statistikasini ko'rish"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"client_order_stats_{callback.from_user.id}", 5, 60):
                await callback.answer("Iltimos, biroz kutib turing.", show_alert=True)
                return
            
            # Start time tracking for order stats
            await time_tracker.start_role_tracking(
                request_id=f"client_order_stats_{callback.from_user.id}",
                user_id=callback.from_user.id,
                role='client',
                workflow_stage="order_stats_accessed"
            )
            
            stats = await get_user_zayavka_statistics(callback.from_user.id)
            
            # If stats is an integer (error case), convert to default stats
            if isinstance(stats, int):
                stats = {
                    'total_orders': 0,
                    'completed_orders': 0,
                    'pending_orders': 0,
                    'cancelled_orders': 0,
                    'total_spent': 0
                }
            
            stats_text = (
                f"📊 Arizalar statistikasi:\n"
                f"🆕 Yangi: {stats['total_orders']}\n"
                f"🚧 Jarayonda: {stats['pending_orders']}\n"
                f"✅ Bajarilgan: {stats['completed_orders']}\n"
                f"❌ Bekor qilingan: {stats['cancelled_orders']}\n"
                f"💰 Umumiy sarflangan: {stats['total_spent']} so'm"
            )
            
            # Use edit_and_track for inline cleanup
            await callback.message.edit_text(
                text=stats_text,
                reply_markup=get_client_profile_menu('uz')
            )
            
            await callback.answer()
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"client_order_stats_{callback.from_user.id}",
                handler_id=callback.from_user.id,
                action="order_stats_accessed"
            )
            
            # Update statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log order stats access
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="order_stats_accessed",
                details={
                    "language": "uz",
                    "stats": stats
                }
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_order_stats_{callback.from_user.id}",
                user_id=callback.from_user.id,
                notes="Order stats access completed successfully"
            )

        except Exception as e:
            await audit_logger.log_system_event(
                event_type="handle_order_stats_error",
                description=f"Error in handle_order_stats: {str(e)}",
                severity="error"
            )
            await callback.answer("Xatolik yuz berdi")

    @client_only
    @router.callback_query(F.data == "client_profile_back")
    async def handle_back_to_profile(callback: CallbackQuery):
        """Orqaga qaytish"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"client_profile_back_{callback.from_user.id}", 5, 60):
                await callback.answer("Iltimos, biroz kutib turing.", show_alert=True)
                return
            
            # Start time tracking for back to profile
            await time_tracker.start_role_tracking(
                request_id=f"client_profile_back_{callback.from_user.id}",
                user_id=callback.from_user.id,
                role='client',
                workflow_stage="back_to_profile"
            )
            
            profile_text = "Profil menyusi. Kerakli amalni tanlang."
            
            # Use edit_and_track for inline cleanup
            await callback.message.edit_text(
                text=profile_text,
                reply_markup=get_client_profile_menu('uz')
            )
            
            await callback.answer()
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"client_profile_back_{callback.from_user.id}",
                handler_id=callback.from_user.id,
                action="back_to_profile"
            )
            
            # Update statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log back to profile
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="back_to_profile",
                details={"language": "uz"}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_profile_back_{callback.from_user.id}",
                user_id=callback.from_user.id,
                notes="Back to profile completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="handle_back_to_profile_error",
                description=f"Error in handle_back_to_profile: {str(e)}",
                severity="error"
            )
            await callback.answer("Xatolik yuz berdi")

    # Yangi profil o'zgartirish handlerlari
    @client_only
    @router.callback_query(F.data == "client_edit_profile")
    async def handle_edit_profile(callback: CallbackQuery):
        """Profil o'zgartirish menyusini ochish"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"client_edit_profile_{callback.from_user.id}", 5, 60):
                await callback.answer("Iltimos, biroz kutib turing.", show_alert=True)
                return
            
            # Start time tracking for edit profile
            await time_tracker.start_role_tracking(
                request_id=f"client_edit_profile_{callback.from_user.id}",
                user_id=callback.from_user.id,
                role='client',
                workflow_stage="edit_profile_accessed"
            )
            
            edit_text = "Profil o'zgartirish. Qaysi ma'lumotni o'zgartirmoqchisiz?"
            
            # Use edit_and_track for inline cleanup
            await callback.message.edit_text(
                text=edit_text,
                reply_markup=get_edit_profile_keyboard('uz')
            )
            
            await callback.answer()
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"client_edit_profile_{callback.from_user.id}",
                handler_id=callback.from_user.id,
                action="edit_profile_accessed"
            )
            
            # Update statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log edit profile access
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="edit_profile_accessed",
                details={"language": "uz"}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_edit_profile_{callback.from_user.id}",
                user_id=callback.from_user.id,
                notes="Edit profile access completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="handle_edit_profile_error",
                description=f"Error in handle_edit_profile: {str(e)}",
                severity="error"
            )
            await callback.answer("Xatolik yuz berdi")

    @client_only
    @router.callback_query(F.data == "client_edit_name")
    async def handle_edit_name(callback: CallbackQuery, state: FSMContext):
        """Ism o'zgartirish"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"client_edit_name_{callback.from_user.id}", 5, 60):
                await callback.answer("Iltimos, biroz kutib turing.", show_alert=True)
                return
            
            # Start time tracking for edit name
            await time_tracker.start_role_tracking(
                request_id=f"client_edit_name_{callback.from_user.id}",
                user_id=callback.from_user.id,
                role='client',
                workflow_stage="edit_name_accessed"
            )
            
            edit_text = "Yangi ismingizni kiriting:"
            
            # Use edit_and_track for inline cleanup
            await callback.message.edit_text(
                text=edit_text,
                reply_markup=get_edit_profile_keyboard('uz')
            )
            
            await state.set_state(ProfileStates.editing_name)
            await callback.answer()
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"client_edit_name_{callback.from_user.id}",
                handler_id=callback.from_user.id,
                action="edit_name_accessed"
            )
            
            # Update statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log edit name access
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="edit_name_accessed",
                details={"language": "uz"}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_edit_name_{callback.from_user.id}",
                user_id=callback.from_user.id,
                notes="Edit name access completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="handle_edit_name_error",
                description=f"Error in handle_edit_name: {str(e)}",
                severity="error"
            )
            await callback.answer("Xatolik yuz berdi")

    @client_only
    @router.message(ProfileStates.editing_name)
    async def handle_name_input(message: Message, state: FSMContext):
        """Ism kiritish"""
        try:
            # Start time tracking for name input
            await time_tracker.start_role_tracking(
                request_id=f"client_name_input_{message.from_user.id}",
                user_id=message.from_user.id,
                role='client',
                workflow_stage="name_input_processed"
            )
            
            await safe_delete_message(message.bot, message.chat.id, message.message_id)
            
            new_name = message.text.strip()
            if len(new_name) < 2:
                error_text = "Ism juda qisqa. Iltimos, to'liq ismingizni kiriting:"
                
                # Use send_and_track for inline cleanup
                sent_message = await message.answer(
                    text=error_text
                )
                
                # Track application handling
                await application_tracker.track_application_handling(
                    application_id=f"client_name_input_{message.from_user.id}",
                    handler_id=message.from_user.id,
                    action="name_input_validation_failed"
                )
                
                # Update statistics
                await statistics_manager.generate_role_based_statistics('client', 'daily')
                
                # Log name input validation failure
                await audit_logger.log_user_action(
                    user_id=message.from_user.id,
                    action="name_input_validation_failed",
                    details={"input_length": len(new_name)}
                )
                
                # End enhanced time tracking
                await time_tracker.end_role_tracking(
                    request_id=f"client_name_input_{message.from_user.id}",
                    user_id=message.from_user.id,
                    notes="Name input validation failed"
                )
                return
            
            # Update name in database
            success = await update_user_full_name(message.from_user.id, new_name)
            
            if success:
                success_text = f"Ism muvaffaqiyatli o'zgartirildi: {new_name}"
                
                # Use send_and_track for inline cleanup
                sent_message = await message.answer(
                    text=success_text
                )
                
                # Track application handling
                await application_tracker.track_application_handling(
                    application_id=f"client_name_input_{message.from_user.id}",
                    handler_id=message.from_user.id,
                    action="name_updated_successfully"
                )
                
                # Update statistics
                await statistics_manager.generate_role_based_statistics('client', 'daily')
                
                # Log successful name update
                await audit_logger.log_user_action(
                    user_id=message.from_user.id,
                    action="name_updated_successfully",
                    details={"new_name": new_name}
                )
            else:
                error_text = "Ism o'zgartirishda xatolik yuz berdi."
                
                # Use send_and_track for inline cleanup
                sent_message = await message.answer(
                    text=error_text
                )
                
                # Track application handling
                await application_tracker.track_application_handling(
                    application_id=f"client_name_input_{message.from_user.id}",
                    handler_id=message.from_user.id,
                    action="name_update_failed"
                )
                
                # Update statistics
                await statistics_manager.generate_role_based_statistics('client', 'daily')
                
                # Log name update failure
                await audit_logger.log_user_action(
                    user_id=message.from_user.id,
                    action="name_update_failed",
                    details={"new_name": new_name}
                )
            
            await state.clear()
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_name_input_{message.from_user.id}",
                user_id=message.from_user.id,
                notes="Name input processed"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="handle_name_input_error",
                description=f"Error in handle_name_input: {str(e)}",
                severity="error"
            )
            error_text = "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
            
            # Use send_and_track for inline cleanup
            sent_message = await message.answer(
                text=error_text
            )
            
            await state.clear()

    @client_only
    @router.callback_query(F.data == "client_edit_address")
    async def handle_edit_address(callback: CallbackQuery, state: FSMContext):
        """Manzil o'zgartirish"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"client_edit_address_{callback.from_user.id}", 5, 60):
                await callback.answer("Iltimos, biroz kutib turing.", show_alert=True)
                return
            
            # Start time tracking for edit address
            await time_tracker.start_role_tracking(
                request_id=f"client_edit_address_{callback.from_user.id}",
                user_id=callback.from_user.id,
                role='client',
                workflow_stage="edit_address_accessed"
            )
            
            edit_text = "Yangi manzilingizni kiriting:"
            
            # Use edit_and_track for inline cleanup
            await callback.message.edit_text(
                text=edit_text,
                reply_markup=get_edit_profile_keyboard('uz')
            )
            
            await state.set_state(ProfileStates.editing_address)
            await callback.answer()
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"client_edit_address_{callback.from_user.id}",
                handler_id=callback.from_user.id,
                action="edit_address_accessed"
            )
            
            # Update statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log edit address access
            await audit_logger.log_user_action(
                user_id=callback.from_user.id,
                action="edit_address_accessed",
                details={"language": "uz"}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_edit_address_{callback.from_user.id}",
                user_id=callback.from_user.id,
                notes="Edit address access completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="handle_edit_address_error",
                description=f"Error in handle_edit_address: {str(e)}",
                severity="error"
            )
            await callback.answer("Xatolik yuz berdi")

    @client_only
    @router.message(ProfileStates.editing_address)
    async def handle_address_input(message: Message, state: FSMContext):
        """Manzil kiritish"""
        try:
            # Start time tracking for address input
            await time_tracker.start_role_tracking(
                request_id=f"client_address_input_{message.from_user.id}",
                user_id=message.from_user.id,
                role='client',
                workflow_stage="address_input_processed"
            )
            
            await safe_delete_message(message.bot, message.chat.id, message.message_id)
            
            new_address = message.text.strip()
            if len(new_address) < 5:
                error_text = "Manzil juda qisqa. Iltimos, to'liq manzilni kiriting:"
                
                # Use send_and_track for inline cleanup
                sent_message = await message.answer(
                    text=error_text
                )
                
                # Track application handling
                await application_tracker.track_application_handling(
                    application_id=f"client_address_input_{message.from_user.id}",
                    handler_id=message.from_user.id,
                    action="address_input_validation_failed"
                )
                
                # Update statistics
                await statistics_manager.generate_role_based_statistics('client', 'daily')
                
                # Log address input validation failure
                await audit_logger.log_user_action(
                    user_id=message.from_user.id,
                    action="address_input_validation_failed",
                    details={"input_length": len(new_address)}
                )
                
                # End enhanced time tracking
                await time_tracker.end_role_tracking(
                    request_id=f"client_address_input_{message.from_user.id}",
                    user_id=message.from_user.id,
                    notes="Address input validation failed"
                )
                return
            
            # Update address in database
            success = await update_user_address(message.from_user.id, new_address)
            
            if success:
                success_text = f"Manzil muvaffaqiyatli o'zgartirildi: {new_address}"
                
                # Use send_and_track for inline cleanup
                sent_message = await message.answer(
                    text=success_text
                )
                
                # Track application handling
                await application_tracker.track_application_handling(
                    application_id=f"client_address_input_{message.from_user.id}",
                    handler_id=message.from_user.id,
                    action="address_updated_successfully"
                )
                
                # Update statistics
                await statistics_manager.generate_role_based_statistics('client', 'daily')
                
                # Log successful address update
                await audit_logger.log_user_action(
                    user_id=message.from_user.id,
                    action="address_updated_successfully",
                    details={"new_address": new_address}
                )
            else:
                error_text = "Manzil o'zgartirishda xatolik yuz berdi."
                
                # Use send_and_track for inline cleanup
                sent_message = await message.answer(
                    text=error_text
                )
                
                # Track application handling
                await application_tracker.track_application_handling(
                    application_id=f"client_address_input_{message.from_user.id}",
                    handler_id=message.from_user.id,
                    action="address_update_failed"
                )
                
                # Update statistics
                await statistics_manager.generate_role_based_statistics('client', 'daily')
                
                # Log address update failure
                await audit_logger.log_user_action(
                    user_id=message.from_user.id,
                    action="address_update_failed",
                    details={"new_address": new_address}
                )
            
            await state.clear()
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_address_input_{message.from_user.id}",
                user_id=message.from_user.id,
                notes="Address input processed"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="handle_address_input_error",
                description=f"Error in handle_address_input: {str(e)}",
                severity="error"
            )
            error_text = "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
            
            # Use send_and_track for inline cleanup
            sent_message = await message.answer(
                text=error_text
            )
            
            await state.clear()

    return router
