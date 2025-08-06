import json
from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.technician_buttons import get_technician_main_menu_keyboard, get_back_technician_keyboard
from states.technician_states import TechnicianMainMenuStates, TechnicianWorkflowStates

async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'technician',
        'language': 'uz',
        'full_name': 'Test Technician',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

def get_technician_inbox_router():
    """Technician inbox router"""
    from utils.role_system import get_role_router
    router = get_role_router("technician")

    @router.message(F.text == "📥 Inbox")
    @router.callback_query(F.data == "technician_inbox")
    async def show_technician_inbox(event: Message | CallbackQuery, state: FSMContext) -> None:
        """Show technician's inbox with assigned requests"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': event.from_user.id,
                'role': 'technician',
                'language': 'uz',
                'full_name': 'Test Technician'
            }
            
            # Mock inbox data
            zayavkalar = [
                {
                    'id': '12345',
                    'public_id': 'REQ-001',
                    'client_name': 'Test Client',
                    'client_phone': '+998901234567',
                    'description': 'Internet ulanish muammosi',
                    'address': 'Toshkent shahri, Chilonzor tumani',
                    'current_status': 'assigned_to_technician',
                    'created_at': datetime.now(),
                    'priority': 'high'
                },
                {
                    'id': '12346',
                    'public_id': 'REQ-002',
                    'client_name': 'Test Client 2',
                    'client_phone': '+998901234568',
                    'description': 'Televizor signal muammosi',
                    'address': 'Toshkent shahri, Sergeli tumani',
                    'current_status': 'in_progress',
                    'created_at': datetime.now(),
                    'priority': 'normal'
                }
            ]
            
            if not zayavkalar:
                msg = "📭 Sizga biriktirilgan zayavkalar yo'q."
                return await send_or_edit(event, msg, state=state)

            # Prioritize returned requests
            returned = [z for z in zayavkalar if z.get('current_status') == 'returned_to_technician']
            in_progress = [z for z in zayavkalar if z.get('current_status') == 'in_progress']
            assigned = [z for z in zayavkalar if z.get('current_status') == 'assigned_to_technician']
            
            if returned:
                await state.update_data(zayavkalar=returned, current_index=0, only_in_progress=False)
                await show_current_zayavka(event, state, 0, user.get('language', 'uz'))
                return
            if in_progress:
                await state.update_data(zayavkalar=in_progress, current_index=0, only_in_progress=True)
                await show_current_zayavka(event, state, 0, user.get('language', 'uz'))
                return
            await state.update_data(zayavkalar=assigned, current_index=0, only_in_progress=False)
            await show_current_zayavka(event, state, 0, user.get('language', 'uz'))
            
        except Exception as e:
            error_msg = "❌ Xatolik yuz berdi"
            await send_and_track(
                event.answer if hasattr(event, 'answer') else event.message.answer,
                error_msg,
                event.from_user.id
            )

    async def send_or_edit(
        event: Message | CallbackQuery,
        text: str,
        *,
        state: FSMContext,
        **kwargs
    ) -> int:
        """Send a new message or edit existing one"""
        if hasattr(event, 'chat'):
            chat_id = event.chat.id
        elif hasattr(event, 'message') and hasattr(event.message, 'chat'):
            chat_id = event.message.chat.id
        else:
            chat_id = event.from_user.id
            
        data = await state.get_data()
        message_id = data.get("current_message_id")

        if not message_id:
            message = await event.bot.send_message(chat_id=chat_id, text=text, **kwargs)
            await state.update_data(current_message_id=message.message_id)
            return message.message_id

        try:
            await event.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                **kwargs
            )
            return message_id
        except Exception as e:
            try:
                await event.bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass
            
            message = await event.bot.send_message(chat_id=chat_id, text=text, **kwargs)
            await state.update_data(current_message_id=message.message_id)
            return message.message_id

    async def send_and_track(event, text, user_id):
        """Mock send and track function"""
        if hasattr(event, 'answer'):
            await event.answer(text)
        else:
            await event.answer(text)

    async def show_current_zayavka(
        event: Message | CallbackQuery, 
        state: FSMContext, 
        index: int, 
        lang: str
    ) -> None:
        """Show current zayavka details"""
        try:
            data = await state.get_data()
            zayavkalar = data.get('zayavkalar', [])
            only_in_progress = data.get('only_in_progress', False)
            
            if not zayavkalar or index < 0 or index >= len(zayavkalar):
                return await send_or_edit(
                    event, 
                    "📭 Zayavka topilmadi.",
                    state=state
                )

            z = zayavkalar[index]
            created_at = z.get('created_at', '').strftime('%d.%m.%Y %H:%M') if z.get('created_at') else 'N/A'
            desc = z.get('description', 'Tavsif yo\'q')
            status = z.get('status') or z.get('current_status', 'new')
            address = z.get('address', 'Manzil ko\'rsatilmagan')
            client_phone = z.get('client_phone', 'Telefon ko\'rsatilmagan')

            # Status emojis
            emoji = {
                'new': '🆕',
                'assigned_to_technician': '🧑‍🔧',
                'in_progress': '🔧',
                'completed': '✅'
            }.get(status, 'ℹ️')

            # Comments count (mock)
            comments_count = 2

            text = (
                f"{emoji} <b>Zayavka #{z.get('public_id', z.get('id', 'N/A'))}</b>\n"
                f"👤 <b>Mijoz:</b> {z.get('client_name', 'Noma\'lum')}\n"
                f"📞 <b>Telefon:</b> {client_phone}\n"
                f"📍 <b>Manzil:</b> {address}\n"
                f"📄 <b>Tavsif:</b> {desc[:100]}{'...' if len(desc) > 100 else ''}\n"
                f"📅 <b>Yaratilgan:</b> {created_at}\n"
                f"💬 <b>Izohlar:</b> {comments_count} ta"
            )

            request_id = z.get('id')
            public_id = z.get('public_id', z.get('id', 'None'))
            
            # Inline tugmalar
            buttons = []
            
            # Add comment button
            buttons.append([
                InlineKeyboardButton(
                    text="💬 Izoh qo'shish",
                    callback_data=f"tech_add_comment_{request_id}"
                )
            ])
            
            # Add detailed view button
            buttons.append([
                InlineKeyboardButton(
                    text="🔍 Batafsil",
                    callback_data=f"tech_view_{request_id}"
                )
            ])
            
            if status == 'returned_to_technician':
                buttons.append([
                    InlineKeyboardButton(text="Materiallarni qayta tanlash", callback_data=f"tech_wh_yes_{public_id}")
                ])
            
            if request_id:
                if status == 'assigned_to_technician' or status == 'in_progress':
                    buttons.append([
                        InlineKeyboardButton(
                            text="📝 Diagnostika qo'yish",
                            callback_data=f"tech_set_diagnosis_{request_id}"
                        )
                    ])
            
            # Navigatsiya tugmalari
            if len(zayavkalar) > 1 and not only_in_progress and status != 'returned_to_technician':
                buttons.append([
                    InlineKeyboardButton(text="⬅️ Oldingi", callback_data="tech_prev"),
                    InlineKeyboardButton(text="Keyingi ➡️", callback_data="tech_next")
                ])
                
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None
            await send_or_edit(event, text, reply_markup=keyboard, parse_mode="HTML", state=state)
            
        except Exception as e:
            error_msg = "❌ Xatolik yuz berdi"
            await send_and_track(
                event.answer if hasattr(event, 'answer') else event.message.answer,
                error_msg,
                event.from_user.id
            )

    @router.callback_query(F.data == "tech_next")
    async def next_zayavka(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        index = data.get('current_index', 0) + 1
        await state.update_data(current_index=index)
        await show_current_zayavka(callback, state, index, 'uz')

    @router.callback_query(F.data == "tech_prev")
    async def prev_zayavka(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        index = data.get('current_index', 0) - 1
        await state.update_data(current_index=index)
        await show_current_zayavka(callback, state, index, 'uz')

    @router.callback_query(F.data.startswith("tech_view_"))
    async def tech_view_details(callback: CallbackQuery, state: FSMContext):
        request_id = callback.data.replace("tech_view_", "")

        # Mock request details
        z = {
            'id': request_id,
            'client_name': 'Test Client',
            'client_phone': '+998901234567',
            'description': 'Internet ulanish muammosi - signal kuchsiz',
            'address': 'Toshkent shahri, Chilonzor tumani, 15-uy',
            'status': 'in_progress',
            'created_at': datetime.now(),
            'diagnosis': 'Kabel uzilgan'
        }

        created_at = z.get('created_at', '').strftime('%d.%m.%Y %H:%M') if z.get('created_at') else 'Noma\'lum'
        address = z.get('address', 'Manzil ko\'rsatilmagan')

        text = (
            f"🔌 <b>Ariza batafsil ma'lumotlari!</b>\n\n"
            f"📝 <b>ID:</b> {z['id']}\n"
            f"👤 <b>Mijoz:</b> {z.get('client_name', '-')}\n"
            f"📞 <b>Telefon:</b> {z.get('client_phone', '-')}\n"
            f"📍 <b>Manzil:</b> {address}\n"
            f"📄 <b>Ta'rif:</b> {z['description']}\n"
            f"💳 <b>Tarif:</b> Premium\n"
            f"📅 <b>Yaratilgan:</b> {created_at}\n"
            f"🛠 <b>Diagnoz:</b> {z.get('diagnosis', 'Aniqlanmagan')}\n\n"
            f"💬 <b>Izohlar:</b>\n"
            f"1. 🔧 Texnik: Keling, ko'rib chiqamiz\n"
            f"2. 📞 Call Center: Mijoz bilan bog'lanish o'rnatildi"
        )

        buttons = [
            [
                InlineKeyboardButton(text="🔙 Ortga", callback_data="technician_inbox")
            ]
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

    @router.callback_query(F.data == "tech_back_to_menu")
    async def back_to_menu(callback: CallbackQuery, state: FSMContext):
        """Return to main menu"""
        text = "Asosiy menyu"
        await callback.answer(text)
        await state.clear()
        
        await callback.message.answer(
            text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text="📥 Inbox",
                        callback_data="technician_inbox"
                    )
                ]]
            )
        )

    @router.callback_query(F.data.startswith("tech_start_"))
    async def technician_start_work(callback: CallbackQuery, state: FSMContext):
        """Technician starts work on a request"""
        request_id_str = callback.data.replace("tech_start_", "").strip()

        if not request_id_str or request_id_str.lower() == 'none':
            await callback.answer(
                "⚠️ Xatolik: So'rov ID si topilmadi. Iltimos, qaytadan urinib ko'ring.", 
                show_alert=True
            )
            return

        try:
            data = await state.get_data()
            zayavkalar = data.get('zayavkalar', [])
            target_request = next(
                (z for z in zayavkalar if str(z.get('public_id')) == request_id_str), None
            )

            if not target_request:
                await callback.answer(
                    "❗️Zayavka topilmadi (state ichida).",
                    show_alert=True
                )
                return

            await callback.answer("✅ Ish boshlandi!", show_alert=True)
            await show_request_details_for_diagnosis(callback, request_id_str, 'uz', state)

        except Exception as e:
            await callback.answer("⚠️ Xatolik yuz berdi.", show_alert=True)

    async def show_request_details_for_diagnosis(event: Message | CallbackQuery, request_id: str, lang: str, state: FSMContext):
        """Displays the full details of a request and a button to set the diagnosis."""
        # Mock request details
        z = {
            'public_id': request_id,
            'client_name': 'Test Client',
            'client_phone': '+998901234567',
            'description': 'Internet ulanish muammosi',
            'address': 'Toshkent shahri, Chilonzor tumani',
            'status': 'in_progress',
            'created_at': datetime.now()
        }

        created_at = z.get('created_at', '').strftime('%d.%m.%Y %H:%M') if z.get('created_at') else 'N/A'
        details_text = (
            f"📋 <b>Zayavka batafsil ma'lumotlari</b>\n\n"
            f"🆔 <b>ID:</b> {z.get('public_id')}\n"
            f"👤 <b>Mijoz:</b> {z.get('client_name', 'Noma\'lum')}\n"
            f"📞 <b>Telefon:</b> {z.get('client_phone', 'Noma\'lum')}\n"
            f"📄 <b>Ta'rif:</b> {z.get('description', '-')}\n"
            f"📍 <b>Manzil:</b> {z.get('address', 'Ko\'rsatilmagan')}\n"
            f"📊 <b>Status:</b> {z.get('status', '-')}\n"
            f"📅 <b>Yaratilgan:</b> {created_at}"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Diagnostika qo'yish", callback_data=f"tech_set_diagnosis_{request_id}")],
            [InlineKeyboardButton(text="🔙 Ortga", callback_data="technician_inbox")]
        ])

        await send_or_edit(event, details_text, reply_markup=keyboard, parse_mode="HTML", state=state)

    @router.callback_query(F.data.startswith("tech_set_diagnosis_"))
    async def set_diagnosis_handler(callback: CallbackQuery, state: FSMContext):
        request_id = callback.data.replace("tech_set_diagnosis_", "")
        await state.set_state(TechnicianWorkflowStates.waiting_for_diagnosis)
        await state.update_data(current_request_id=request_id)

        await send_or_edit(
            callback, 
            "Diagnostika natijasini matn shaklida yuboring.",
            state=state
        )

    @router.message(TechnicianWorkflowStates.waiting_for_diagnosis, F.text)
    async def process_diagnosis_handler(message: Message, state: FSMContext):
        try:
            data = await state.get_data()
            current_request_id = data.get('current_request_id')
            diagnosis_text = message.text
            
            if not current_request_id:
                await message.answer("Xatolik: Zayavka ID topilmadi.")
                await state.clear()
                return

            # Mock success
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Ha", callback_data=f"tech_wh_yes_{current_request_id}"),
                    InlineKeyboardButton(text="❌ Yo'q", callback_data=f"tech_wh_no_{current_request_id}")
                ]
            ])
            await send_or_edit(
                message,
                "Diagnostika qabul qilindi! Ombor bilan ishlanadimi?",
                reply_markup=keyboard,
                state=state
            )
            await state.set_state(TechnicianWorkflowStates.waiting_for_warehouse_decision)
                
        except Exception as e:
            await message.answer("Xatolik yuz berdi!")
            await state.clear()

    @router.callback_query(TechnicianWorkflowStates.waiting_for_warehouse_decision, F.data.startswith("tech_wh_yes_"))
    async def process_warehouse_yes(callback: CallbackQuery, state: FSMContext):
        request_id = callback.data.replace("tech_wh_yes_", "")

        await state.update_data(
            current_request_id=request_id,
            selected_materials=[],
            warehouse_required=True
        )

        await show_material_list(callback, state, 'uz', preselected=None)
        await callback.answer()

    @router.callback_query(TechnicianWorkflowStates.waiting_for_warehouse_decision, F.data.startswith("tech_wh_no_"))
    async def process_warehouse_no(callback: CallbackQuery, state: FSMContext):
        request_id = callback.data.replace("tech_wh_no_", "")
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ishni yakunlash", callback_data=f"tech_complete_{request_id}")],
            [InlineKeyboardButton(text="📄 Word hujjat", callback_data=f"tech_word_doc_{request_id[:20]}")]
        ])
        await callback.message.edit_text(
            "Ombor kerak emas. Endi ishni yakunlashingiz mumkin.",
            reply_markup=keyboard
        )
        await state.update_data(current_request_id=request_id, warehouse_required=False)
        await callback.answer("Ombor kerak emas!", show_alert=True)

    @router.callback_query(TechnicianWorkflowStates.waiting_for_material_selection, F.data.startswith("tech_select_mat_"))
    async def select_material_handler(callback: CallbackQuery, state: FSMContext):
        """Handles the selection of a material and asks for the quantity."""
        material_id = int(callback.data.replace("tech_select_mat_", ""))
        await state.update_data(selected_material_id=material_id)
        await state.set_state(TechnicianWorkflowStates.waiting_for_material_quantity)

        await callback.message.edit_text(
            "Kerakli miqdorni kiriting:"
        )

    @router.message(TechnicianWorkflowStates.waiting_for_material_quantity, F.text)
    async def process_material_quantity(message: Message, state: FSMContext):
        """Processes the quantity, validates against stock, and asks to add more."""
        if not message.text.isdigit() or int(message.text) <= 0:
            await message.answer("Iltimos, to'g'ri son kiriting.")
            return

        requested_quantity = int(message.text)
        data = await state.get_data()
        material_id = data.get('selected_material_id')

        # Mock validation
        available_quantity = 10
        if requested_quantity > available_quantity:
            await message.answer(
                f"Ushbu materialdan faqat {available_quantity} dona qolgan. Iltimos, kamroq miqdor kiriting."
            )
            return

        # Add the selected material to the list in the state
        selected_materials = data.get('selected_materials', [])
        selected_materials.append({'material_id': material_id, 'quantity': requested_quantity})
        await state.update_data(selected_materials=selected_materials)

        # Ask to add another material or finish
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ Yana qo'shish", callback_data="tech_add_more_mat_yes"),
                InlineKeyboardButton(text="✅ Tugatish", callback_data="tech_add_more_mat_no")
            ]
        ])

        await send_or_edit(
            message,
            "Material qo'shildi. Yana qo'shasizmi?",
            reply_markup=keyboard,
            state=state
        )

    @router.callback_query(F.data == "tech_add_more_mat_yes")
    async def add_another_material_yes(callback: CallbackQuery, state: FSMContext):
        await show_material_list(callback, state, 'uz')

    @router.callback_query(F.data == "tech_add_more_mat_no")
    async def add_another_material_no(callback: CallbackQuery, state: FSMContext):
        """Shows the confirmation list of selected materials with their names."""
        data = await state.get_data()
        selected_materials = data.get('selected_materials', [])

        if not selected_materials:
            await callback.message.edit_text("Hech qanday material tanlanmadi.")
            await state.clear()
            return

        # Mock material details
        material_details = {
            1: {'name': 'Kabel'},
            2: {'name': 'Konnektor'},
            3: {'name': 'Antenna'}
        }

        summary_text = "<b>Tanlangan materiallar:</b>\n"
        for item in selected_materials:
            material_name = material_details.get(item['material_id'], {}).get('name', 'Noma\'lum material')
            summary_text += f"- {material_name}, Miqdori: {item['quantity']}\n"

        await state.set_state(TechnicianWorkflowStates.confirming_materials)
        request_id = data.get('current_request_id')
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"tech_confirm_mats_{request_id}"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="tech_cancel_mats")
            ]
        ])

        await callback.message.edit_text(summary_text, reply_markup=keyboard, parse_mode="HTML")

    @router.callback_query(TechnicianWorkflowStates.confirming_materials, F.data.startswith("tech_confirm_mats_"))
    async def process_material_confirmation(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        request_id = data.get('current_request_id')
        selected_materials = data.get('selected_materials', [])
        
        if not request_id or not selected_materials:
            await callback.message.edit_text("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            await state.clear()
            return
            
        # Mock success
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Zayavkani yakunlash", callback_data=f"tech_final_complete_{request_id}"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="tech_cancel_final")
            ]
        ])
        
        await callback.message.edit_text(
            "✅ Materiallar omborga yuborildi!\n\n"
            "Endi zayavkani yakunlashni xohlaysizmi?",
            reply_markup=keyboard
        )
        await state.clear()

    @router.callback_query(F.data.startswith("tech_final_complete_"))
    async def final_complete_request(callback: CallbackQuery, state: FSMContext):
        """Final completion after sending materials to warehouse"""
        request_id = callback.data.replace("tech_final_complete_", "")
        
        await callback.message.edit_text(
            "✅ Zayavka muvaffaqiyatli yakunlandi!"
        )
        await callback.answer()

    @router.callback_query(F.data == "tech_cancel_final")
    async def cancel_final_completion(callback: CallbackQuery, state: FSMContext):
        """Cancel final completion"""
        await callback.message.edit_text(
            "Zayavka yakunlanmadi. Materiallar omborga yuborildi."
        )
        await callback.answer()

    @router.callback_query(F.data == "tech_cancel_mats")
    async def cancel_material_selection(callback: CallbackQuery, state: FSMContext):
        await callback.message.edit_text("Material tanlash bekor qilindi.")
        await state.clear()

    @router.callback_query(F.data.startswith("tech_add_comment_"))
    async def add_comment_handler(callback: CallbackQuery, state: FSMContext):
        """Handle adding comment for technician"""
        request_id = callback.data.replace("tech_add_comment_", "")

        # Save request ID in state
        await state.update_data(comment_request_id=request_id)
        await state.set_state(TechnicianWorkflowStates.waiting_for_comment)

        prompt_text = "💬 Iltimos, izohingizni yuboring:"
        cancel_text = "❌ Bekor qilish"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=cancel_text, callback_data="tech_cancel_comment")]
        ])

        await callback.message.edit_text(prompt_text, reply_markup=keyboard)
        await callback.answer()

    @router.message(TechnicianWorkflowStates.waiting_for_comment)
    async def process_comment(message: Message, state: FSMContext):
        """Process the comment from technician"""
        comment_text = message.text.strip()
        data = await state.get_data()
        request_id = data.get('comment_request_id')

        if not request_id:
            error_text = "Xatolik: Zayavka topilmadi"
            await message.answer(error_text)
            return

        if not comment_text:
            error_text = "❗️ Izoh bo'sh bo'lishi mumkin emas."
            await message.answer(error_text)
            return

        # Mock success
        success_text = "✅ Izoh muvaffaqiyatli qo'shildi!"
        await message.answer(success_text)

        # Return to inbox
        await show_technician_inbox(message, state)
        await state.clear()

    @router.callback_query(F.data == "tech_cancel_comment")
    async def cancel_comment(callback: CallbackQuery, state: FSMContext):
        """Cancel comment adding"""
        await state.clear()
        await show_technician_inbox(callback, state)
        await callback.answer()

    @router.callback_query(F.data.startswith("tech_word_doc_"))
    async def technician_generate_word(callback: CallbackQuery, state: FSMContext):
        """Generate Word document for technician"""
        try:
            await callback.answer()
            
            # Extract request_id
            request_id = callback.data.replace("tech_word_doc_", "")
            
            await callback.message.answer("📄 Word hujjat yaratilmoqda...")
            
            # Mock success
            await callback.message.answer(
                f"✅ Word hujjat tayyor!\n\nZayavka ID: {request_id}\nTuri: technical_service"
            )
            
        except Exception as e:
            await callback.message.answer(f"Xatolik: {str(e)}")

    @router.callback_query(F.data.startswith("tech_complete_"))
    async def technician_complete(callback: CallbackQuery, state: FSMContext):
        """Texnik ishni yakunlash"""
        request_id = callback.data.replace("tech_complete_", "")
        
        # Request ID ni state'ga saqlash
        await state.update_data(completing_request_id=request_id)
        
        # Service order number so'rash
        await callback.message.answer(
            "📄 Xizmat buyrug'i raqamini kiriting:"
        )
        await state.set_state(TechnicianWorkflowStates.entering_service_order_number)
        await callback.answer()
    
    @router.message(TechnicianWorkflowStates.entering_service_order_number)
    async def get_service_order_number(message: Message, state: FSMContext):
        """Service order number olish va diagnosis so'rash"""
        # Service order number saqlash
        await state.update_data(service_order_number=message.text)
        
        # Diagnosis so'rash
        await message.answer(
            "🔍 Diagnostika natijasini kiriting:"
        )
        await state.set_state(TechnicianWorkflowStates.entering_diagnostics_result)
    
    @router.message(TechnicianWorkflowStates.entering_diagnostics_result)
    async def get_diagnosis_and_complete(message: Message, state: FSMContext):
        """Diagnosis olish va yakunlash"""
        data = await state.get_data()
        request_id = data.get('completing_request_id')
        service_order_number = data.get('service_order_number')
        diagnosis = message.text
        
        await message.answer(
            "✅ Ish muvaffaqiyatli yakunlandi!",
            reply_markup=get_technician_main_menu_keyboard('uz')
        )
        
        # Clear state
        await state.clear()

    # Utility function for showing material list
    async def show_material_list(event: CallbackQuery | Message, state: FSMContext, lang: str, preselected=None):
        """Reusable function to display the list of available materials."""
        # Mock materials
        materials = [
            {'id': 1, 'name': 'Kabel', 'quantity': 50},
            {'id': 2, 'name': 'Konnektor', 'quantity': 100},
            {'id': 3, 'name': 'Antenna', 'quantity': 25}
        ]
        
        if not materials:
            await send_or_edit(event, "Omborda materiallar mavjud emas.", state=state)
            await state.clear()
            return
            
        await state.set_state(TechnicianWorkflowStates.waiting_for_material_selection)
        buttons = []
        for material in materials:
            button_text = f"{material['name']} (Qolgan: {material['quantity']})"
            buttons.append([InlineKeyboardButton(text=button_text, callback_data=f"tech_select_mat_{material['id']}")])
        buttons.append([InlineKeyboardButton(text="🔙 Ortga", callback_data="technician_inbox")])
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await send_or_edit(event, "Kerakli materialni tanlang:", reply_markup=keyboard, state=state)

    return router