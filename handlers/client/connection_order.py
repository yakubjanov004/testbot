"""
Client Connection Order Handler - Simplified Implementation

This module handles connection order creation for clients.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from datetime import datetime
from keyboards.client_buttons import (
    zayavka_type_keyboard, geolocation_keyboard, confirmation_keyboard
)
from states.client_states import ConnectionOrderStates

def get_connection_order_router():
    router = Router()

    @router.message(F.text.in_(["🔌 Ulanish uchun ariza"]))
    async def start_connection_order(message: Message, state: FSMContext):
        """Yangi ulanish uchun ariza jarayonini boshlash"""
        try:
            # Hududni so'rash
            await message.answer(
                "Hududni tanlang:",
                reply_markup=get_regions_keyboard()
            )
            
            await state.set_state(ConnectionOrderStates.selecting_region)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("region_"), StateFilter(ConnectionOrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            region = callback.data.split("_")[-1]
            await state.update_data(region=region)
            
            # Ulanish turini so'rash
            await callback.message.answer(
                "Ulanish turini tanlang:",
                reply_markup=zayavka_type_keyboard('uz')
            )
            
            await state.set_state(ConnectionOrderStates.selecting_connection_type)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(ConnectionOrderStates.selecting_connection_type))
    async def select_connection_type(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            connection_type = callback.data.split("_")[-1]
            await state.update_data(connection_type=connection_type)
            
            # Tarifni so'rash
            await callback.message.answer(
                "Tarifni tanlang:",
                reply_markup=get_tariff_keyboard()
            )
            
            await state.set_state(ConnectionOrderStates.selecting_tariff)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.in_(["tariff_standard", "tariff_new"]))
    async def select_tariff(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            tariff = callback.data.split("_")[-1]
            await state.update_data(tariff=tariff)
            
            # Manzilni so'rash
            await callback.message.answer(
                "Manzilni kiriting:",
                reply_markup=get_back_keyboard()
            )
            
            await state.set_state(ConnectionOrderStates.entering_address)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(ConnectionOrderStates.entering_address))
    async def get_connection_address(message: Message, state: FSMContext):
        try:
            address = message.text
            await state.update_data(address=address)
            
            # Geolokatsiya so'rash
            await message.answer(
                "Geolokatsiyani yuborishni xohlaysizmi?",
                reply_markup=geolocation_keyboard('uz')
            )
            
            await state.set_state(ConnectionOrderStates.asking_for_geo)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(ConnectionOrderStates.asking_for_geo))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            if callback.data == "send_location_yes":
                await callback.message.answer("📍 Geolokatsiyani yuboring:")
                await state.set_state(ConnectionOrderStates.waiting_for_geo)
            else:
                await finish_connection_order(callback, state)
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(ConnectionOrderStates.waiting_for_geo), F.location)
    async def get_geo(message: Message, state: FSMContext):
        try:
            geo = f"{message.location.latitude}, {message.location.longitude}"
            await state.update_data(geo=geo)
            await finish_connection_order(message, state, geo)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def finish_connection_order(message_or_callback, state: FSMContext, geo=None):
        """Finish connection order and show confirmation"""
        try:
            data = await state.get_data()
            
            # Generate order ID
            order_id = f"UL_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Format confirmation message
            region_names = {
                'tashkent': 'Toshkent shahri',
                'tashkent_viloyat': 'Toshkent viloyati',
                'andijon': 'Andijon',
                'fargona': 'Farg\'ona',
                'namangan': 'Namangan',
                'samarqand': 'Samarqand',
                'buxoro': 'Buxoro',
                'navoiy': 'Navoiy',
                'qashqadaryo': 'Qashqadaryo',
                'surxondaryo': 'Surxondaryo',
                'jizzax': 'Jizzax',
                'sirdaryo': 'Sirdaryo',
                'xorazm': 'Xorazm',
                'qoraqalpogiston': 'Qoraqalpog\'iston'
            }
            
            connection_types = {
                'home': 'Uy interneti',
                'office': 'Ofis interneti',
                'business': 'Biznes interneti'
            }
            
            tariffs = {
                'standard': 'Standart tarif',
                'new': 'Yangi tarif'
            }
            
            confirmation_text = f"""
🔌 **Yangi Ulanish Arizi #{order_id}**

📋 **Ma'lumotlar:**
• Hudud: {region_names.get(data.get('region', 'N/A'), 'N/A')}
• Tur: {connection_types.get(data.get('connection_type', 'N/A'), 'N/A')}
• Tarif: {tariffs.get(data.get('tariff', 'N/A'), 'N/A')}

📍 **Manzil:**
{data.get('address', 'N/A')}

"""
            
            if geo:
                confirmation_text += f"📍 **Geolokatsiya:** {geo}\n"
            
            confirmation_text += f"""
📅 **Sana:** {datetime.now().strftime('%d.%m.%Y %H:%M')}
👤 **Mijoz:** {message_or_callback.from_user.full_name}
📞 **Telefon:** +998901234567

Arizani tasdiqlaysizmi?
"""
            
            await message_or_callback.answer(
                confirmation_text,
                reply_markup=confirmation_keyboard('uz'),
                parse_mode="Markdown"
            )
            
            await state.set_state(ConnectionOrderStates.confirming_connection)
            
        except Exception as e:
            await message_or_callback.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "confirm_zayavka", StateFilter(ConnectionOrderStates.confirming_connection))
    async def confirm_connection_order(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            data = await state.get_data()
            order_id = f"UL_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Send to group
            group_message = f"""
🔌 **Yangi Ulanish Arizi #{order_id}**

👤 **Mijoz:** {callback.from_user.full_name}
📞 **Telefon:** +998901234567
📍 **Hudud:** {data.get('region', 'N/A')}
🏠 **Manzil:** {data.get('address', 'N/A')}
🔧 **Tur:** {data.get('connection_type', 'N/A')}
💳 **Tarif:** {data.get('tariff', 'N/A')}
📅 **Sana:** {datetime.now().strftime('%d.%m.%Y %H:%M')}

✅ **Ariza qabul qilindi va guruhga yuborildi**
"""
            
            await callback.message.edit_text(
                group_message,
                parse_mode="Markdown"
            )
            
            await state.clear()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

def get_regions_keyboard():
    """Get regions keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="Toshkent shahri", callback_data="region_tashkent")],
        [InlineKeyboardButton(text="Toshkent viloyati", callback_data="region_tashkent_viloyat")],
        [InlineKeyboardButton(text="Andijon", callback_data="region_andijon")],
        [InlineKeyboardButton(text="Farg'ona", callback_data="region_fargona")],
        [InlineKeyboardButton(text="Namangan", callback_data="region_namangan")],
        [InlineKeyboardButton(text="Samarqand", callback_data="region_samarqand")],
        [InlineKeyboardButton(text="Buxoro", callback_data="region_buxoro")],
        [InlineKeyboardButton(text="Navoiy", callback_data="region_navoiy")],
        [InlineKeyboardButton(text="Qashqadaryo", callback_data="region_qashqadaryo")],
        [InlineKeyboardButton(text="Surxondaryo", callback_data="region_surxondaryo")],
        [InlineKeyboardButton(text="Jizzax", callback_data="region_jizzax")],
        [InlineKeyboardButton(text="Sirdaryo", callback_data="region_sirdaryo")],
        [InlineKeyboardButton(text="Xorazm", callback_data="region_xorazm")],
        [InlineKeyboardButton(text="Qoraqalpog'iston", callback_data="region_qoraqalpogiston")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_tariff_keyboard():
    """Get tariff keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="Standart tarif", callback_data="tariff_standard")],
        [InlineKeyboardButton(text="Yangi tarif", callback_data="tariff_new")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_keyboard():
    """Get back keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

    return router
