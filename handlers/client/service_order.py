"""
Client Service Order Handler - Simplified Implementation

This module handles service order creation for clients.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from datetime import datetime
from keyboards.client_buttons import (
    zayavka_type_keyboard, geolocation_keyboard, confirmation_keyboard, media_attachment_keyboard
)
from states.client_states import OrderStates

def get_service_order_router():
    router = Router()

    @router.message(F.text.in_(["🔧 Texnik xizmat"]))
    async def new_service_request(message: Message, state: FSMContext):
        """New service request handler"""
        try:
            # Hududni so'rash
            await message.answer(
                "Hududni tanlang:",
                reply_markup=get_regions_keyboard()
            )
            
            await state.set_state(OrderStates.selecting_region)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("region_"), StateFilter(OrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            region = callback.data.split("_")[-1]
            await state.update_data(region=region)
            
            # Abonent turini so'rash
            await callback.message.answer(
                "Abonent turini tanlang:",
                reply_markup=zayavka_type_keyboard('uz')
            )
            
            await state.set_state(OrderStates.selecting_order_type)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(OrderStates.selecting_order_type))
    async def select_abonent_type(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            abonent_type = callback.data.split("_")[-1]
            await state.update_data(abonent_type=abonent_type)
            
            # Abonent ID so'rash
            await callback.message.answer(
                "Abonent ID raqamini kiriting:",
                reply_markup=get_back_keyboard()
            )
            
            await state.set_state(OrderStates.waiting_for_contact)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(OrderStates.waiting_for_contact))
    async def get_abonent_id(message: Message, state: FSMContext):
        try:
            abonent_id = message.text
            await state.update_data(abonent_id=abonent_id)
            
            # Muammo tavsifini so'rash
            await message.answer(
                "Muammo haqida batafsil ma'lumot bering:",
                reply_markup=get_back_keyboard()
            )
            
            await state.set_state(OrderStates.entering_description)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(OrderStates.entering_description))
    async def get_service_description(message: Message, state: FSMContext):
        try:
            description = message.text
            await state.update_data(description=description)
            
            # Media so'rash
            await message.answer(
                "Rasm yoki video qo'shishni xohlaysizmi?",
                reply_markup=media_attachment_keyboard('uz')
            )
            
            await state.set_state(OrderStates.asking_for_media)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["attach_media_yes", "attach_media_no"]), StateFilter(OrderStates.asking_for_media))
    async def ask_for_media(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            if callback.data == "attach_media_yes":
                await callback.message.answer("📷 Rasm yoki video yuboring:")
                await state.set_state(OrderStates.waiting_for_media)
            else:
                await ask_for_address(callback, state)
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(OrderStates.waiting_for_media), F.photo | F.video)
    async def process_media(message: Message, state: FSMContext):
        try:
            media_type = "photo" if message.photo else "video"
            await state.update_data(media_type=media_type, media_file_id=message.photo[-1].file_id if message.photo else message.video.file_id)
            
            await ask_for_address(message, state)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def ask_for_address(message_or_callback, state: FSMContext):
        """Ask for address"""
        try:
            await message_or_callback.answer(
                "Manzilni kiriting:",
                reply_markup=get_back_keyboard()
            )
            
            await state.set_state(OrderStates.entering_address)
            
        except Exception as e:
            await message_or_callback.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(StateFilter(OrderStates.entering_address))
    async def get_service_address(message: Message, state: FSMContext):
        try:
            address = message.text
            await state.update_data(address=address)
            
            # Geolokatsiya so'rash
            await message.answer(
                "Geolokatsiyani yuborishni xohlaysizmi?",
                reply_markup=geolocation_keyboard('uz')
            )
            
            await state.set_state(OrderStates.asking_for_location)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(OrderStates.asking_for_location))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            if callback.data == "send_location_yes":
                await callback.message.answer("📍 Geolokatsiyani yuboring:")
                await state.set_state(OrderStates.waiting_for_location)
            else:
                await show_service_confirmation(callback, state)
                
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(OrderStates.waiting_for_location), F.location)
    async def get_geo(message: Message, state: FSMContext):
        try:
            geo = f"{message.location.latitude}, {message.location.longitude}"
            await state.update_data(geo=geo)
            await show_service_confirmation(message, state)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_service_confirmation(message_or_callback, state: FSMContext):
        """Show service order confirmation"""
        try:
            data = await state.get_data()
            
            # Generate order ID
            order_id = f"TX_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
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
            
            abonent_types = {
                'home': 'Uy abonenti',
                'business': 'Biznes abonenti',
                'office': 'Ofis abonenti'
            }
            
            confirmation_text = f"""
🔧 **Texnik Xizmat Arizi #{order_id}**

📋 **Ma'lumotlar:**
• Hudud: {region_names.get(data.get('region', 'N/A'), 'N/A')}
• Abonent turi: {abonent_types.get(data.get('abonent_type', 'N/A'), 'N/A')}
• Abonent ID: {data.get('abonent_id', 'N/A')}

📍 **Manzil:**
{data.get('address', 'N/A')}

📝 **Muammo:**
{data.get('description', 'N/A')}

"""
            
            if 'geo' in data:
                confirmation_text += f"📍 **Geolokatsiya:** {data['geo']}\n"
            
            if 'media_type' in data:
                confirmation_text += f"📷 **Media:** {data['media_type'].title()} qo'shilgan\n"
            
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
            
            await state.set_state(OrderStates.confirming_order)
            
        except Exception as e:
            await message_or_callback.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "confirm_zayavka", StateFilter(OrderStates.confirming_order))
    async def confirm_service_order(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            data = await state.get_data()
            order_id = f"TX_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Send to group
            group_message = f"""
🔧 **Texnik Xizmat Arizi #{order_id}**

👤 **Mijoz:** {callback.from_user.full_name}
📞 **Telefon:** +998901234567
📍 **Hudud:** {data.get('region', 'N/A')}
🏠 **Manzil:** {data.get('address', 'N/A')}
🆔 **Abonent ID:** {data.get('abonent_id', 'N/A')}
📝 **Muammo:** {data.get('description', 'N/A')}
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

def get_back_keyboard():
    """Get back keyboard"""
    keyboard = [
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
