"""
Start Handler - Database Implementation

This module handles the /start command and initial user registration
using the real database.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

# Import database service
from database.service import DatabaseService
from database.models import UserRole

logger = logging.getLogger(__name__)

# States for registration
class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_language = State()

def get_start_router():
    router = Router()
    
    @router.message(Command("start"))
    async def start_handler(message: Message, state: FSMContext):
        """Handle /start command"""
        try:
            user_id = message.from_user.id
            username = message.from_user.username
            full_name = message.from_user.full_name
            
            # Get or create user in database
            user = await DatabaseService.get_or_create_user(
                telegram_id=user_id,
                username=username,
                full_name=full_name
            )
            
            # Clear any existing state
            await state.clear()
            
            # Check if user needs to complete registration
            if not user.phone_number:
                # Start registration process
                await state.set_state(RegistrationStates.waiting_for_phone)
                
                text = (
                    f"Assalomu alaykum, {full_name}! 🎉\n\n"
                    "AlfaConnect tizimiga xush kelibsiz!\n\n"
                    "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring:\n"
                    "(Format: +998901234567)"
                )
                
                # Create phone number request button
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="📱 Telefon raqamni yuborish",
                        callback_data="request_phone"
                    )]
                ])
                
                await message.answer(text, reply_markup=keyboard)
            else:
                # User already registered, show main menu based on role
                await show_main_menu(message, user)
                
        except Exception as e:
            logger.error(f"Error in start handler: {e}")
            await message.answer(
                "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.\n"
                "/start buyrug'ini qayta yuboring."
            )
    
    @router.message(RegistrationStates.waiting_for_phone)
    async def process_phone(message: Message, state: FSMContext):
        """Process phone number input"""
        try:
            phone = message.text.strip()
            
            # Validate phone number
            if not phone.startswith('+998') or len(phone) != 13:
                await message.answer(
                    "❌ Noto'g'ri telefon raqam formati!\n"
                    "Iltimos, +998901234567 formatida yuboring."
                )
                return
            
            # Update user phone number
            user = await DatabaseService.update_user(
                telegram_id=message.from_user.id,
                phone_number=phone
            )
            
            if user:
                # Ask for language preference
                await state.set_state(RegistrationStates.waiting_for_language)
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
                        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
                    ]
                ])
                
                await message.answer(
                    "Tilni tanlang / Выберите язык:",
                    reply_markup=keyboard
                )
            else:
                await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")
                
        except Exception as e:
            logger.error(f"Error processing phone: {e}")
            await message.answer("❌ Xatolik yuz berdi.")
    
    @router.callback_query(F.data.startswith("lang_"))
    async def process_language(callback: CallbackQuery, state: FSMContext):
        """Process language selection"""
        try:
            language = callback.data.split("_")[1]
            
            # Update user language
            user = await DatabaseService.update_user(
                telegram_id=callback.from_user.id,
                language=language
            )
            
            if user:
                # Clear state
                await state.clear()
                
                # Send success message
                success_text = {
                    'uz': "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!\n\nEndi tizimdan foydalanishingiz mumkin.",
                    'ru': "✅ Вы успешно зарегистрированы!\n\nТеперь вы можете использовать систему."
                }
                
                await callback.message.edit_text(success_text.get(language, success_text['uz']))
                
                # Show main menu
                await show_main_menu(callback.message, user)
            else:
                await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error processing language: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    async def show_main_menu(message: Message, user):
        """Show main menu based on user role"""
        try:
            # Get role-specific menu text
            role_menus = {
                UserRole.ADMIN: "👨‍💼 Admin Panel",
                UserRole.MANAGER: "📊 Manager Dashboard",
                UserRole.JUNIOR_MANAGER: "📋 Junior Manager Panel",
                UserRole.CONTROLLER: "🎮 Controller Dashboard",
                UserRole.TECHNICIAN: "🔧 Technician Panel",
                UserRole.CALL_CENTER: "☎️ Call Center Dashboard",
                UserRole.CALL_CENTER_SUPERVISOR: "📞 Call Center Supervisor Panel",
                UserRole.CLIENT: "🏠 Asosiy Menyu"
            }
            
            menu_title = role_menus.get(user.role, "🏠 Asosiy Menyu")
            
            text = f"{menu_title}\n\n"
            text += f"👤 Foydalanuvchi: {user.full_name}\n"
            text += f"📱 Telefon: {user.phone_number}\n"
            text += f"🔑 Rol: {user.role.value}\n\n"
            text += "Kerakli bo'limni tanlang:"
            
            # Create role-specific keyboard
            keyboard = create_role_keyboard(user.role, user.language)
            
            await message.answer(text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error showing main menu: {e}")
            await message.answer("❌ Menyu yuklanmadi")
    
    def create_role_keyboard(role: UserRole, language: str):
        """Create role-specific keyboard"""
        keyboards = {
            UserRole.CLIENT: InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔌 Ulanish uchun ariza", callback_data="connection_request")],
                [InlineKeyboardButton(text="🔧 Texnik xizmat", callback_data="technical_service")],
                [InlineKeyboardButton(text="📋 Mening arizalarim", callback_data="my_applications")],
                [InlineKeyboardButton(text="📞 Aloqa", callback_data="contact")],
                [InlineKeyboardButton(text="ℹ️ Yordam", callback_data="help")]
            ]),
            UserRole.MANAGER: InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📊 Arizalar", callback_data="applications")],
                [InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="users")],
                [InlineKeyboardButton(text="📈 Statistika", callback_data="statistics")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="orders")],
                [InlineKeyboardButton(text="🔔 Xabarnomalar", callback_data="notifications")]
            ]),
            UserRole.TECHNICIAN: InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📋 Mening buyurtmalarim", callback_data="my_orders")],
                [InlineKeyboardButton(text="🗺 Xarita", callback_data="map")],
                [InlineKeyboardButton(text="📊 Hisobotlar", callback_data="reports")],
                [InlineKeyboardButton(text="🔔 Xabarnomalar", callback_data="notifications")]
            ])
        }
        
        # Return appropriate keyboard or default
        return keyboards.get(role, InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Asosiy menyu", callback_data="main_menu")]
        ]))
    
    return router 