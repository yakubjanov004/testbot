"""
Controller handlers for Technicians - Soddalashtirilgan versiya

Bu modul controller uchun texniklarni boshqarish handlerlarini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567'
    }

async def get_user_lang(user_id: int):
    """Mock user language"""
    return 'uz'

# Removed duplicate get_role_router - using centralized version from utils.role_system

async def get_all_technicians():
    """Mock all technicians"""
    return [
        {
            'id': 1,
            'full_name': 'Ahmad Toshmatov',
            'phone_number': '+998901234567',
            'address': 'Tashkent, Chorsu',
            'status': 'Faol',
            'is_active': True
        },
        {
            'id': 2,
            'full_name': 'Bekzod Karimov',
            'phone_number': '+998901234568',
            'address': 'Tashkent, Yunusabad',
            'status': 'Faol',
            'is_active': True
        },
        {
            'id': 3,
            'full_name': 'Dilshod Mirzayev',
            'phone_number': '+998901234569',
            'address': 'Samarkand, Registon',
            'status': 'Nofaol',
            'is_active': False
        }
    ]

async def get_technician_details(technician_id: int):
    """Mock technician details"""
    technicians = await get_all_technicians()
    for tech in technicians:
        if tech['id'] == technician_id:
            return tech
    return None

async def update_technician_status(technician_id: int, new_status: bool):
    """Mock update technician status"""
    return True

# Mock keyboards
def technicians_menu(lang: str):
    """Mock technicians menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Texniklar ro'yxati", callback_data="show_technicians_list"),
            InlineKeyboardButton(text="📊 Samaradorlik", callback_data="show_technicians_performance")
        ],
        [
            InlineKeyboardButton(text="🎯 Vazifa tayinlash", callback_data="task_assignment"),
            InlineKeyboardButton(text="📈 Hisobot", callback_data="technicians_report")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_controllers")
        ]
    ])

def technician_assignment_keyboard(technicians: list, lang: str):
    """Mock technician assignment keyboard"""
    keyboard = []
    
    for tech in technicians:
        if tech['is_active']:
            status_emoji = "🟢" if tech['is_active'] else "🔴"
            button_text = f"{status_emoji} {tech['full_name']}"
            keyboard.append([
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"assign_to_technician_{tech['id']}"
                )
            ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Bekor qilish",
            callback_data="cancel_assignment"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def controllers_main_menu(lang: str):
    """Mock controllers main menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔌 Ulanish arizasi", callback_data="connection_request"),
            InlineKeyboardButton(text="🔧 Texnik xizmat", callback_data="technical_service")
        ],
        [
            InlineKeyboardButton(text="👨‍🔧 Texniklar", callback_data="technicians"),
            InlineKeyboardButton(text="📊 Hisobotlar", callback_data="reports")
        ],
        [
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")
        ]
    ])

def get_controller_technicians_router():
    """Get controller technicians router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["👨‍🔧 Texniklar"]))
    async def show_technicians(message: Message, state: FSMContext):
        """Show the list of technicians as a reply message"""
        try:
            lang = await get_user_lang(message.from_user.id)
            technicians = await get_all_technicians()
            
            if not technicians:
                await message.answer(
                    "Texniklar topilmadi.",
                    reply_markup=controllers_main_menu(lang)
                )
                return
            
            text = "👨‍🔧 Texniklar ro'yxati:\n"
            for tech in technicians:
                status_emoji = "🟢" if tech['is_active'] else "🔴"
                text += f"\n{status_emoji} {tech['full_name']} ({tech['phone_number']})"
            
            await message.answer(text, reply_markup=controllers_main_menu(lang))
            
        except Exception as e:
            print(f"Error in show_technicians: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith('technician:'))
    async def handle_technician_action(callback: CallbackQuery, state: FSMContext):
        """Handle technician-related actions"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            action, technician_id = callback.data.split(':')[1:]
            technician_id = int(technician_id)
            
            # Get technician details
            technician = await get_technician_details(technician_id)
            if not technician:
                await callback.answer("Texnik topilmadi", show_alert=True)
                return
            
            # Handle different actions
            if action == 'view':
                # Show technician details
                details_text = f"""👨‍🔧 <b>Texnik ma'lumotlari</b>

👤 Ism: {technician['full_name']}
📱 Telefon: {technician['phone_number']}
📍 Manzil: {technician['address']}
📊 Status: {technician['status']}"""
                
                # Create a simple details keyboard
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🔄 Status o'zgartirish",
                            callback_data=f"technician:status:{technician_id}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🔙 Orqaga",
                            callback_data="back_to_technicians"
                        )
                    ]
                ])
                await callback.message.edit_text(details_text, reply_markup=keyboard)
            
            elif action == 'status':
                # Update technician status
                await update_technician_status(technician_id, not technician['is_active'])
                await callback.answer("Texnik statusi yangilandi")
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in handle_technician_action: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_technicians")
    async def back_to_technicians(callback: CallbackQuery, state: FSMContext):
        """Go back to technicians menu"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Show technicians list again
            technicians = await get_all_technicians()
            
            if not technicians:
                await callback.message.edit_text(
                    "Texniklar topilmadi.",
                    reply_markup=controllers_main_menu(lang)
                )
                return
            
            text = "👨‍🔧 Texniklar ro'yxati:\n"
            for tech in technicians:
                status_emoji = "🟢" if tech['is_active'] else "🔴"
                text += f"\n{status_emoji} {tech['full_name']} ({tech['phone_number']})"
            
            await callback.message.edit_text(
                text,
                reply_markup=controllers_main_menu(lang)
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in back_to_technicians: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router
