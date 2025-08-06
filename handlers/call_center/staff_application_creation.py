"""
Call Center Staff Application Creation Handler

This module implements application creation handlers for Call Center role,
allowing call center operators to create both connection requests and technical service
applications on behalf of clients during phone calls.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

# States imports
from states.staff_application_states import StaffApplicationStates

# Keyboard imports
from keyboards.call_center_buttons import call_center_main_menu_reply

def get_call_center_staff_application_creation_router():
    """Get router for call center staff application creation handlers"""
    router = Router(name="call_center_staff_application")
    
    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish", "🔌 Создать заявку на подключение"]))
    async def call_center_create_connection_request(message: Message, state: FSMContext):
        """Handle call center creating connection request for client"""
        lang = 'uz'  # Default language
        
        # Mock application creation start
        await state.update_data(
            creator_context={'role': 'call_center', 'id': 123},
            application_type='connection_request'
        )
        
        await state.set_state(StaffApplicationStates.selecting_client_search_method)
        
        prompt_text = (
            "📞 Call Center: Ulanish arizasi yaratish\n\n"
            "Mijoz bilan telefon orqali gaplashayotgan vaqtda ariza yaratish.\n\n"
            "Mijozni qanday qidirishni xohlaysiz?\n\n"
            "📱 Telefon raqami bo'yicha\n"
            "👤 Ism bo'yicha\n"
            "🆔 Mijoz ID bo'yicha\n"
            "➕ Yangi mijoz qo'shish"
        )
        
        await message.answer(prompt_text)

    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish", "🔧 Создать техническую заявку"]))
    async def call_center_create_technical_service(message: Message, state: FSMContext):
        """Handle call center creating technical service request for client"""
        lang = 'uz'  # Default language
        
        # Mock application creation start
        await state.update_data(
            creator_context={'role': 'call_center', 'id': 123},
            application_type='technical_service'
        )
        
        await state.set_state(StaffApplicationStates.selecting_client_search_method)
        
        prompt_text = (
            "🔧 Call Center: Texnik xizmat arizasi yaratish\n\n"
            "Mijoz bilan telefon orqali gaplashayotgan vaqtda texnik xizmat arizasi yaratish.\n\n"
            "Mijozni qanday qidirishni xohlaysiz?\n\n"
            "📱 Telefon raqami bo'yicha\n"
            "👤 Ism bo'yicha\n"
            "🆔 Mijoz ID bo'yicha\n"
            "➕ Yangi mijoz qo'shish"
        )
        
        await message.answer(prompt_text)

    @router.callback_query(F.data.startswith("cc_client_search_"))
    async def handle_call_center_client_search_method(callback: CallbackQuery, state: FSMContext):
        """Handle call center client search method selection"""
        await callback.answer()
        
        search_method = callback.data.replace("cc_client_search_", "")
        lang = 'uz'  # Default language
        
        if search_method == "phone":
            await state.set_state(StaffApplicationStates.entering_client_phone)
            prompt_text = (
                "📱 Mijoz telefon raqamini kiriting:\n\n"
                "Masalan: +998 90 123 45 67"
            )
            await callback.message.edit_text(prompt_text)
            
        elif search_method == "name":
            await state.set_state(StaffApplicationStates.entering_client_name)
            prompt_text = (
                "👤 Mijoz ismini kiriting:\n\n"
                "Masalan: Ahmad Karimov"
            )
            await callback.message.edit_text(prompt_text)
            
        elif search_method == "id":
            await state.set_state(StaffApplicationStates.entering_client_id)
            prompt_text = (
                "🆔 Mijoz ID ni kiriting:\n\n"
                "Masalan: CL123456"
            )
            await callback.message.edit_text(prompt_text)
            
        elif search_method == "new":
            # Mock new client creation
            await state.set_state(StaffApplicationStates.entering_client_name)
            prompt_text = (
                "➕ Yangi mijoz qo'shish\n\n"
                "Mijoz to'liq ismini kiriting:"
            )
            await callback.message.edit_text(prompt_text)

    @router.callback_query(F.data == "cc_cancel_application_creation")
    async def call_center_cancel_application_creation(callback: CallbackQuery, state: FSMContext):
        """Handle call center canceling application creation"""
        await callback.answer()
        
        lang = 'uz'  # Default language
        
        cancel_text = (
            "❌ Ariza yaratish bekor qilindi.\n\n"
            "Bosh sahifaga qaytdingiz."
        )
        
        await callback.message.edit_text(cancel_text)
        await state.clear()

    @router.message(StaffApplicationStates.entering_client_phone)
    async def handle_call_center_client_phone_input(message: Message, state: FSMContext):
        """Handle call center client phone input"""
        phone = message.text.strip()
        
        if not phone:
            await message.answer("Iltimos, telefon raqamini kiriting.")
            return
        
        # Mock client found
        await state.update_data(client_phone=phone)
        
        success_text = (
            f"✅ Mijoz topildi!\n\n"
            f"📱 Telefon: {phone}\n"
            f"👤 Ism: Ahmad Karimov\n"
            f"🆔 ID: CL123456\n\n"
            f"Ariza yaratish davom etadi..."
        )
        
        await message.answer(success_text)
        await state.set_state(StaffApplicationStates.application_created)

    @router.message(StaffApplicationStates.entering_client_name)
    async def handle_call_center_client_name_input(message: Message, state: FSMContext):
        """Handle call center client name input"""
        name = message.text.strip()
        
        if not name:
            await message.answer("Iltimos, mijoz ismini kiriting.")
            return
        
        # Mock client found
        await state.update_data(client_name=name)
        
        success_text = (
            f"✅ Mijoz topildi!\n\n"
            f"👤 Ism: {name}\n"
            f"📱 Telefon: +998 90 123 45 67\n"
            f"🆔 ID: CL123456\n\n"
            f"Ariza yaratish davom etadi..."
        )
        
        await message.answer(success_text)
        await state.set_state(StaffApplicationStates.application_created)

    @router.message(StaffApplicationStates.entering_client_id)
    async def handle_call_center_client_id_input(message: Message, state: FSMContext):
        """Handle call center client ID input"""
        client_id = message.text.strip()
        
        if not client_id:
            await message.answer("Iltimos, mijoz ID ni kiriting.")
            return
        
        # Mock client found
        await state.update_data(client_id=client_id)
        
        success_text = (
            f"✅ Mijoz topildi!\n\n"
            f"🆔 ID: {client_id}\n"
            f"👤 Ism: Ahmad Karimov\n"
            f"📱 Telefon: +998 90 123 45 67\n\n"
            f"Ariza yaratish davom etadi..."
        )
        
        await message.answer(success_text)
        await state.set_state(StaffApplicationStates.application_created)

    return router
