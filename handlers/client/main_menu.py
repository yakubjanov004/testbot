from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_main_menu_keyboard
from states.client_states import MainMenuStates
from utils.role_system import get_role_router
from aiogram.filters import StateFilter

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

async def get_user_role(user_id: int) -> str:
    """Mock get user role"""
    return 'client'

def get_client_main_menu_router():
    router = get_role_router("client")

    @router.message(F.text.in_(["🏠 Asosiy menyu", "🏠 Главное меню"]))
    async def main_menu_handler(message: Message, state: FSMContext):
        """Client main menu handler with enhanced workflow tracking"""
        try:
            # Rate limiting check
            if not await rate_limiter.check_rate_limit(f"main_menu_{message.from_user.id}", 10, 60):
                lang = await get_user_lang(message.from_user.id)
                error_text = "Iltimos, biroz kutib turing." if lang == 'uz' else "Пожалуйста, подождите немного."
                await message.answer(error_text)
                return
            
            # Start enhanced time tracking for main menu access
            await time_tracker.start_role_tracking(
                request_id=f"main_menu_{message.from_user.id}",
                user_id=message.from_user.id,
                role='client',
                workflow_stage="main_menu_accessed"
            )
            
            # Track workflow transition for main menu access
            await workflow_manager.track_workflow_transition(
                request_id=f"main_menu_{message.from_user.id}",
                from_role="client_start",
                to_role="main_menu",
                user_id=message.from_user.id,
                notes='Client accessing main menu'
            )
            
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            main_menu_text = (
                "Quyidagi menyudan kerakli bo'limni tanlang."
                if lang == 'uz' else
                "Выберите нужный раздел из меню ниже."
            )
            
            # Use send_and_track for inline cleanup
            sent_message = await send_and_track(
                message=message,
                text=main_menu_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.update_data(last_message_id=sent_message.message_id)  # Message_id saqlash
            await state.set_state(MainMenuStates.main_menu)
            
            # Track application handling
            await application_tracker.track_application_handling(
                application_id=f"main_menu_{message.from_user.id}",
                handler_id=message.from_user.id,
                action="main_menu_accessed"
            )
            
            # Update enhanced statistics
            await statistics_manager.generate_role_based_statistics('client', 'daily')
            
            # Log main menu access
            await audit_logger.log_user_action(
                user_id=message.from_user.id,
                action="main_menu_accessed",
                details={"role": "client", "language": lang}
            )
            
            # End enhanced time tracking
            await time_tracker.end_role_tracking(
                request_id=f"main_menu_{message.from_user.id}",
                user_id=message.from_user.id,
                notes="Main menu access completed successfully"
            )
            
        except Exception as e:
            await audit_logger.log_system_event(
                event_type="main_menu_error",
                description=f"Error in main_menu_handler: {str(e)}",
                severity="error"
            )
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка"
            await message.answer(error_text)

    return router
