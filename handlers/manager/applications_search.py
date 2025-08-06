"""
Applications Search Handler - Soddalashtirilgan versiya

Bu modul manager uchun arizalar qidirish va ID orqali ko'rish funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from states.manager_states import ManagerApplicationStates
from keyboards.manager_buttons import get_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'


# Mock workflow access control
class MockWorkflowAccessControl:
    """Mock workflow access control"""
    async def get_filtered_requests_for_role(self, user_id: int, user_role: str):
        """Mock get filtered requests for role"""
        from datetime import datetime
        return [
            {
                'id': 'req_001_2024_01_15',
                'workflow_type': 'connection_request',
                'current_status': 'in_progress',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Aziz Karimov',
                    'phone': '+998901234567'
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'description': 'Internet ulanish arizasi',
                'location': 'Tashkent, Chorsu'
            },
            {
                'id': 'req_002_2024_01_16',
                'workflow_type': 'technical_service',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Malika Toshmatova',
                    'phone': '+998901234568'
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'description': 'TV signal muammosi',
                'location': 'Tashkent, Yunusabad'
            },
            {
                'id': 'req_003_2024_01_17',
                'workflow_type': 'call_center_direct',
                'current_status': 'completed',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Jahongir Azimov',
                    'phone': '+998901234569'
                },
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'description': 'Qo\'ng\'iroq markazi arizasi',
                'location': 'Tashkent, Sergeli'
            }
        ]

# Mock state manager
class MockStateManager:
    """Mock state manager"""
    async def get_request(self, request_id: str):
        """Mock get request"""
        from datetime import datetime
        return {
            'id': request_id,
            'workflow_type': 'connection_request',
            'current_status': 'in_progress',
            'role_current': 'manager',
            'contact_info': {
                'full_name': 'Test Client',
                'phone': '+998901234567'
            },
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'description': 'Test ariza',
            'location': 'Test manzil'
        }

# Mock workflow type enum
class WorkflowType:
    CONNECTION_REQUEST = "connection_request"
    TECHNICAL_SERVICE = "technical_service"
    CALL_CENTER_DIRECT = "call_center_direct"

def get_applications_search_router():
    """Router for applications search functionality"""
    router = Router()

    @router.message(F.text.in_(["🔎 ID bo'yicha ko'rish"]))
    async def view_by_id_prompt(message: Message, state: FSMContext):
        """Manager view by ID prompt handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            text = "Ariza ID raqamini kiriting :"
            
            # Use send_and_track for inline cleanup
            await message.answer(text, reply_markup=get_manager_back_keyboard(lang))
            
            await state.set_state(ManagerApplicationStates.waiting_for_id)
            
        except Exception as e:
            print(f"Error in view_by_id_prompt: {e}")
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(StateFilter(ManagerApplicationStates.waiting_for_id))
    async def view_application_by_id(message: Message, state: FSMContext):
        """Manager view application by ID handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            request_id_short = message.text.strip()
            
            # Use state manager to find request by partial ID
            state_manager = MockStateManager()
            
            # Search for requests with matching partial ID
            access_control = MockWorkflowAccessControl()
            all_requests = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager'
            )
            
            matching_request = None
            for req in all_requests:
                if req['id'].startswith(request_id_short):
                    matching_request = req
                    break
            
            if not matching_request:
                text = f"ID {request_id_short} bilan boshlanadigan ariza topilmadi."
                
                # Use send_and_track for inline cleanup
                await message.answer(text, reply_markup=get_manager_back_keyboard(lang))
                
                await state.clear()
                return
            
            # Get full request details
            request = await state_manager.get_request(matching_request['id'])
            
            if not request:
                text = "Ariza tafsilotlari topilmadi."
                
                # Use send_and_track for inline cleanup
                await message.answer(text, reply_markup=get_manager_back_keyboard(lang))
                
                await state.clear()
                return
            
            # Format request details
            workflow_type_display = {
                'connection_request': 'Ulanish',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Call markaz'
            }.get(request['workflow_type'], request['workflow_type'])
            
            status_text = {
                'created': 'Yaratilgan',
                'in_progress': 'Jarayonda',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }.get(request['current_status'], request['current_status'])
            
            client_name = request['contact_info'].get('full_name', 'N/A') if isinstance(request['contact_info'], dict) else 'N/A'
            client_phone = request['contact_info'].get('phone', 'N/A') if isinstance(request['contact_info'], dict) else 'N/A'
            
            text = f"""📋 Ariza tafsilotlari:

🆔 ID: {request['id'][:8]}...
🏷️ Turi: {workflow_type_display}
👤 Mijoz: {client_name}
📱 Telefon: {client_phone}
📊 Status: {status_text}
📅 Yaratilgan: {request['created_at']}
🏠 Manzil: {request.get('location', 'N/A')}
📝 Tavsif: {request.get('description', 'N/A')}"""
            
            # Create action buttons based on workflow state
            buttons = []
            
            # Manager can assign to junior manager for connection requests
            if request['workflow_type'] == WorkflowType.CONNECTION_REQUEST and request['role_current'] == 'manager':
                buttons.append([InlineKeyboardButton(
                    text="👨‍💼 Junior menejerga biriktirish",
                    callback_data=f"assign_junior_{request['id'][:8]}"
                )])
            
            # Add comment button
            buttons.append([InlineKeyboardButton(
                text="💬 Izoh qo'shish",
                callback_data=f"add_comment_{request['id'][:8]}"
            )])
            
            buttons.append([InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data="back_to_applications"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            # Use send_and_track for inline cleanup
            await message.answer(text, reply_markup=keyboard)
            
            await state.clear()
            
        except Exception as e:
            print(f"Error in view_application_by_id: {e}")
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)
            await state.clear()

    return router 