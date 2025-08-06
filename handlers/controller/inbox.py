from datetime import datetime
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from states.controller_states import ControllerRequestStates

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

async def get_users_by_role(role: str):
    """Mock users by role"""
    if role == 'technician':
        return [
            {
                'id': 1,
                'full_name': 'Technician 1',
                'role': 'technician',
                'telegram_id': 123456789,
                'active_requests': 0
            },
            {
                'id': 2,
                'full_name': 'Technician 2',
                'role': 'technician',
                'telegram_id': 987654321,
                'active_requests': 2
            }
        ]
    elif role == 'call_center_supervisor':
        return [
            {
                'id': 3,
                'full_name': 'Call Center Supervisor 1',
                'role': 'call_center_supervisor',
                'telegram_id': 111222333
            }
        ]
    return []

async def get_role_router(role: str):
    """Mock role router"""
    return Router()

async def get_user_lang(user_id: int) -> str:
    """Mock user language"""
    return 'uz'

# Mock bot and database
class MockBot:
    async def send_message(self, chat_id, text, **kwargs):
        print(f"MockBot: Sending message to {chat_id}: {text}")
        return True
    async def edit_message_text(self, chat_id, message_id, text, **kwargs):
        print(f"MockBot: Editing message {message_id} in {chat_id}: {text}")
        return True
    async def delete_message(self, chat_id, message_id):
        print(f"MockBot: Deleting message {message_id} in {chat_id}")
        return True

class MockDB:
    async def fetchrow(self, query, *args):
        """Mock database fetchrow"""
        return {
            'full_name': 'Test Technician',
            'phone_number': '+998901234567'
        }
    async def execute(self, query, *args):
        """Mock database execute"""
        print(f"MockDB: Executing query: {query}")
        return True

bot = MockBot()
bot.db = MockDB()

class ControllerRequestStates(StatesGroup):
    waiting_for_technician = State()
    waiting_for_comment = State()

# 1. send_or_edit universal qiladi va message_id qaytaradi
async def send_or_edit(
    event: Message | CallbackQuery,
    text: str,
    *,
    state: FSMContext,
    **kwargs
) -> int:
    data = await state.get_data()
    message_id = data.get("current_message_id")
    chat_id = event.from_user.id

    try:
        if message_id:
            await event.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                **kwargs
            )
            return message_id
        else:
            message = await event.bot.send_message(chat_id=chat_id, text=text, **kwargs)
            await state.update_data(current_message_id=message.message_id)
            return message.message_id
    except Exception as e:
        print(f"Could not edit message {message_id}, sending a new one. Error: {e}")
        try:
            if message_id:
                await event.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as del_e:
            print(f"Error deleting old message {message_id}: {del_e}")
        
        message = await event.bot.send_message(chat_id=chat_id, text=text, **kwargs)
        await state.update_data(current_message_id=message.message_id)
        return message.message_id

def get_controller_inbox_router():
    """Get controller inbox router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")
    
    @router.callback_query(F.data.startswith("open_inbox_"))
    async def handle_inbox_notification(callback: CallbackQuery, state: FSMContext):
        """Handle inbox notification button click"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id_short = callback.data.replace("open_inbox_", "")
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            # Show inbox
            await show_controller_inbox_from_notification(callback.message, state, request_id_short)
            
        except Exception as e:
            print(f"Error handling inbox notification: {e}")
            await callback.answer("Xatolik yuz berdi")
    
    async def show_controller_inbox_from_notification(message: Message, state: FSMContext, target_request_id: str = None):
        """Show controller inbox with focus on specific request"""
        try:
            user = await get_user_by_telegram_id(message.chat.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            
            # Mock inbox messages
            inbox_messages = [
                {
                    'id': 1,
                    'application_id': 'req123456',
                    'message_type': 'new_request'
                },
                {
                    'id': 2,
                    'application_id': 'req789012',
                    'message_type': 'new_request'
                }
            ]
            
            if not inbox_messages:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            # Find target request index if specified
            target_index = 0
            if target_request_id:
                for i, msg in enumerate(inbox_messages):
                    if msg['application_id'].startswith(target_request_id):
                        target_index = i
                        break
            
            # Get full request details
            requests = []
            for msg in inbox_messages:
                try:
                    request_details = {
                        'id': msg['application_id'],
                        'workflow_type': 'connection_request',
                        'client_name': 'Test Client',
                        'client_phone': '+998901234567',
                        'location': 'Test Address',
                        'description': 'Test description',
                        'created_at': datetime.now(),
                        'current_status': 'new',
                        'contact_info': {
                            'phone': '+998901234567',
                            'full_name': 'Test Client'
                        },
                        'state_data': {
                            'selected_tariff': 'Test Tariff'
                        }
                    }
                    request_details['inbox_message'] = msg
                    requests.append(request_details)
                except:
                    pass
            
            if not requests:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            await state.update_data(
                controller_requests=requests,
                current_index=target_index
            )
            
            await display_controller_request(message, state, requests[target_index], target_index, lang)
            
        except Exception as e:
            print(f"Error in show_controller_inbox_from_notification: {e}")

    @router.message(F.text == "📥 Inbox")
    async def show_controller_inbox(event: Message, state: FSMContext):
        user_id = event.from_user.id
        
        try:
            await state.clear()
            await state.update_data(current_page=0)
            # Faqat menyudan bosilganda yangi xabar yuboriladi
            await state.update_data(current_message_id=None)
            await display_inbox_page(event, state)
            
        except Exception as e:
            print(f"Error in show_controller_inbox: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await event.answer(error_text)

    @router.callback_query(F.data == "controller_inbox")
    async def show_controller_inbox_callback(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        # Callback orqali chaqirilganda current_message_id ni o'chirmang!
        await display_inbox_page(callback, state)

    async def display_inbox_page(event: Message | CallbackQuery, state: FSMContext):
        user_id = event.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                error_text = "Sizda ruxsat yo'q."
                await send_or_edit(event, error_text, state=state)
                return

            lang = user.get('language', 'uz')
            
            # Mock requests
            requests = [
                {
                    'id': 'req123456',
                    'workflow_type': 'connection_request',
                    'client_name': 'Test Client 1',
                    'client_phone': '+998901234567',
                    'location': 'Test Address 1',
                    'description': 'Test description 1',
                    'created_at': datetime.now(),
                    'current_status': 'new',
                    'contact_info': {
                        'phone': '+998901234567',
                        'full_name': 'Test Client 1'
                    },
                    'state_data': {
                        'selected_tariff': 'Test Tariff 1'
                    }
                },
                {
                    'id': 'req789012',
                    'workflow_type': 'technical_service',
                    'client_name': 'Test Client 2',
                    'client_phone': '+998901234568',
                    'location': 'Test Address 2',
                    'description': 'Test description 2',
                    'created_at': datetime.now(),
                    'current_status': 'assigned_to_controller',
                    'contact_info': {
                        'phone': '+998901234568',
                        'full_name': 'Test Client 2'
                    },
                    'state_data': {
                        'selected_tariff': 'Test Tariff 2'
                    }
                }
            ]
            
            if not requests:
                no_requests = "📭 Sizga biriktirilgan zayavkalar yo'q."
                await send_or_edit(event, no_requests, state=state)
                return
                
            # Save requests in state and show first one
            await state.update_data(requests=[dict(r) for r in requests], current_idx=0)
            await show_request(event, state, 0, lang)
            
        except Exception as e:
            print(f"Error in controller_inbox: user_id={event.from_user.id}, error={e}")
            error_msg = "Xatolik yuz berdi"
            await send_or_edit(event, error_msg, state=state)

    # Kontroller uchun "batafsil" ko'rinish yo'q, shuning uchun inbox xabarini yangilaymiz
    async def show_request(
        event: Message | CallbackQuery, 
        state: FSMContext, 
        idx: int, 
        lang: str
    ) -> int:
        """Show a single request with navigation controls - simplified view"""
        data = await state.get_data()
        requests = data.get('requests', [])
        
        if not requests or idx < 0 or idx >= len(requests):
            msg_id = await send_or_edit(event, "📭 Zayavkalar topilmadi.", state=state)
            await state.update_data(current_message_id=msg_id)
            return msg_id
            
        request_id = requests[idx]['id']
        request = requests[idx]
        
        if not request:
            msg_id = await send_or_edit(event, "📭 Zayavka topilmadi.", state=state)
            await state.update_data(current_message_id=msg_id)
            return msg_id

        contact_info = request.get('contact_info', {})
        state_data = request.get('state_data', {})
        
        client_name = request.get('client_name', 'Noma\'lum')
        client_phone = contact_info.get('phone', request.get('client_phone', 'Noma\'lum'))
        created_at = request.get('created_at').strftime('%d.%m.%Y %H:%M') if request.get('created_at') else 'Noma\'lum'
        status = request.get('current_status', 'new')

        # Status emojis
        status_emoji = {
            'new': '🆕',
            'assigned_to_controller': '🎛️',
            'in_progress': '⏳',
            'completed': '✅',
            'cancelled': '❌'
        }.get(status, 'ℹ️')

        # Get comments count
        comments_count = 0

        # Full info template
        text = (
            f"🆔 <b>ID:</b> {request_id[:8]}\n"
            f"📋 <b>Tur:</b> {request.get('workflow_type', 'Noma\'lum')}\n"
            f"👤 <b>Mijoz:</b> {client_name}\n"
            f"📞 <b>Telefon:</b> {client_phone}\n"
            f"📍 <b>Manzil:</b> {request.get('location', 'Noma\'lum')}\n"
            f"📅 <b>Yaratilgan:</b> {created_at}\n"
            f"{status_emoji} <b>Holat:</b> {status}\n"
            f"💬 <b>Izohlar:</b> {comments_count} ta\n"
            f"📝 <b>Tavsif:</b> {request.get('description', '')[:150]}{'...' if request.get('description') and len(request.get('description')) > 150 else ''}\n"
        )

        # Create buttons
        buttons = []
        
        # Add comment button
        buttons.append([
            InlineKeyboardButton(
                text="💬 Izoh qo'shish",
                callback_data=f"ctrl_add_comment_{request_id}"
            )
        ])
        
        # Add detailed view button
        buttons.append([
            InlineKeyboardButton(
                text="🔍 Batafsil",
                callback_data=f"ctrl_detail_{request_id}"
            )
        ])

        # Add technician assignment button
        buttons.append([
            InlineKeyboardButton(
                text="🧰 Texnikka biriktirish",
                callback_data=f"ctrl_assign_tech_{request_id}"
            )
        ])
        # Add call center supervisor transfer button
        buttons.append([
            InlineKeyboardButton(
                text="📞 CallCenterSupervisorga yuborish",
                callback_data=f"ctrl_transfer_ccsupervisor_{request_id}"
            )
        ])

        # Navigation buttons
        nav_buttons = []
        if idx > 0:
            nav_buttons.append(InlineKeyboardButton(
                text="⬅️ Oldingi",
                callback_data="ctrl_prev_request"
            ))
        if idx < len(requests) - 1:
            nav_buttons.append(InlineKeyboardButton(
                text="Keyingisi ➡️",
                callback_data="ctrl_next_request"
            ))
        
        if nav_buttons:
            buttons.append(nav_buttons)

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        msg_id = await send_or_edit(event, text, reply_markup=keyboard, parse_mode='HTML', state=state)
        await state.update_data(current_message_id=msg_id)
        return msg_id

    @router.callback_query(F.data.startswith("ctrl_assign_tech_"))
    async def assign_to_technician(callback: CallbackQuery, state: FSMContext):
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'controller':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return
        lang = user.get('language', 'uz')
        request_id = callback.data.replace("ctrl_assign_tech_", "")
        try:
            # Get available technicians with their workload
            technicians = await get_users_by_role('technician')
            if not technicians:
                no_tech_text = "Faol texniklar topilmadi!"
                await callback.answer(no_tech_text, show_alert=True)
                return
            # Create buttons for each technician
            keyboard_buttons = []
            for tech in technicians[:8]:  # Max 8 technicians
                workload_emoji = "🟢" if tech['active_requests'] == 0 else "🟡" if tech['active_requests'] < 3 else "🔴"
                button_text = f"{workload_emoji} {tech['full_name']} ({tech['active_requests']})"
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text=button_text,
                        callback_data=f"ctrl_select_tech_{request_id}_{tech['id']}"
                    )
                ])
            # Add cancel button
            cancel_text = "❌ Bekor qilish"
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text=cancel_text,
                    callback_data=f"ctrl_cancel_assign_{request_id}"
                )
            ])
            select_text = (
                "👨‍🔧 <b>Qaysi texnikka tayinlaysiz?</b>\n\n"
                "🟢 - Bo'sh\n🟡 - Kam yuklangan\n🔴 - Ko'p yuklangan\n"
                "Qavs ichida faol zayavkalar soni ko'rsatilgan."
            )
            await send_or_edit(
                callback,
                select_text,
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons),
                state=state
            )
        except Exception as e:
            print(f"Error in assign_to_technician: user_id={callback.from_user.id}, request_id={request_id}, error={e}")
            error_msg = "Xatolik yuz berdi!"
            await callback.answer(error_msg, show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_select_tech_"))
    async def select_technician(callback: CallbackQuery, state: FSMContext):
        """Assign request to selected technician"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'controller':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return
            
        lang = user.get('language', 'uz')
        parts = callback.data.split("_")
        request_id = parts[3]
        tech_id = int(parts[4])
        
        try:
            # Mock assignment
            success = True
            
            if success:
                # Get technician's name
                tech_info = await bot.db.fetchrow(
                    "SELECT full_name, phone_number as phone FROM users WHERE id = $1", tech_id
                )
                
                tech_name = tech_info['full_name'] if tech_info else "Noma'lum"
                
                success_text = (
                    f"✅ <b>Zayavka muvaffaqiyatli {tech_name}ga tayinlandi!</b>"
                )
                
                # Update message with success status
                return await send_or_edit(callback, success_text, parse_mode='HTML', state=state)
                
                # Update the request in our state
                data = await state.get_data()
                requests = data.get('requests', [])
                for req in requests:
                    if str(req.get('id')) == request_id:
                        req['current_status'] = 'assigned_to_technician'
                        break
                
                await state.update_data(requests=requests)
                
                success_msg = "Muvaffaqiyatli tayinlandi!"
                await callback.answer(success_msg)
            else:
                error_text = "❌ <b>Xatolik yuz berdi!</b>"
                return await send_or_edit(callback, error_text, parse_mode='HTML', state=state)
                
                error_msg = "Xatolik yuz berdi!"
                await callback.answer(error_msg, show_alert=True)
                
        except Exception as e:
            print(f"Error selecting technician: user_id={callback.from_user.id}, request_id={request_id}, tech_id={tech_id}, error={e}")
            error_text = "❌ <b>Xatolik yuz berdi!</b>"
            return await send_or_edit(callback, error_text, parse_mode='HTML', state=state)
            
            error_msg = "Xatolik yuz berdi!"
            await callback.answer(error_msg, show_alert=True)
            
    @router.callback_query(F.data == "ctrl_prev_request")
    @router.callback_query(F.data == "ctrl_next_request")
    async def navigate_requests(callback: CallbackQuery, state: FSMContext):
        """Handle navigation between requests"""
        data = await state.get_data()
        current_idx = data.get('current_idx', 0)
        
        if callback.data == "ctrl_prev_request":
            new_idx = max(0, current_idx - 1)
        else:  # next_request
            requests = data.get('requests', [])
            new_idx = min(len(requests) - 1, current_idx + 1)
        
        await state.update_data(current_idx=new_idx)
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'
        
        return await show_request(callback, state, new_idx, lang)
        
    @router.callback_query(F.data.startswith("ctrl_detail_"))
    async def show_detail(callback: CallbackQuery, state: FSMContext):
        """Show detailed request information with all comments"""
        request_id = callback.data.replace("ctrl_detail_", "")
        user = await get_user_by_telegram_id(callback.from_user.id)
        lang = user.get('language', 'uz')

        try:
            # Mock request data
            request = {
                'id': request_id,
                'workflow_type': 'connection_request',
                'client_name': 'Test Client',
                'client_phone': '+998901234567',
                'location': 'Test Address',
                'description': 'Test description',
                'created_at': datetime.now(),
                'current_status': 'new',
                'contact_info': {
                    'phone': '+998901234567',
                    'full_name': 'Test Client'
                },
                'state_data': {
                    'selected_tariff': 'Test Tariff'
                }
            }
            
            if not request:
                await callback.answer("Zayavka topilmadi!", show_alert=True)
                return

            # Mock comments
            comments = []

            comments_info = ""
            if comments:
                comments_info = "\n\n💬 <b>Izohlar:</b>\n"
                for c in comments:
                    created_str = c.get('created_at')
                    if created_str:
                        # Handle both string and datetime objects
                        if isinstance(created_str, str):
                            created = datetime.fromisoformat(created_str).strftime('%d.%m.%Y %H:%M')
                        else:
                            created = created_str.strftime('%d.%m.%Y %H:%M')
                    else:
                        created = '-'
                    
                    # Get role from comment_type
                    comment_type = c.get('comment_type', '')
                    role = comment_type.replace('_comment', '') if comment_type else 'unknown'
                    
                    # Role emojis
                    role_emoji = {
                        'manager': '👨‍💼',
                        'junior_manager': '👨‍💼',
                        'controller': '🎛️',
                        'technician': '🔧',
                        'warehouse': '📦',
                        'call_center': '📞',
                        'call_center_supervisor': '📞',
                        'admin': '👑'
                    }.get(role, '👤')
                    
                    comments_info += f"{role_emoji} <b>{c['commenter']}</b> ({role}): {c['comment']} ({created})\n"

            contact_info = request.get('contact_info', {})
            state_data = request.get('state_data', {})
            
            client_name = request.get('client_name', 'Noma\'lum')
            client_phone = contact_info.get('phone', request.get('client_phone', 'Noma\'lum'))
            created_at = request.get('created_at').strftime('%d.%m.%Y %H:%M') if request.get('created_at') else 'Noma\'lum'
            tariff = state_data.get('selected_tariff', 'Noma\'lum')
            
            text = (
                f"🔌 <b>Ariza batafsil ma'lumotlari!</b>\n\n"
                f"📝 <b>ID:</b> {request['id']}\n"
                f"👤 <b>Mijoz:</b> {client_name}\n"
                f"📞 <b>Telefon:</b> {client_phone}\n"
                f"📄 <b>Ta'rif:</b> {request['description']}\n"
                f"💳 <b>Tarif:</b> {tariff}\n"
                f"📅 <b>Yaratilgan:</b> {created_at}\n"
                f"🌐 <b>Manzil:</b> {request.get('location', 'Noma\'lum')}\n"
                f"📊 <b>Status:</b> {request.get('current_status', 'Noma\'lum')}"
                f"{comments_info}"
            )

            buttons = [
                [
                    InlineKeyboardButton(text="🔙 Ortga", callback_data="ctrl_back_to_inbox")
                ]
            ]

            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
            
        except Exception as e:
            print(f"Error in show_detail: {e}")
            await callback.answer("Xatolik yuz berdi!", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_add_comment_"))
    async def add_comment_start(callback: CallbackQuery, state: FSMContext):
        """Start adding comment for controller"""
        request_id = callback.data.replace("ctrl_add_comment_", "")
        user = await get_user_by_telegram_id(callback.from_user.id)
        lang = user.get('language', 'uz')

        # Save request ID in state
        await state.update_data(comment_request_id=request_id)
        await state.set_state(ControllerRequestStates.waiting_for_comment)

        prompt_text = (
            "💬 Iltimos, izohingizni yuboring:"
        )

        cancel_text = "❌ Bekor qilish"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=cancel_text, callback_data="ctrl_cancel_comment")]
        ])

        await callback.message.edit_text(prompt_text, reply_markup=keyboard)
        await callback.answer()

    @router.message(ControllerRequestStates.waiting_for_comment)
    async def process_comment(message: Message, state: FSMContext):
        """Process the comment from controller"""
        user = await get_user_by_telegram_id(message.from_user.id)
        if not user:
            await message.answer("❌ Sizda ruxsat yo'q.")
            return

        lang = user.get('language', 'uz')
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

        try:
            # Mock comment addition
            success = True

            if success:
                success_text = "✅ Izoh muvaffaqiyatli qo'shildi!"
                await message.answer(success_text)

                # Return to inbox
                await show_controller_inbox(message, state)
            else:
                error_text = "❌ Izoh qo'shishda xatolik!"
                await message.answer(error_text)

        except Exception as e:
            print(f"Error saving comment: {e}")
            error_text = "❌ Fikrni saqlashda xatolik!"
            await message.answer(error_text)

        await state.clear()

    @router.callback_query(F.data == "ctrl_cancel_comment")
    async def cancel_comment(callback: CallbackQuery, state: FSMContext):
        """Cancel comment adding"""
        await state.clear()
        await show_controller_inbox(callback, state)
        await callback.answer()
        
    @router.callback_query(lambda c: c.data.startswith("ctrl_monitor_"))
    async def monitor_request(callback: CallbackQuery):
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'controller':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return
            
        lang = user.get('language', 'uz')
        request_id = callback.data.split("_", 2)[2]
        
        try:
            # Mock monitoring data
            monitoring_data = {
                'success': True,
                'request': {
                    'id': request_id,
                    'current_status': 'new',
                    'created_at': datetime.now()
                },
                'transitions': [],
                'technician': None
            }
            
            if not monitoring_data['success']:
                error_text = "Zayavka topilmadi!"
                await callback.answer(error_text, show_alert=True)
                return
            
            request_details = monitoring_data['request']
            transitions = monitoring_data['transitions']
            technician = monitoring_data['technician']
            
            # Monitoring ma'lumotlari
            monitor_text = f"""📊 <b>Zayavka monitoringi</b>

🆔 <b>ID:</b> {request_details['id'][:8]}...
📊 <b>Joriy status:</b> {request_details.get('current_status', '-')}
⏱️ <b>Yaratilganidan beri:</b> {(datetime.now() - request_details['created_at']).days if request_details.get('created_at') else 0} kun"""
            
            # Texnik holati
            if technician:
                tech_status = (
                    f"\n👨‍🔧 <b>Tayinlangan texnik:</b> {technician['full_name']}\n"
                    f"📞 <b>Telefon:</b> {technician.get('phone_number', 'Noma\'lum')}"
                )
                monitor_text += tech_status
            
            # So'nggi faoliyat
            if transitions:
                last_transition = transitions[-1]
                last_activity = (
                    f"\n\n⏰ <b>So'nggi faoliyat:</b>\n"
                    f"{last_transition['created_at'].strftime('%d.%m.%Y %H:%M')} - "
                    f"{last_transition.get('actor_name', 'Tizim')}: {last_transition.get('action', '-')}"
                )
                monitor_text += last_activity
            
            # Back tugmasi
            back_text = "◀️ Orqaga"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=back_text, callback_data="ctrl_back_to_inbox")]
            ])
            
            return await send_or_edit(callback, monitor_text, parse_mode='HTML', reply_markup=keyboard, state=state)
            await callback.answer()
            
        except Exception as e:
            print(f"Error in monitor_request: user_id={callback.from_user.id}, request_id={request_id}, error={e}")
            error_text = "Xatolik yuz berdi"
            await callback.answer(error_text, show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_cancel_assign_"))
    async def cancel_assign(callback: CallbackQuery, state: FSMContext):
        user = await get_user_by_telegram_id(callback.from_user.id)
        lang = user.get('language', 'uz') if user else 'uz'
        
        cancel_text = "❌ <b>Tayinlash bekor qilindi</b>"
        return await send_or_edit(callback, cancel_text, parse_mode='HTML', state=state)

    @router.callback_query(F.data == "ctrl_back_to_inbox")
    async def back_to_inbox(callback: CallbackQuery, state: FSMContext):
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            lang = user.get('language', 'uz')

            # Mock requests
            requests = [
                {
                    'id': 'req123456',
                    'workflow_type': 'connection_request',
                    'client_name': 'Test Client 1',
                    'client_phone': '+998901234567',
                    'location': 'Test Address 1',
                    'description': 'Test description 1',
                    'created_at': datetime.now(),
                    'current_status': 'new',
                    'contact_info': {
                        'phone': '+998901234567',
                        'full_name': 'Test Client 1'
                    },
                    'state_data': {
                        'selected_tariff': 'Test Tariff 1'
                    }
                }
            ]

            if not requests:
                await callback.message.edit_text("Arizalar topilmadi.")
                return

            # State'ni yangilash
            await state.update_data(requests=requests, current_index=0)

            # 0-indexli arizani ko'rsatish
            await display_inbox_page(callback, state) # Changed from show_controller_inbox to display_inbox_page
            await callback.answer()
        except Exception as e:
            print(f"Error in back_to_inbox: {e}")
            await callback.answer("Xatolik yuz berdi!", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_transfer_ccsupervisor_"))
    async def transfer_to_ccsupervisor(callback: CallbackQuery, state: FSMContext):
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'controller':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return
        lang = user.get('language', 'uz')
        request_id = callback.data.replace("ctrl_transfer_ccsupervisor_", "")
        try:
            # Mock database update
            await bot.db.execute(
                "UPDATE service_requests SET role_current = 'call_center_supervisor', current_status = 'assigned_to_call_center_supervisor', updated_at = NOW() WHERE id = $1",
                request_id
            )
            msg_text = (
                "✅ Ariza Callcenter Supervisorga muvaffaqiyatli yuborildi!"
            )
            back_text = "📥 Inboxga qaytish"
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=back_text, callback_data="controller_inbox")]
            ])
            await send_or_edit(
                callback,
                msg_text,
                reply_markup=keyboard,
                parse_mode='HTML',
                state=state
            )
            await callback.answer("Muvaffaqiyatli yuborildi!")
        except Exception as e:
            print(f"Error transferring to callcenter supervisor: user_id={callback.from_user.id}, request_id={request_id}, error={e}")
            error_msg = "Xatolik yuz berdi!"
            await callback.answer(error_msg, show_alert=True)

    return router