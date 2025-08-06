from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import warehouse_main_menu
from states.warehouse_states import WarehouseMainMenuStates

def get_warehouse_main_menu_router():
    """Warehouse main menu router"""
    from utils.role_system import get_role_router
    router = get_role_router("warehouse")

    @router.message(F.text == "📦 Ombor")
    async def warehouse_start(message: Message, state: FSMContext):
        """Warehouse main menu handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            # Tex.txt bo'yicha warehouse vazifasi
            welcome_text = f"""
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, {user.get('full_name', 'Warehouse xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            await message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=warehouse_main_menu('uz')
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "/start")
    async def warehouse_start_command(message: Message, state: FSMContext):
        """Warehouse start command handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = f"""
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, {user.get('full_name', 'Warehouse xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            await message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=warehouse_main_menu('uz')
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "warehouse_main_menu")
    async def warehouse_main_menu_callback(callback: CallbackQuery, state: FSMContext):
        """Return to warehouse main menu"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = f"""
🏢 <b>Warehouse Panel</b>

👤 {user.get('full_name', 'Warehouse xodimi')}
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            await callback.message.edit_text(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=warehouse_main_menu('uz')
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "warehouse_back")
    async def warehouse_back_handler(callback: CallbackQuery, state: FSMContext):
        """Go back to warehouse main menu"""
        try:
            await warehouse_main_menu_callback(callback, state)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Language change handler
    @router.message(F.text == "🌐 Tilni o'zgartirish")
    async def change_language_handler(message: Message, state: FSMContext):
        """Language change handler for warehouse"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            from keyboards.warehouse_buttons import language_selection_keyboard
            
            lang_text = "🌐 Tilni tanlang:"
            
            await message.answer(
                lang_text,
                reply_markup=language_selection_keyboard()
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("set_language_"))
    async def set_language_callback(callback: CallbackQuery, state: FSMContext):
        """Set language callback"""
        try:
            new_lang = callback.data.split("_")[2]  # uz or ru
            
            # Mock success response (like other modules)
            success_text = "✅ Til muvaffaqiyatli o'zgartirildi!"
            
            await callback.message.edit_text(success_text)
            await callback.answer()
            
            # Return to main menu with new language
            await state.set_state(WarehouseMainMenuStates.main_menu)
            await callback.message.answer(
                "🏢 Warehouse Panel",
                reply_markup=warehouse_main_menu(new_lang)
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "🏠 Bosh sahifa")
    async def warehouse_home_handler(message: Message, state: FSMContext):
        """Warehouse home handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = f"""
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, {user.get('full_name', 'Warehouse xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            await message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=warehouse_main_menu('uz')
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

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
            
            await message.answer(
                help_text.strip(),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    return router

# Mock functions (like other modules)
async def get_warehouse_user_by_telegram_id(telegram_id: int):
    """Get warehouse user by telegram id (mock function like other modules)"""
    try:
        # Mock user data (like other modules)
        return {
            'id': 1,
            'telegram_id': telegram_id,
            'full_name': 'Warehouse xodimi',
            'role': 'warehouse',
            'language': 'uz'
        }
    except Exception as e:
        return None

async def update_warehouse_user_language(user_id: int, language: str):
    """Update warehouse user language (mock function like other modules)"""
    try:
        # Mock update (like other modules)
        return True
    except Exception as e:
        return False

async def get_user_lang(user_id: int):
    """Get user language (mock function like other modules)"""
    try:
        # Mock language (like other modules)
        return 'uz'
    except Exception as e:
        return 'uz'
