from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_contact_keyboard
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

async def get_user_lang(user_id: int) -> str:
    """Mock get user language"""
    return 'uz'

async def send_and_track(message: Message, text: str, reply_markup=None):
    """Mock send and track"""
    return await message.answer(text, reply_markup=reply_markup)

async def edit_and_track(message: Message, text: str, reply_markup=None):
    """Mock edit and track"""
    return await message.edit_text(text, reply_markup=reply_markup)

async def answer_and_cleanup(callback: CallbackQuery, text: str = None):
    """Mock answer and cleanup"""
    await callback.answer(text)

def get_client_contact_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["📞 Aloqa", "📞 Контакты"]))
    async def client_contact_handler(message: Message, state: FSMContext):
        """Client contact handler with enhanced workflow tracking"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"client_contact_{message.from_user.id}", 5, 60):
                await message.answer("Iltimos, biroz kutib turing.")
                return
            
            # Start enhanced time tracking for contact access
            await time_tracker.start_role_tracking(
                request_id=f"client_contact_{message.from_user.id}",
                user_id=message.from_user.id,
                role='client',
                workflow_stage="contact_accessed"
            )
            
            # Track workflow transition for contact access
            await workflow_manager.track_workflow_transition(
                request_id=f"client_contact_{message.from_user.id}",
                from_role="main_menu",
                to_role="contact",
                user_id=message.from_user.id,
                notes='Client accessing contact section'
            )
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            lang = user.get('language', 'uz')
            contact_text = (
                "Aloqa ma'lumotlari:"
                if lang == 'uz' else
                "Контактная информация:"
            )
            
            # Use send_and_track for inline cleanup
            sent_message = await send_and_track(
                message=message,
                text=contact_text,
                reply_markup=get_contact_keyboard(lang)
            )
            
            await state.set_state(ContactStates.contact_menu)
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"client_contact_{message.from_user.id}",
                handler_id=message.from_user.id,
                action="contact_accessed"
            )
            
            # Update enhanced statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log contact access
            await audit_logger.log_user_action(
                user_id=message.from_user.id,
                action="contact_accessed",
                details={"language": lang}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"client_contact_{message.from_user.id}",
                user_id=message.from_user.id,
                notes="Contact access completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="client_contact_handler_error",
                description=f"Error in client_contact_handler: {str(e)}",
                severity="error"
            )
            await message.answer("Xatolik yuz berdi")

    return router
