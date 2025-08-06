from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_language_keyboard
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

async def update_user_language(user_id: int, language: str):
    """Mock update user language"""
    print(f"Mock: Updated user {user_id} language to {language}")

async def get_user_lang(user_id: int) -> str:
    """Mock get user language"""
    return 'uz'

async def answer_and_cleanup(callback, cleanup_after=True):
    """Mock answer and cleanup"""
    await callback.answer()

def get_client_language_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["🌐 Til o'zgartirish"]))
    async def client_change_language(message: Message, state: FSMContext):
        """Client language change handler"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"language_change_{message.from_user.id}", 5, 60):
                error_text = "Iltimos, biroz kutib turing."
                await message.answer(error_text)
                return
            
            # Start enhanced time tracking for language change
            await time_tracker.start_role_tracking(
                request_id=f"language_change_{message.from_user.id}",
                user_id=message.from_user.id,
                role='client',
                workflow_stage="language_change_initiated"
            )
            
            # Track workflow transition for language change
            await workflow_manager.track_workflow_transition(
                request_id=f"language_change_{message.from_user.id}",
                from_role="main_menu",
                to_role="language_change",
                user_id=message.from_user.id,
                notes='Client initiating language change'
            )
            
            user = await get_user_by_telegram_id(message.from_user.id)
            
            # Use send_and_track for inline cleanup
            sent_message = await send_and_track(
                message=message,
                text="Tilni tanlang:",
                reply_markup=get_language_keyboard('client')
            )
            
            await state.update_data(last_message_id=sent_message.message_id)  
            await state.set_state(LanguageStates.language_settings)
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"language_change_{message.from_user.id}",
                handler_id=message.from_user.id,
                action="language_change_initiated"
            )
            
            # Update enhanced statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log language change initiation
            await audit_logger.log_user_action(
                user_id=message.from_user.id,
                action="language_change_initiated",
                details={"role": "client", "current_language": "uz"}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"language_change_{message.from_user.id}",
                user_id=message.from_user.id,
                notes="Language change initiated successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="language_change_error",
                description=f"Error in client_change_language: {str(e)}",
                severity="error"
            )
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    async def process_client_language_change(callback: CallbackQuery, state: FSMContext):
        """Process client language change"""
        try:
            # Start enhanced time tracking for language processing
            await time_tracker.start_role_tracking(
                request_id=f"process_language_{callback.from_user.id}",
                user_id=callback.from_user.id,
                role='client',
                workflow_stage="language_change_processing"
            )
            
            # Track workflow transition for language processing
            await workflow_manager.track_workflow_transition(
                request_id=f"process_language_{callback.from_user.id}",
                from_role="language_change",
                to_role="language_change_processing",
                user_id=callback.from_user.id,
                notes='Processing client language change'
            )
            
            await answer_and_cleanup(callback, cleanup_after=True)
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"process_language_{callback.from_user.id}",
                handler_id=callback.from_user.id,
                action="language_change_processing"
            )
            
            await process_language_change(callback, state, role='client')
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"process_language_{callback.from_user.id}",
                user_id=callback.from_user.id,
                notes="Language change processing completed"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="process_language_change_error",
                description=f"Error in process_client_language_change: {str(e)}",
                severity="error"
            )
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("client_lang_"))
    async def handle_language_change_callback(call: CallbackQuery, state: FSMContext):
        """Handle language change callback"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"lang_callback_{call.from_user.id}", 3, 60):
                await call.answer("Iltimos, biroz kutib turing.", show_alert=True)
                return
            
            # Start enhanced time tracking for language change callback
            await time_tracker.start_role_tracking(
                request_id=f"lang_callback_{call.from_user.id}",
                user_id=call.from_user.id,
                role='client',
                workflow_stage="language_change_callback"
            )
            
            # Track workflow transition for language change callback
            await workflow_manager.track_workflow_transition(
                request_id=f"lang_callback_{call.from_user.id}",
                from_role="language_change_processing",
                to_role="language_change_callback",
                user_id=call.from_user.id,
                notes='Processing language change callback'
            )
            
            # Get current user data
            user = await get_user_by_telegram_id(call.from_user.id)
            if not user:
                await call.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            # Extract language from callback data
            new_lang = call.data.replace("client_lang_", "")
            old_lang = user.get('language', 'uz')
            
            # Update user language in database
            await update_user_language(call.from_user.id, new_lang)
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"lang_callback_{call.from_user.id}",
                handler_id=call.from_user.id,
                action="language_changed"
            )
            
            # Update enhanced statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Prepare success message
            success_text = "Til muvaffaqiyatli o'zgartirildi"
            
            # Use edit_and_track for inline cleanup
            await edit_and_track(
                message=call.message,
                text=success_text,
                reply_markup=get_main_menu_keyboard(new_lang)
            )
            
            # Track new message for cleanup
            await inline_message_manager.track(call.from_user.id, call.message.message_id)
            
            # Clear state
            await state.clear()
            
            # Answer callback
            await call.answer()
            
            # Log successful language change
            await audit_logger.log_user_action(
                user_id=call.from_user.id,
                action="language_changed",
                details={
                    "old_language": old_lang,
                    "new_language": new_lang,
                    "role": "client"
                }
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"lang_callback_{call.from_user.id}",
                user_id=call.from_user.id,
                notes="Language change callback completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="language_change_callback_error",
                description=f"Error in handle_language_change_callback: {str(e)}",
                severity="error"
            )
            error_text = "Xatolik yuz berdi"
            await call.answer(error_text, show_alert=True)

    async def show_language_selection(message: Message, lang: str, role: str = 'client'):
        """Show language selection"""
        try:
            # Start enhanced time tracking for language selection display
            await time_tracker.start_role_tracking(
                request_id=f"show_lang_{message.from_user.id}",
                user_id=message.from_user.id,
                role=role,
                workflow_stage="language_selection_shown"
            )
            
            # Track workflow transition for language selection display
            await workflow_manager.track_workflow_transition(
                request_id=f"show_lang_{message.from_user.id}",
                from_role="main_menu",
                to_role="language_selection",
                user_id=message.from_user.id,
                notes='Showing language selection options'
            )
            
            text = "Tilni tanlang:"
            
            # Use send_and_track for inline cleanup
            sent_message = await send_and_track(
                message=message,
                text=text,
                reply_markup=get_language_keyboard(role)
            )
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"show_lang_{message.from_user.id}",
                handler_id=message.from_user.id,
                action="language_selection_shown"
            )
            
            # Log language selection display
            await audit_logger.log_user_action(
                user_id=message.from_user.id,
                action="language_selection_shown",
                details={"role": role, "current_language": lang}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"show_lang_{message.from_user.id}",
                user_id=message.from_user.id,
                notes="Language selection display completed"
            )
            
            return sent_message
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="show_language_selection_error",
                description=f"Error in show_language_selection: {str(e)}",
                severity="error"
            )
            # Fallback to original method
            text = "Tilni tanlang:"
            sent_message = await message.answer(
                text,
                reply_markup=get_language_keyboard(role)
            )
            return sent_message

    return router
