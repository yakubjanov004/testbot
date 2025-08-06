"""
Junior Manager Applications Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun arizalarni ko'rish va boshqarish funksionalligini o'z ichiga oladi.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from utils.role_system import get_role_router

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

# Mock workflow and state management
class MockStateManager:
    """Mock state manager"""
    async def get_filtered_requests_for_role(self, user_id: int, user_role: str):
        """Mock get filtered requests for role"""
        return [
            {
                'id': 'req_001',
                'current_status': 'assigned_to_junior_manager',
                'contact_info': {
                    'full_name': 'Aziz Karimov',
                    'phone': '+998901234567'
                },
                'location': 'Tashkent, Chorsu',
                'description': 'Internet ulanish arizasi',
                'created_at': datetime.now(),
                'role_current': 'junior_manager'
            },
            {
                'id': 'req_002',
                'current_status': 'in_progress',
                'contact_info': {
                    'full_name': 'Malika Toshmatova',
                    'phone': '+998901234568'
                },
                'location': 'Tashkent, Yunusabad',
                'description': 'TV signal muammosi',
                'created_at': datetime.now(),
                'role_current': 'junior_manager'
            }
        ]

    async def get_request(self, request_id: str):
        """Mock get request"""
        return {
            'id': request_id,
            'current_status': 'assigned_to_junior_manager',
            'contact_info': {
                'full_name': 'Test Client',
                'phone': '+998901234567'
            },
            'location': 'Tashkent, Test Address',
            'description': 'Test description',
            'created_at': datetime.now(),
            'role_current': 'junior_manager',
            'state_data': {
                'selected_tariff': 'Premium',
                'connection_type': 'Fiber',
                'call_notes': 'Mijoz bilan bog\'lanish amalga oshirildi'
            }
        }

class MockWorkflowEngine:
    """Mock workflow engine"""
    async def transition_workflow(self, request_id: str, action: str, role: str, data: dict):
        """Mock workflow transition"""
        return True

class MockWorkflowEngineFactory:
    """Mock workflow engine factory"""
    @staticmethod
    def create_workflow_engine(state_manager, notification_system, inventory_manager):
        """Mock create workflow engine"""
        return MockWorkflowEngine()

class MockNotificationSystem:
    """Mock notification system"""
    async def send_notification_to_role(self, role: str, message: str, notification_type: str):
        """Mock send notification"""
        pass

class MockInventoryManager:
    """Mock inventory manager"""
    pass

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerStates(StatesGroup):
    entering_call_notes = State()
    entering_forward_comment = State()

# Mock workflow actions
class WorkflowAction:
    CALL_CLIENT = "call_client"
    FORWARD_TO_CONTROLLER = "forward_to_controller"

def get_applications_router():
    """Get applications router"""
    router = get_role_router("junior_manager")

    @router.message(F.text.in_(["📥 Inbox"]))
    async def show_junior_manager_inbox(message: Message, state: FSMContext):
        """Show junior manager inbox with assigned applications"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return
            
            lang = user.get('language', 'uz')
            
            # Get junior manager's requests using mock workflow access control
            state_manager = MockStateManager()
            requests = await state_manager.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='junior_manager'
            )
            
            if not requests:
                text = "📭 Sizga tayinlangan arizalar yo'q."
                await message.answer(text)
                return
            
            # Store requests and initialize navigation
            await state.update_data(
                inbox_requests=requests,
                current_index=0,
                inbox_active=True
            )
            
            # Show first request
            await display_junior_manager_request(message, state, requests, 0, lang, user)
            
        except Exception as e:
            print(f"Error in show_junior_manager_inbox: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    async def display_junior_manager_request(event, state: FSMContext, requests, index, lang, user):
        """Display a single request with junior manager action buttons"""
        try:
            user_id = event.from_user.id if hasattr(event, 'from_user') else event.chat.id
            
            req = requests[index]
            
            # Get full request details
            state_manager = MockStateManager()
            request = await state_manager.get_request(req['id'])
            
            if not request:
                text = "Ariza tafsilotlari topilmadi"
                if hasattr(event, 'answer'):
                    await event.answer(text)
                else:
                    await event.edit_text(text)
                return
            
            # Format request display
            workflow_emoji = '🔌'  # Junior managers only handle connection requests
            
            status_emoji = {
                'created': '🆕',
                'assigned_to_junior_manager': '👨‍💼',
                'in_progress': '⏳',
                'completed': '✅',
                'cancelled': '❌'
            }.get(request.current_status, '📋')
            
            client_name = request.contact_info.get('full_name', 'N/A') if isinstance(request.contact_info, dict) else 'N/A'
            client_phone = request.contact_info.get('phone', 'N/A') if isinstance(request.contact_info, dict) else 'N/A'
            
            # Check if client was called and notes added
            state_data = request.state_data or {}
            client_called = state_data.get('client_called', False)
            call_notes = state_data.get('call_notes', '')
            
            text = f"""🔌 <b>Junior Manager Inbox</b>

🆔 <b>ID:</b> {request.id[:8]}-{request.id[8:12].upper()}
🗂 <b>Holat:</b> {status_emoji} {request.current_status}
👤 <b>Biriktirilgan:</b> Junior Manager
👥 <b>Mijoz:</b> {client_name}
📱 <b>Telefon:</b> {client_phone}
📍 <b>Manzil:</b> {request.location or 'N/A'}
📝 <b>Tavsif:</b> {request.description[:100]}{'...' if len(request.description) > 100 else ''}
📅 <b>Yaratilgan:</b> {request.created_at}
<i>Ariza {index + 1}/{len(requests)}</i>"""
            
            # Create action buttons
            buttons = []
            
            # Navigation buttons
            nav_buttons = []
            if index > 0:
                nav_buttons.append(InlineKeyboardButton(
                    text="⬅️ Oldingi",
                    callback_data="jm_prev"
                ))
            if index < len(requests) - 1:
                nav_buttons.append(InlineKeyboardButton(
                    text="Keyingisi ➡️",
                    callback_data="jm_next"
                ))
            
            if nav_buttons:
                buttons.append(nav_buttons)
            
            # Action buttons
            action_row1 = [
                InlineKeyboardButton(
                    text="📄 Batafsil",
                    callback_data=f"jm_detail_{request.id[:8]}"
                )
            ]
            
            # Show appropriate action buttons based on client call status
            action_row2 = []
            if not client_called:
                action_row2.append(InlineKeyboardButton(
                    text="📞 Mijozni chaqirish",
                    callback_data=f"jm_call_client_{request.id[:8]}"
                ))
            else:
                action_row2.append(InlineKeyboardButton(
                    text="📤 Controllerga yuborish",
                    callback_data=f"jm_forward_controller_{request.id[:8]}"
                ))
            
            buttons.append(action_row1)
            if action_row2:
                buttons.append(action_row2)
            
            # Store current request in state
            await state.update_data(
                current_request_id=request.id,
                current_request_short=request.id[:8]
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            # Send or edit message
            if hasattr(event, 'edit_text'):
                await event.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await event.answer(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            print(f"Error in display_junior_manager_request: {str(e)}")
            text = "Xatolik yuz berdi"
            if hasattr(event, 'answer'):
                await event.answer(text)
            else:
                await event.edit_text(text)

    @router.callback_query(F.data == "jm_prev")
    async def navigate_prev(callback: CallbackQuery, state: FSMContext):
        """Navigate to previous application in inbox"""
        try:
            data = await state.get_data()
            requests = data.get('inbox_requests', [])
            current_index = data.get('current_index', 0)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return
            
            lang = user.get('language', 'uz')
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_index=new_index)
                
                await display_junior_manager_request(callback, state, requests, new_index, lang, user)
            else:
                await callback.answer("Bu birinchi ariza")
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in navigate_prev: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "jm_next")
    async def navigate_next(callback: CallbackQuery, state: FSMContext):
        """Navigate to next application in inbox"""
        try:
            data = await state.get_data()
            requests = data.get('inbox_requests', [])
            current_index = data.get('current_index', 0)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                return
            
            lang = user.get('language', 'uz')
            
            if current_index < len(requests) - 1:
                new_index = current_index + 1
                await state.update_data(current_index=new_index)
                
                await display_junior_manager_request(callback, state, requests, new_index, lang, user)
            else:
                await callback.answer("Bu oxirgi ariza")
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in navigate_next: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_detail_"))
    async def show_detail(callback: CallbackQuery, state: FSMContext):
        try:
            request_id_short = callback.data.replace("jm_detail_", "")
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            data = await state.get_data()
            current_request_id = data.get('current_request_id')
            
            if not current_request_id:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Get full request details
            state_manager = MockStateManager()
            request = await state_manager.get_request(current_request_id)
            
            if not request:
                await callback.answer("Ariza tafsilotlari topilmadi", show_alert=True)
                return
            
            # Format detailed view
            client_name = request.contact_info.get('full_name', 'N/A') if isinstance(request.contact_info, dict) else 'N/A'
            client_phone = request.contact_info.get('phone', 'N/A') if isinstance(request.contact_info, dict) else 'N/A'
            
            # Get connection request special data
            special_info = ""
            if request.state_data:
                tariff = request.state_data.get('selected_tariff', 'N/A')
                connection_type = request.state_data.get('connection_type', 'N/A')
                call_notes = request.state_data.get('call_notes', '')
                
                special_info = f"""📦 <b>Tarif:</b> {tariff}
🔗 <b>Ulanish turi:</b> {connection_type}
📞 <b>Qo'ng'iroq izohlari:</b> {call_notes or 'Yo\'q'}"""
            
            text = f"""📄 <b>Ariza tafsilotlari</b>

🆔 <b>ID:</b> {request.id[:8]}-{request.id[8:12].upper()}
👤 <b>Mijoz:</b> {client_name}
📱 <b>Telefon:</b> {client_phone}
📍 <b>Manzil:</b> {request.location or 'N/A'}
📝 <b>Tavsif:</b> {request.description}
📅 <b>Yaratilgan:</b> {request.created_at}
📊 <b>Status:</b> {request.current_status}
👨‍💼 <b>Joriy rol:</b> {request.role_current}
{special_info}"""
            
            # Back button
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="🔙 Orqaga",
                    callback_data="jm_back_to_inbox"
                )
            ]])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            await callback.answer()
            
        except Exception as e:
            print(f"Error in show_detail: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "jm_back_to_inbox")
    async def back_to_inbox(callback: CallbackQuery, state: FSMContext):
        try:
            data = await state.get_data()
            requests = data.get('inbox_requests', [])
            current_index = data.get('current_index', 0)
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            await display_junior_manager_request(callback.message, state, requests, current_index, lang, user)
            await callback.answer()
            
        except Exception as e:
            print(f"Error in back_to_inbox: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("jm_call_client_"))
    async def call_client_start(callback: CallbackQuery, state: FSMContext):
        try:
            request_id_short = callback.data.replace("jm_call_client_", "")
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            await state.update_data(call_request_id_short=request_id_short)
            
            text = f"""📞 <b>Mijozni chaqirish</b>

📋 Ariza ID: {request_id_short}

Mijoz bilan qo'ng'iroq qiling va natijani yozing:

• Mijoz bilan bog'lanish holati
• Qo'shimcha ma'lumotlar
• Keyingi harakatlar

Qo'ng'iroq natijasini yozing:"""
            
            await callback.message.edit_text(text, parse_mode='HTML')
            await state.set_state(JuniorManagerStates.entering_call_notes)
            await callback.answer()
            
        except Exception as e:
            print(f"Error in call_client_start: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(JuniorManagerStates.entering_call_notes))
    async def process_call_notes(message: Message, state: FSMContext):
        try:
            call_notes = message.text
            data = await state.get_data()
            current_request_id = data.get('current_request_id')
            
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            if not current_request_id:
                await message.answer("Sessiya muddati tugadi. Qaytadan boshlang.")
                await state.clear()
                return
            
            # Initialize workflow engine and record call
            state_manager = MockStateManager()
            notification_system = MockNotificationSystem()
            inventory_manager = MockInventoryManager()
            workflow_engine = MockWorkflowEngineFactory.create_workflow_engine(
                state_manager, notification_system, inventory_manager
            )
            
            transition_data = {
                'actor_id': user['id'],
                'client_called': True,
                'call_notes': call_notes,
                'call_timestamp': str(datetime.now()),
                'comments': f"Client called by junior manager: {call_notes}"
            }
            
            success = await workflow_engine.transition_workflow(
                current_request_id,
                WorkflowAction.CALL_CLIENT.value,
                'junior_manager',
                transition_data
            )
            
            if success:
                text = f"""✅ <b>Qo'ng'iroq qayd qilindi!</b>

📞 Natija: {call_notes[:100]}{'...' if len(call_notes) > 100 else ''}

Endi arizani controllerga yuborishingiz mumkin."""
                await message.answer(text, parse_mode='HTML')
                
                # Return to inbox
                requests = data.get('inbox_requests', [])
                current_index = data.get('current_index', 0)
                
                if requests:
                    await display_junior_manager_request(message, state, requests, current_index, lang, user)
                
            else:
                await message.answer("Saqlashda xatolik yuz berdi")
            
            # Clear call state but keep inbox data
            call_data = await state.get_data()
            call_data.pop('call_request_id_short', None)
            await state.set_data(call_data)
            await state.clear()
            
        except Exception as e:
            print(f"Error in process_call_notes: {str(e)}")
            await message.answer("Xatolik yuz berdi")
            await state.clear()

    @router.callback_query(F.data.startswith("jm_forward_controller_"))
    async def forward_to_controller(callback: CallbackQuery, state: FSMContext):
        try:
            request_id_short = callback.data.replace("jm_forward_controller_", "")
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Store request info for comment
            await state.update_data(forward_request_id_short=request_id_short)
            
            text = f"""📤 <b>Controllerga yuborish</b>

📋 Ariza ID: {request_id_short}

Controllerga yuborishdan oldin qo'shimcha izoh qoldirmoqchimisiz?
(Bu majburiy emas)

Izohingizni yozing yoki /skip yozing:"""
            
            await callback.message.edit_text(text, parse_mode='HTML')
            await state.set_state(JuniorManagerStates.entering_forward_comment)
            await callback.answer()
            
        except Exception as e:
            print(f"Error in forward_to_controller: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(JuniorManagerStates.entering_forward_comment))
    async def process_forward_comment(message: Message, state: FSMContext):
        try:
            comment = message.text.strip() if message.text != '/skip' else ''
            data = await state.get_data()
            current_request_id = data.get('current_request_id')
            
            user = await get_user_by_telegram_id(message.from_user.id)
            lang = user.get('language', 'uz')
            
            if not current_request_id:
                await message.answer("Sessiya muddati tugadi. Qaytadan boshlang.")
                await state.clear()
                return
            
            # Initialize workflow engine and forward to controller
            state_manager = MockStateManager()
            notification_system = MockNotificationSystem()
            inventory_manager = MockInventoryManager()
            workflow_engine = MockWorkflowEngineFactory.create_workflow_engine(
                state_manager, notification_system, inventory_manager
            )
            
            transition_data = {
                'actor_id': user['id'],
                'forwarded_to_controller': True,
                'forward_timestamp': str(datetime.now()),
                'forward_comment': comment,
                'comments': f"Forwarded to controller by junior manager {user.get('full_name', 'N/A')}" + 
                           (f". Additional comment: {comment}" if comment else "")
            }
            
            success = await workflow_engine.transition_workflow(
                current_request_id,
                WorkflowAction.FORWARD_TO_CONTROLLER.value,
                'junior_manager',
                transition_data
            )
            
            if success:
                text = f"""✅ <b>Controllerga yuborildi!</b>

📝 Ariza ID: {current_request_id[:8]}
💬 Izoh: {comment if comment else 'Yo\'q'}

Ariza sizning inboxingizdan o'chirilib, controller inboxiga o'tdi."""
                
                await message.answer(text, parse_mode='HTML')
                
                # Remove the request from current session
                requests = data.get('inbox_requests', [])
                updated_requests = [r for r in requests if r['id'] != current_request_id]
                current_index = data.get('current_index', 0)
                
                if updated_requests:
                    # Adjust index if needed
                    if current_index >= len(updated_requests):
                        current_index = len(updated_requests) - 1
                    
                    await state.update_data(
                        inbox_requests=updated_requests,
                        current_index=current_index
                    )
                    
                    # Show next request after 2 seconds
                    import asyncio
                    await asyncio.sleep(2)
                    await display_junior_manager_request(message, state, updated_requests, current_index, lang, user)
                else:
                    await state.clear()
                    
            else:
                await message.answer("Yuborishda xatolik yuz berdi")
            
            # Clear forward state but keep inbox data
            forward_data = await state.get_data()
            forward_data.pop('forward_request_id_short', None)
            await state.set_data(forward_data)
            await state.clear()
            
        except Exception as e:
            print(f"Error in process_forward_comment: {str(e)}")
            await message.answer("Xatolik yuz berdi")
            await state.clear()

    return router
