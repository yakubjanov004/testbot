"""
Controller Technicians Handler
Manages technicians for controller
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from filters.role_filter import RoleFilter

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
    """Mock get user language"""
    return 'uz'

async def get_all_technicians():
    """Mock get all technicians"""
    return [
        {
            'id': 1,
            'full_name': 'Aziz Karimov',
            'role': 'technician',
            'status': 'active',
            'phone': '+998901234567',
            'email': 'aziz@example.com',
            'specialization': 'Internet xizmati',
            'active_orders': 3,
            'completed_today': 2,
            'avg_rating': 4.8,
            'experience_years': 3
        },
        {
            'id': 2,
            'full_name': 'Malika Yusupova',
            'role': 'technician',
            'status': 'active',
            'phone': '+998901234568',
            'email': 'malika@example.com',
            'specialization': 'TV xizmati',
            'active_orders': 1,
            'completed_today': 3,
            'avg_rating': 4.6,
            'experience_years': 2
        },
        {
            'id': 3,
            'full_name': 'Bekzod Toirov',
            'role': 'technician',
            'status': 'inactive',
            'phone': '+998901234569',
            'email': 'bekzod@example.com',
            'specialization': 'Texnik xizmat',
            'active_orders': 0,
            'completed_today': 1,
            'avg_rating': 4.4,
            'experience_years': 1
        }
    ]

async def get_technician_details(technician_id: int):
    """Mock get technician details"""
    return {
        'id': technician_id,
        'full_name': f'Test Technician {technician_id}',
        'role': 'technician',
        'status': 'active',
        'phone': '+998901234567',
        'email': f'tech{technician_id}@example.com',
        'specialization': 'Internet xizmati',
        'active_orders': 2,
        'completed_today': 1,
        'avg_rating': 4.5,
        'experience_years': 2
    }

async def update_technician_status(technician_id: int, new_status: bool):
    """Mock update technician status"""
    return True

def technicians_menu(lang: str):
    """Create technicians menu"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Barcha texniklar", callback_data="all_technicians"),
            InlineKeyboardButton(text="🟢 Faol texniklar", callback_data="active_technicians")
        ],
        [
            InlineKeyboardButton(text="🔴 Inaktiv texniklar", callback_data="inactive_technicians"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="technicians_stats")
        ],
        [
            InlineKeyboardButton(text="➕ Yangi texnik", callback_data="add_technician"),
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_controllers")
        ]
    ])

def technician_assignment_keyboard(technicians: list, lang: str):
    """Create technician assignment keyboard"""
    keyboard_buttons = []
    for tech in technicians[:8]:  # Max 8 technicians
        status_emoji = "🟢" if tech['status'] == 'active' else "🔴"
        button_text = f"{status_emoji} {tech['full_name']} ({tech['active_orders']})"
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"technician:{tech['id']}"
            )
        ])
    
    keyboard_buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_technicians")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

def controllers_main_menu(lang: str):
    """Create controllers main menu"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_controllers")]
    ])

def get_controller_technicians_router():
    """Get controller technicians router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["👨‍🔧 Texniklar"]))
    async def show_technicians(message: Message, state: FSMContext):
        """Handle show technicians"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            technicians = await get_all_technicians()
            
            if not technicians:
                no_technicians_text = "👨‍🔧 Hozircha texniklar mavjud emas."
                await message.answer(no_technicians_text)
                return
            
            # Calculate statistics
            total_technicians = len(technicians)
            active_technicians = len([t for t in technicians if t['status'] == 'active'])
            inactive_technicians = len([t for t in technicians if t['status'] == 'inactive'])
            total_active_orders = sum(t['active_orders'] for t in technicians)
            total_completed_today = sum(t['completed_today'] for t in technicians)
            
            technicians_text = (
                "👨‍🔧 <b>Texniklar</b>\n\n"
                "📊 <b>Umumiy statistika:</b>\n"
                f"• Jami texniklar: {total_technicians}\n"
                f"• Faol texniklar: {active_technicians}\n"
                f"• Inaktiv texniklar: {inactive_technicians}\n"
                f"• Faol buyurtmalar: {total_active_orders}\n"
                f"• Bugun bajarilgan: {total_completed_today}\n\n"
                "Kerakli bo'limni tanlang:"
            )
            
            await message.answer(
                technicians_text,
                reply_markup=technicians_menu(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in show_technicians: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

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
📱 Telefon: {technician['phone']}
📍 Manzil: {technician['email']}
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
                await update_technician_status(technician_id, not technician['status'] == 'active')
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
                status_emoji = "🟢" if tech['status'] == 'active' else "🔴"
                text += f"\n{status_emoji} {tech['full_name']} ({tech['phone']})"
            
            await callback.message.edit_text(
                text,
                reply_markup=controllers_main_menu(lang)
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in back_to_technicians: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router
