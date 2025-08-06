"""
Junior Manager Client Search - Simplified Implementation

This module handles junior manager client search functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.junior_manager_buttons import get_client_search_keyboard, get_junior_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def search_clients(query: str):
    """Mock search clients"""
    # Mock client data
    all_clients = [
        {
            'id': 1,
            'full_name': 'Aziz Karimov',
            'phone': '+998901234567',
            'email': 'aziz@example.com',
            'address': 'Tashkent, Chorsu',
            'created_at': datetime.now(),
            'total_applications': 3,
            'last_application': '2024-01-15'
        },
        {
            'id': 2,
            'full_name': 'Malika Toshmatova',
            'phone': '+998901234568',
            'email': 'malika@example.com',
            'address': 'Tashkent, Yunusabad',
            'created_at': datetime.now(),
            'total_applications': 1,
            'last_application': '2024-01-14'
        },
        {
            'id': 3,
            'full_name': 'Jahongir Azimov',
            'phone': '+998901234569',
            'email': 'jahongir@example.com',
            'address': 'Tashkent, Sergeli',
            'created_at': datetime.now(),
            'total_applications': 5,
            'last_application': '2024-01-16'
        }
    ]
    
    # Simple search logic
    query_lower = query.lower()
    results = []
    
    for client in all_clients:
        if (query_lower in client['full_name'].lower() or
            query_lower in client['phone'].lower() or
            query_lower in client['email'].lower() or
            query_lower in client['address'].lower()):
            results.append(client)
    
    return results

def get_client_search_router():
    """Router for client search functionality"""
    router = Router()

    @router.message(F.text.in_(["🔍 Mijoz qidiruv", "🔍 Поиск клиентов"]))
    async def view_client_search(message: Message, state: FSMContext):
        """Junior manager view client search handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return
            
            lang = user.get('language', 'uz')
            
            search_text = (
                "🔍 <b>Mijoz qidiruv - To'liq ma'lumot</b>\n\n"
                "📋 <b>Qidirish mumkin bo'lgan ma'lumotlar:</b>\n"
                "• Mijoz ismi va familiyasi\n"
                "• Telefon raqami\n"
                "• Email manzili\n"
                "• Manzil va hudud\n\n"
                "Qidiruv so'zini kiriting:"
                if lang == 'uz' else
                "🔍 <b>Поиск клиентов - Полная информация</b>\n\n"
                "📋 <b>Информация для поиска:</b>\n"
                "• Имя и фамилия клиента\n"
                "• Номер телефона\n"
                "• Email адрес\n"
                "• Адрес и регион\n\n"
                "Введите поисковый запрос:"
            )
            
            sent_message = await message.answer(
                text=search_text,
                reply_markup=get_client_search_keyboard(lang),
                parse_mode='HTML'
            )
            
            await state.set_state("waiting_for_search_query")
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(lambda message: message.text and len(message.text) > 2)
    async def handle_search_query(message: Message, state: FSMContext):
        """Handle search query"""
        try:
            current_state = await state.get_state()
            if current_state != "waiting_for_search_query":
                return
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return
            
            # Perform search
            search_results = await search_clients(message.text)
            
            if not search_results:
                no_results_text = (
                    f"📭 '{message.text}' bo'yicha natija topilmadi.\n\n"
                    f"Boshqa so'z bilan qidirib ko'ring."
                    if user.get('language', 'uz') == 'uz' else
                    f"📭 По запросу '{message.text}' ничего не найдено.\n\n"
                    f"Попробуйте поиск с другими словами."
                )
                
                await message.answer(
                    text=no_results_text,
                    reply_markup=get_junior_manager_back_keyboard(user.get('language', 'uz'))
                )
                return
            
            # Show first result
            await show_client_details(message, search_results[0], search_results, 0, message.text)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_client_details(message_or_callback, client, clients, index, query):
        """Show client details with navigation"""
        try:
            # Format date
            created_date = client['created_at'].strftime('%d.%m.%Y')
            
            # To'liq ma'lumot
            text = (
                f"👤 <b>Mijoz ma'lumotlari - To'liq ma'lumot</b>\n\n"
                f"🔎 <b>Qidiruv so'zi:</b> {query}\n"
                f"🆔 <b>Mijoz ID:</b> {client['id']}\n"
                f"👤 <b>To'liq ism:</b> {client['full_name']}\n"
                f"📞 <b>Telefon:</b> {client['phone']}\n"
                f"📧 <b>Email:</b> {client['email']}\n"
                f"🏠 <b>Manzil:</b> {client['address']}\n"
                f"📅 <b>Ro'yxatdan o'tgan:</b> {created_date}\n"
                f"📊 <b>Jami arizalar:</b> {client['total_applications']}\n"
                f"📅 <b>Oxirgi ariza:</b> {client['last_application']}\n\n"
                f"📊 <b>Mijoz #{index + 1} / {len(clients)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_clients_navigation_keyboard(index, len(clients))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "client_prev")
    async def show_previous_client(callback: CallbackQuery, state: FSMContext):
        """Show previous client"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_client_index', 0)
            
            # Get search results from state
            search_data = await state.get_data()
            search_results = search_data.get('search_results', [])
            query = search_data.get('search_query', '')
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_client_index=new_index)
                await show_client_details(callback, search_results[new_index], search_results, new_index, query)
            else:
                await callback.answer("Bu birinchi mijoz")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "client_next")
    async def show_next_client(callback: CallbackQuery, state: FSMContext):
        """Show next client"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_client_index', 0)
            
            # Get search results from state
            search_data = await state.get_data()
            search_results = search_data.get('search_results', [])
            query = search_data.get('search_query', '')
            
            if current_index < len(search_results) - 1:
                new_index = current_index + 1
                await state.update_data(current_client_index=new_index)
                await show_client_details(callback, search_results[new_index], search_results, new_index, query)
            else:
                await callback.answer("Bu oxirgi mijoz")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

def get_clients_navigation_keyboard(current_index: int, total_clients: int):
    """Create navigation keyboard for clients"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="client_prev"
        ))
    
    # Next button
    if current_index < total_clients - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="client_next"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 

def get_junior_manager_client_search_router():
    """Get junior manager client search router - alias for get_client_search_router"""
    return get_client_search_router() 