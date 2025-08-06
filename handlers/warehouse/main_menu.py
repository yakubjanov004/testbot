from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.warehouse_states import WarehouseMainMenuStates

def get_warehouse_main_menu_router():
    """Warehouse main menu router - Simplified Implementation"""
    router = Router()

    @router.message(F.text == "📦 Ombor")
    async def warehouse_start(message: Message, state: FSMContext):
        """Warehouse main menu handler"""
        try:
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = """
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, Warehouse xodimi!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 Inventar", callback_data="warehouse_inventory")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="warehouse_orders")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="warehouse_statistics")],
                [InlineKeyboardButton(text="📥 Inbox", callback_data="warehouse_inbox")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="warehouse_language")]
            ])
            
            await message.answer(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "/start")
    async def warehouse_start_command(message: Message, state: FSMContext):
        """Warehouse start command handler"""
        try:
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = """
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, Warehouse xodimi!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 Inventar", callback_data="warehouse_inventory")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="warehouse_orders")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="warehouse_statistics")],
                [InlineKeyboardButton(text="📥 Inbox", callback_data="warehouse_inbox")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="warehouse_language")]
            ])
            
            await message.answer(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "warehouse_main_menu")
    async def warehouse_main_menu_callback(callback: CallbackQuery, state: FSMContext):
        """Return to warehouse main menu"""
        try:
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = """
🏢 <b>Warehouse Panel</b>

👤 Warehouse xodimi
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 Inventar", callback_data="warehouse_inventory")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="warehouse_orders")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="warehouse_statistics")],
                [InlineKeyboardButton(text="📥 Inbox", callback_data="warehouse_inbox")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="warehouse_language")]
            ])
            
            await callback.message.edit_text(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "warehouse_back")
    async def warehouse_back_handler(callback: CallbackQuery, state: FSMContext):
        """Go back to warehouse main menu"""
        try:
            await warehouse_main_menu_callback(callback, state)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "🌐 Tilni o'zgartirish")
    async def change_language_handler(message: Message, state: FSMContext):
        """Language change handler for warehouse"""
        try:
            lang_text = "🌐 Tilni tanlang:"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="warehouse_lang_uz")],
                [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="warehouse_lang_ru")],
                [InlineKeyboardButton(text="🇬🇧 English", callback_data="warehouse_lang_en")]
            ])
            
            await message.answer(lang_text, reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("warehouse_lang_"))
    async def set_language_callback(callback: CallbackQuery, state: FSMContext):
        """Set language callback"""
        try:
            new_lang = callback.data.replace("warehouse_lang_", "")
            
            success_text = "✅ Til muvaffaqiyatli o'zgartirildi!"
            await callback.answer(success_text, show_alert=True)
            
            await warehouse_main_menu_callback(callback, state)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "🏠 Bosh sahifa")
    async def warehouse_home_handler(message: Message, state: FSMContext):
        """Warehouse home handler"""
        try:
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = """
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, Warehouse xodimi!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📦 Inventar", callback_data="warehouse_inventory")],
                [InlineKeyboardButton(text="📋 Buyurtmalar", callback_data="warehouse_orders")],
                [InlineKeyboardButton(text="📊 Statistika", callback_data="warehouse_statistics")],
                [InlineKeyboardButton(text="📥 Inbox", callback_data="warehouse_inbox")],
                [InlineKeyboardButton(text="🌐 Tilni o'zgartirish", callback_data="warehouse_language")]
            ])
            
            await message.answer(welcome_text.strip(), parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "ℹ️ Yordam")
    async def warehouse_help_handler(message: Message, state: FSMContext):
        """Warehouse help handler"""
        try:
            help_text = """
ℹ️ <b>Warehouse Yordam</b>

📋 <b>Asosiy funksiyalar:</b>
• 📦 Inventar boshqaruvi
• 📋 Buyurtmalar ko'rish
• 📊 Statistika va hisobotlar
• 📥 Yangi so'rovlarni ko'rish
• ✅ Tayyor bo'lgan so'rovlarni yuborish

📞 <b>Qo'llab-quvvatlash:</b>
Agar muammo bo'lsa, administrator bilan bog'laning.

🔧 <b>Texnik yordam:</b>
Sistemada muammo bo'lsa, texnik xizmat bilan bog'laning.
            """
            
            await message.answer(help_text.strip(), parse_mode='HTML')
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    return router
