"""
Controller uchun zayavka yaratish handleri
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.controller_states import ControllerApplicationStates
from filters.role_filter import RoleFilter
from keyboards.controllers_buttons import (
    get_application_creator_keyboard,
    get_client_selection_keyboard,
    get_priority_selection_keyboard
)

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller'
    }

async def get_user_lang(user_id: int) -> str:
    """Mock user language"""
    return 'uz'

# Removed duplicate get_role_router - using centralized version from utils.role_system

async def search_clients_by_phone(phone: str, db):
    """Mock search clients by phone"""
    return [
        {
            'id': 1,
            'full_name': 'Test Client 1',
            'phone': phone
        },
        {
            'id': 2,
            'full_name': 'Test Client 2',
            'phone': phone
        }
    ]

async def search_clients_by_name(name: str, db):
    """Mock search clients by name"""
    return [
        {
            'id': 1,
            'full_name': name,
            'phone': '+998901234567'
        }
    ]

async def create_controller_application(controller_id: int, client_id: int, application_type: str, description: str, location: str, priority: str, pool):
    """Mock create controller application"""
    return {
        'success': True,
        'request_id': f'REQ_{controller_id}_{client_id}_{priority.upper()}'
    }

def get_controller_application_creator_router():
    """Get controller application creator router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def start_connection_application(message: Message, state: FSMContext):
        """Ulanish arizasi yaratishni boshlash"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return

            lang = user.get('language', 'uz')
            await state.set_state(ControllerApplicationStates.selecting_client_search_method)
            await state.update_data(application_type='connection_request', controller_id=user['id'])

            prompt_text = (
                "🔌 <b>Ulanish arizasi yaratish</b>\n\n"
                "Mijozni qanday qidirishni xohlaysiz?"
            )

            keyboard = get_application_creator_keyboard(lang)

            await message.answer(
                prompt_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["🔧 Texnik xizmat arizasi yaratish"]))
    async def start_technical_application(message: Message, state: FSMContext):
        """Texnik xizmat arizasi yaratishni boshlash"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return

            lang = user.get('language', 'uz')
            await state.set_state(ControllerApplicationStates.selecting_client_search_method)
            await state.update_data(application_type='technical_service', controller_id=user['id'])

            prompt_text = (
                "🔧 <b>Texnik xizmat arizasi yaratish</b>\n\n"
                "Mijozni qanday qidirishni xohlaysiz?"
            )

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📱 Telefon",
                        callback_data="ctrl_search_phone"
                    ),
                    InlineKeyboardButton(
                        text="👤 Ism",
                        callback_data="ctrl_search_name"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🆔 ID",
                        callback_data="ctrl_search_id"
                    ),
                    InlineKeyboardButton(
                        text="➕ Yangi mijoz",
                        callback_data="ctrl_search_new"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Bekor qilish",
                        callback_data="ctrl_cancel_creation"
                    )
                ]
            ])

            await message.answer(
                prompt_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    # Callback handlers
    @router.callback_query(F.data == "ctrl_search_phone")
    async def search_by_phone(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            lang = user.get('language', 'uz')

            await state.set_state(ControllerApplicationStates.entering_phone)
            
            prompt_text = (
                "📱 <b>Telefon raqamini kiriting:</b>\n\n"
                "Masalan: +998901234567"
            )

            await callback.message.edit_text(
                prompt_text,
                parse_mode='HTML'
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ctrl_search_name")
    async def search_by_name(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            lang = user.get('language', 'uz')

            await state.set_state(ControllerApplicationStates.entering_name)
            
            prompt_text = (
                "👤 <b>Mijoz ismini kiriting:</b>\n\n"
                "Masalan: Alisher Karimov"
            )

            await callback.message.edit_text(
                prompt_text,
                parse_mode='HTML'
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ctrl_search_id")
    async def search_by_id(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            lang = user.get('language', 'uz')

            await state.set_state(ControllerApplicationStates.entering_client_id)
            
            prompt_text = (
                "🆔 <b>Mijoz ID sini kiriting:</b>\n\n"
                "Masalan: 12345"
            )

            await callback.message.edit_text(
                prompt_text,
                parse_mode='HTML'
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ctrl_search_new")
    async def create_new_client(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            lang = user.get('language', 'uz')

            await state.set_state(ControllerApplicationStates.entering_new_client_name)
            
            prompt_text = (
                "➕ <b>Yangi mijoz yaratish</b>\n\n"
                "Mijozning to'liq ismini kiriting:"
            )

            await callback.message.edit_text(
                prompt_text,
                parse_mode='HTML'
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "ctrl_cancel_creation")
    async def cancel_creation(callback: CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            lang = user.get('language', 'uz')

            await state.clear()
            
            cancel_text = (
                "❌ <b>Zayavka yaratish bekor qilindi</b>"
            )

            await callback.message.edit_text(
                cancel_text,
                parse_mode='HTML'
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Text input handlers
    @router.message(ControllerApplicationStates.entering_phone)
    async def process_phone_search(message: Message, state: FSMContext):
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            lang = user.get('language', 'uz')
            phone = message.text.strip()

            clients = await search_clients_by_phone(phone, None)
            
            if not clients:
                not_found_text = (
                    f"📱 Telefon raqami {phone} bo'yicha mijoz topilmadi.\n\n"
                    "Yangi mijoz yaratishni xohlaysizmi?"
                )

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="➕ Yangi mijoz yaratish",
                            callback_data="ctrl_create_new_with_phone"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🔍 Boshqa qidirish",
                            callback_data="ctrl_search_again"
                        )
                    ]
                ])

                await state.update_data(search_phone=phone)
                await message.answer(
                    not_found_text,
                    reply_markup=keyboard
                )
                return

            # Mijozlar topildi
            await state.update_data(found_clients=clients)
            await state.set_state(ControllerApplicationStates.selecting_client)

            select_text = (
                f"📱 {phone} bo'yicha {len(clients)} ta mijoz topildi:\n\n"
                "Kerakli mijozni tanlang:"
            )

            keyboard_buttons = []
            for i, client in enumerate(clients[:5]):  # Maksimal 5 ta
                button_text = f"{client['full_name']} - {client.get('phone', 'N/A')}"
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text=button_text,
                        callback_data=f"ctrl_select_client_{i}"
                    )
                ])

            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="ctrl_cancel_creation"
                )
            ])

            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            await message.answer(
                select_text,
                reply_markup=keyboard
            )

        except Exception as e:
            error_text = "Qidirishda xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(ControllerApplicationStates.entering_name)
    async def process_name_search(message: Message, state: FSMContext):
        user = await get_user_by_telegram_id(message.from_user.id)
        lang = user.get('language', 'uz')
        name = message.text.strip()

        try:
            clients = await search_clients_by_name(name, None)
            
            if not clients:
                not_found_text = (
                    f"👤 '{name}' ismli mijoz topilmadi.\n\n"
                    "Yangi mijoz yaratishni xohlaysizmi?"
                )

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="➕ Yangi mijoz yaratish",
                            callback_data="ctrl_create_new_with_name"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🔍 Boshqa qidirish",
                            callback_data="ctrl_search_again"
                        )
                    ]
                ])

                await state.update_data(search_name=name)
                await message.answer(not_found_text, reply_markup=keyboard)
                return

            # Mijozlar topildi
            await state.update_data(found_clients=clients)
            await state.set_state(ControllerApplicationStates.selecting_client)

            select_text = (
                f"👤 '{name}' bo'yicha {len(clients)} ta mijoz topildi:\n\n"
                "Kerakli mijozni tanlang:"
            )

            keyboard_buttons = []
            for i, client in enumerate(clients[:5]):
                button_text = f"{client['full_name']} - {client.get('phone', 'N/A')}"
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text=button_text,
                        callback_data=f"ctrl_select_client_{i}"
                    )
                ])

            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="ctrl_cancel_creation"
                )
            ])

            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            await message.answer(select_text, reply_markup=keyboard)

        except Exception as e:
            error_text = "Qidirishda xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(lambda c: c.data.startswith("ctrl_select_client_"))
    async def select_client(callback: CallbackQuery, state: FSMContext):
        user = await get_user_by_telegram_id(callback.from_user.id)
        lang = user.get('language', 'uz')
        
        client_index = int(callback.data.split("_")[-1])
        data = await state.get_data()
        clients = data.get('found_clients', [])
        
        if client_index >= len(clients):
            await callback.answer("Xatolik yuz berdi", show_alert=True)
            return
        
        selected_client = clients[client_index]
        await state.update_data(selected_client=selected_client)
        await state.set_state(ControllerApplicationStates.entering_description)
        
        prompt_text = (
            f"✅ <b>Tanlangan mijoz:</b> {selected_client['full_name']}\n"
            f"📱 <b>Telefon:</b> {selected_client.get('phone', 'N/A')}\n\n"
            "📝 <b>Zayavka tavsifini kiriting:</b>"
        )
        
        await callback.message.edit_text(prompt_text, parse_mode='HTML')
        await callback.answer()

    @router.message(ControllerApplicationStates.entering_description)
    async def process_description(message: Message, state: FSMContext):
        user = await get_user_by_telegram_id(message.from_user.id)
        lang = user.get('language', 'uz')
        description = message.text.strip()
        
        await state.update_data(description=description)
        await state.set_state(ControllerApplicationStates.entering_location)
        
        prompt_text = (
            "📍 <b>Manzilni kiriting:</b>\n\n"
            "Masalan: Toshkent sh., Yunusobod t., 5-mavze, 10-uy"
        )
        
        await message.answer(prompt_text, parse_mode='HTML')

    @router.message(ControllerApplicationStates.entering_location)
    async def process_location(message: Message, state: FSMContext):
        user = await get_user_by_telegram_id(message.from_user.id)
        lang = user.get('language', 'uz')
        location = message.text.strip()
        
        await state.update_data(location=location)
        await state.set_state(ControllerApplicationStates.selecting_priority)
        
        prompt_text = (
            "⚡ <b>Muhimlik darajasini tanlang:</b>"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟢 Past",
                    callback_data="ctrl_priority_low"
                ),
                InlineKeyboardButton(
                    text="🟡 O'rta",
                    callback_data="ctrl_priority_medium"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🟠 Yuqori",
                    callback_data="ctrl_priority_high"
                ),
                InlineKeyboardButton(
                    text="🔴 Shoshilinch",
                    callback_data="ctrl_priority_urgent"
                )
            ]
        ])
        
        await message.answer(prompt_text, reply_markup=keyboard, parse_mode='HTML')

    @router.callback_query(lambda c: c.data.startswith("ctrl_priority_"))
    async def select_priority(callback: CallbackQuery, state: FSMContext):
        user = await get_user_by_telegram_id(callback.from_user.id)
        lang = user.get('language', 'uz')
        
        priority = callback.data.split("_")[-1]
        data = await state.get_data()
        
        # Zayavka yaratish
        try:
            result = await create_controller_application(
                controller_id=data['controller_id'],
                client_id=data['selected_client']['id'],
                application_type=data['application_type'],
                description=data['description'],
                location=data['location'],
                priority=priority,
                pool=None
            )
            
            if result['success']:
                success_text = (
                    f"✅ <b>Zayavka muvaffaqiyatli yaratildi!</b>\n\n"
                    f"🆔 <b>ID:</b> {result['request_id']}\n"
                    f"👤 <b>Mijoz:</b> {data['selected_client']['full_name']}\n"
                    f"📝 <b>Tavsif:</b> {data['description']}\n"
                    f"📍 <b>Manzil:</b> {data['location']}\n"
                    f"⚡ <b>Muhimlik:</b> {priority}\n\n"
                    "Zayavka junior menejerga yuborildi."
                )
                
                await callback.message.edit_text(success_text, parse_mode='HTML')
                await state.clear()
            else:
                error_text = (
                    f"❌ <b>Xatolik yuz berdi:</b>\n{result['message']}"
                )
                
                await callback.message.edit_text(error_text, parse_mode='HTML')
                
        except Exception as e:
            error_text = "Zayavka yaratishda xatolik yuz berdi"
            await callback.message.edit_text(error_text)
        
        await callback.answer()

    return router