from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from typing import Union, List, Dict, Any
from datetime import datetime
import json

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'call_center_supervisor',
        'language': 'uz',
        'full_name': 'Test Call Center Supervisor',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_role_router(role: str):
    """Mock role router"""
    from aiogram import Router
    return Router()

async def get_call_center_supervisor_orders(user_id: int, db=None):
    """Mock supervisor orders"""
    return [
        {
            'id': '12345678',
            'contact_info': {
                'full_name': 'Test Client',
                'phone': '+998901234567'
            },
            'location': 'Toshkent shahri',
            'description': 'Internet ulanish muammosi',
            'created_at': datetime.now(),
            'current_status': 'Yangi'
        },
        {
            'id': '87654321',
            'contact_info': {
                'full_name': 'Another Client',
                'phone': '+998987654321'
            },
            'location': 'Samarqand viloyati',
            'description': 'Televizor signallari yo\'q',
            'created_at': datetime.now(),
            'current_status': 'Ko\'rib chiqilmoqda'
        }
    ]

async def get_available_operators(db):
    """Mock available operators"""
    return [
        {'id': 1, 'full_name': 'Operator 1', 'active_requests': 0},
        {'id': 2, 'full_name': 'Operator 2', 'active_requests': 2},
        {'id': 3, 'full_name': 'Operator 3', 'active_requests': 1}
    ]

async def assign_order_to_staff(order_id: str, operator_id: int, supervisor_id: int, db):
    """Mock assign order"""
    return True

async def create_supervisor_note(order_id: str, supervisor_id: int, comment: str, db):
    """Mock create note"""
    return True

async def get_service_request_details_for_supervisor(order_id: str):
    """Mock service request details"""
    return {
        'id': order_id,
        'client_name': 'Test Client',
        'description': 'Internet ulanish muammosi',
        'contact_info': '{"phone": "+998901234567"}',
        'state_data': '{"selected_tariff": "Premium", "diagnosis": "Kabel uzilgan"}',
        'location': 'Toshkent shahri',
        'created_at': datetime.now(),
        'comments': []
    }

async def send_and_track(message, user_id: int):
    """Mock send and track"""
    return await message

class CallCenterSupervisorStates(StatesGroup):
    waiting_for_operator_select = State()

async def send_or_edit(
    event: Union[Message, CallbackQuery],
    text: str,
    state: FSMContext = None,
    **kwargs
) -> int:
    try:
        if isinstance(event, CallbackQuery):
            msg_id = None
            if state:
                data = await state.get_data()
                msg_id = data.get("current_message_id")
            if msg_id:
                try:
                    msg = await event.message.edit_text(
                        chat_id=event.from_user.id,
                        message_id=msg_id,
                        text=text,
                        **kwargs
                    )
                    return msg.message_id
                except Exception as e:
                    await event.answer("Xatolik yuz berdi!", show_alert=True)
                    return None
            else:
                try:
                    msg = await event.message.edit_text(text, **kwargs)
                    return msg.message_id
                except Exception as e:
                    await event.answer("Xatolik yuz berdi!", show_alert=True)
                    return None
        else:
            try:
                msg = await event.answer(text, **kwargs)
                return msg.message_id if hasattr(msg, 'message_id') else None
            except Exception as e:
                return None
    except Exception as e:
        if isinstance(event, CallbackQuery):
            await event.answer("Xatolik yuz berdi!", show_alert=True)
        return None

def get_call_center_supervisor_inbox_router():
    """Get call center supervisor inbox router"""
    from utils.role_system import get_role_router
    router = get_role_router("call_center_supervisor")

    @router.callback_query(F.data.startswith("open_inbox_"))
    async def handle_inbox_notification(callback: CallbackQuery, state: FSMContext):
        """Handle inbox notification button click"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id_short = callback.data.replace("open_inbox_", "")
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            # Show inbox
            await show_supervisor_inbox_from_notification(callback.message, state, request_id_short)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")
    
    async def show_supervisor_inbox_from_notification(message: Message, state: FSMContext, target_request_id: str = None):
        """Show supervisor inbox with focus on specific request"""
        try:
            user = await get_user_by_telegram_id(message.chat.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            # Get inbox messages from inbox manager
            inbox_messages = [
                {
                    'id': 1,
                    'application_id': '12345678',
                    'message': 'Yangi ariza'
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
                    request_details = await get_service_request_details_for_supervisor(msg['application_id'])
                    if request_details:
                        request_details['inbox_message'] = msg
                        requests.append(request_details)
                except:
                    pass
            
            if not requests:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            await state.update_data(
                supervisor_requests=requests,
                current_index=target_index
            )
            
            # Show the targeted request
            await display_supervisor_request(message, state, requests[target_index], target_index)
            
        except Exception as e:
            pass

    @router.message(F.text.in_(["📥 Inbox"]))
    @router.callback_query(F.data == "ccs_inbox")
    async def supervisor_inbox(event: Union[Message, CallbackQuery], state: FSMContext):
        """Show call center supervisor's inbox with assigned orders"""
        if isinstance(event, CallbackQuery):
            await event.answer()
            
        user = await get_user_by_telegram_id(event.from_user.id)

        if not isinstance(user, dict):
            error_text = "Foydalanuvchi ma'lumotlarini olishda xatolik."
            await send_or_edit(event, error_text, state=state)
            return

        if user.get('role') != 'call_center_supervisor':
            error_text = "Sizda ruxsat yo'q."
            await send_or_edit(event, error_text, state=state)
            return
            
        try:
            orders = await get_call_center_supervisor_orders(user_id=user['id'])
            
            if not orders:
                no_orders = "📭 Sizga biriktirilgan buyurtmalar yo'q."
                await send_or_edit(event, no_orders, state=state)
                return
            
            # Validate and convert orders
            if not isinstance(orders, list):
                error_msg = "Xatolik: Buyurtmalar ro'yxati noto'g'ri formatda."
                await send_or_edit(event, error_msg, state=state)
                return
                
            valid_orders = []
            for o in orders:
                try:
                    order_dict = dict(o)
                    # Always parse contact_info if it's a string
                    if isinstance(order_dict.get('contact_info'), str):
                        try:
                            order_dict['contact_info'] = json.loads(order_dict['contact_info'])
                        except Exception as e:
                            order_dict['contact_info'] = {}
                    valid_orders.append(order_dict)
                except (TypeError, ValueError) as e:
                    continue
            
            if not valid_orders:
                no_orders = "📭 Sizga biriktirilgan buyurtmalar yo'q."
                await send_or_edit(event, no_orders, state=state)
                return
            
            await state.update_data(orders=valid_orders, current_idx=0)
            await show_order(event, state, 0)
            
        except Exception as e:
            error_msg = "Xatolik yuz berdi"
            await send_or_edit(event, error_msg, state=state)

    async def show_order(
        event: Union[Message, CallbackQuery], 
        state: FSMContext, 
        idx: int
    ) -> int:
        """Show a single order with navigation controls"""
        data = await state.get_data()
        orders = data.get('orders', [])
        
        if not orders or idx < 0 or idx >= len(orders):
            msg_id = await send_or_edit(
                event, 
                "📭 Buyurtmalar topilmadi.", 
                state=state
            )
            await state.update_data(current_message_id=msg_id)
            return msg_id
            
        order = orders[idx]
        
        # Ensure order is a dictionary
        if not isinstance(order, dict):
            msg_id = await send_or_edit(
                event,
                "Xatolik: Buyurtma ma'lumotlari noto'g'ri.",
                state=state
            )
            await state.update_data(current_message_id=msg_id)
            return msg_id
        
        contact_info = order.get('contact_info', {})
        if not isinstance(contact_info, dict):
            contact_info = {}
        
        created_at = order.get('created_at', '')
        if isinstance(created_at, datetime):
            created_at = created_at.strftime('%d.%m.%Y %H:%M')
        else:
            created_at = ''
        
        desc = order.get('description', 'Tavsif yo\'q')
        desc = (desc[:100] + '...') if isinstance(desc, str) and len(desc) > 100 else desc
        
        text = (
            f"📌 <b>Buyurtmas #{order.get('id', '')[:8]}</b>\n\n"
            f"👤 <b>Mijoz:</b> {contact_info.get('full_name', 'Noma\'lum')}\n"
            f"📞 <b>Telefon:</b> {contact_info.get('phone', 'Noma\'lum')}\n"
            f"📍 <b>Manzil:</b> {order.get('location', 'Ko\'rsatilmagan')}\n"
            f"📝 <b>Tavsif:</b> {desc}\n"
            f"🕒 <b>Yuborilgan:</b> {created_at}\n"
            f"📊 <b>Status:</b> {order.get('current_status', 'Yangi')}"
        )
        
        keyboard = [
            [
                InlineKeyboardButton(
                    text="👷 Operatorga biriktirish",
                    callback_data=f"ccs_assign_operator_{order['id']}"
                )
            ]
        ]
        
        nav_buttons = []
        if idx > 0:
            nav_buttons.append(InlineKeyboardButton(
                text="⬅️ Oldingi",
                callback_data="ccs_prev_order"
            ))
        if idx < len(orders) - 1:
            nav_buttons.append(InlineKeyboardButton(
                text="Keyingi ➡️",
                callback_data="ccs_next_order"
            ))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        msg_id = await send_or_edit(
            event,
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
            parse_mode='HTML',
            state=state
        )
        await state.update_data(current_message_id=msg_id)
        return msg_id

    @router.callback_query(F.data.startswith("ccs_assign_operator_"))
    async def assign_to_operator(callback: CallbackQuery, state: FSMContext):
        """Show available operators for assignment"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not isinstance(user, dict) or user.get('role') != 'call_center_supervisor':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return
            
        order_id = callback.data.split("_", 3)[3]
        
        try:
            operators = await get_available_operators(None)
            
            if not operators:
                no_ops_text = "Faol operatorlar topilmadi!"
                await callback.answer(no_ops_text, show_alert=True)
                return
            
            keyboard_buttons = []
            for op in operators[:8]:  # Max 8 operators
                workload_emoji = "🟢" if op['active_requests'] == 0 else "🟡" if op['active_requests'] < 3 else "🔴"
                button_text = f"{workload_emoji} {op['full_name']} ({op['active_requests']})"
                
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text=button_text, 
                        callback_data=f"ccs_select_operator_{order_id}_{op['id']}"
                    )
                ])
            
            cancel_text = "❌ Bekor qilish"
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text=cancel_text, 
                    callback_data=f"ccs_cancel_assign_{order_id}"
                )
            ])
            
            select_text = (
                "👷 <b>Qaysi operatorga tayinlaysiz?</b>\n\n"
                "🟢 - Bo'sh\n🟡 - Kam yuklangan\n🔴 - Ko'p yuklangan\n"
                "Qavs ichida faol buyurtmalar soni ko'rsatilgan."
            )
            
            msg_id = await send_or_edit(
                callback,
                select_text,
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons),
                state=state
            )
            await state.update_data(current_message_id=msg_id)
            await state.set_state(CallCenterSupervisorStates.waiting_for_operator_select)
            await callback.answer()
            
        except Exception as e:
            error_msg = "Xatolik yuz berdi"
            await send_or_edit(callback, error_msg, state=state)
            await callback.answer(error_msg, show_alert=True)

    @router.callback_query(F.data.startswith("ccs_select_operator_"))
    async def select_operator(callback: CallbackQuery, state: FSMContext):
        """Assign order to selected operator"""
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not isinstance(user, dict) or user.get('role') != 'call_center_supervisor':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return
            
        parts = callback.data.split("_")
        order_id = parts[3]
        operator_id = int(parts[4])
        
        try:
            success = await assign_order_to_staff(order_id, operator_id, user['id'], None)
            
            if success:
                op_name = "Test Operator"
                
                success_text = f"✅ <b>Buyurtma muvaffaqiyatli {op_name}ga tayinlandi!</b>"
                
                msg_id = await send_or_edit(
                    callback,
                    success_text,
                    parse_mode='HTML',
                    state=state
                )
                await state.update_data(current_message_id=msg_id)
                
                data = await state.get_data()
                orders = data.get('orders', [])
                for order in orders:
                    if str(order.get('id')) == order_id:
                        order['current_status'] = 'assigned_to_operator'
                        order['current_assignee_id'] = operator_id
                        break
                
                await state.update_data(orders=orders)
                await state.set_state(None)
                await callback.answer("Muvaffaqiyatli tayinlandi!")
            else:
                error_text = "❌ <b>Xatolik yuz berdi!</b>"
                msg_id = await send_or_edit(
                    callback,
                    error_text,
                    parse_mode='HTML',
                    state=state
                )
                await state.update_data(current_message_id=msg_id)
                await callback.answer("Xatolik yuz berdi!", show_alert=True)
                
        except Exception as e:
            error_text = "❌ <b>Xatolik yuz berdi!</b>"
            msg_id = await send_or_edit(
                callback,
                error_text,
                parse_mode='HTML',
                state=state
            )
            await state.update_data(current_message_id=msg_id)
            await callback.answer("Xatolik yuz berdi!", show_alert=True)

    @router.callback_query(F.data.startswith("ccs_cancel_assign_"))
    async def cancel_assign(callback: CallbackQuery, state: FSMContext):
        """Cancel operator assignment"""
        cancel_text = "❌ <b>Tayinlash bekor qilindi</b>"
        msg_id = await send_or_edit(
            callback,
            cancel_text,
            parse_mode='HTML',
            state=state
        )
        await state.update_data(current_message_id=msg_id)
        await callback.answer()


    @router.callback_query(F.data.in_(["ccs_prev_order", "ccs_next_order"]))
    async def navigate_orders(callback: CallbackQuery, state: FSMContext):
        """Handle navigation between orders"""
        data = await state.get_data()
        current_idx = data.get('current_idx', 0)
        
        if callback.data == "ccs_prev_order":
            new_idx = max(0, current_idx - 1)
        else:  # ccs_next_order
            orders = data.get('orders', [])
            new_idx = min(len(orders) - 1, current_idx + 1)
        
        await state.update_data(current_idx=new_idx)
        
        await show_order(callback, state, new_idx)
        await callback.answer()

    return router