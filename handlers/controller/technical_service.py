"""
Controller handlers for Technical Service requests - Soddalashtirilgan versiya

Bu modul controller uchun texnik xizmat so'rovlarini boshqarish handlerlarini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime

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

async def get_user_lang(user_id: int):
    """Mock user language"""
    return 'uz'

async def get_role_router(role: str):
    """Mock role router"""
    from aiogram import Router
    return Router()

async def send_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock send and track"""
    return await message_func(text, **kwargs)

async def edit_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock edit and track"""
    return await message_func(text, **kwargs)

async def cleanup_user_inline_messages(user_id: int):
    """Mock cleanup function"""
    pass

async def get_available_technicians():
    """Mock available technicians"""
    return [
        {
            'id': 1,
            'full_name': 'Ahmad Toshmatov',
            'phone': '+998901234567',
            'specialization': 'Internet',
            'is_available': True,
            'current_location': 'Tashkent'
        },
        {
            'id': 2,
            'full_name': 'Bekzod Karimov',
            'phone': '+998901234568',
            'specialization': 'TV',
            'is_available': True,
            'current_location': 'Tashkent'
        },
        {
            'id': 3,
            'full_name': 'Dilshod Mirzayev',
            'phone': '+998901234569',
            'specialization': 'Telefon',
            'is_available': False,
            'current_location': 'Samarkand'
        }
    ]

# Mock state manager
class MockStateManager:
    """Mock state manager"""
    
    async def get_requests_by_role(self, role: str, status: str):
        """Mock get requests by role"""
        return [
            {
                'id': 'req_001',
                'description': 'Internet tezligi sekin',
                'created_at': datetime.now(),
                'priority': 'medium',
                'workflow_type': 'technical_service'
            },
            {
                'id': 'req_002', 
                'description': 'TV signal yo\'q',
                'created_at': datetime.now(),
                'priority': 'high',
                'workflow_type': 'technical_service'
            },
            {
                'id': 'req_003',
                'description': 'Telefon ishlamayapti',
                'created_at': datetime.now(),
                'priority': 'urgent',
                'workflow_type': 'technical_service'
            }
        ]
    
    async def get_request(self, request_id: str):
        """Mock get request"""
        return {
            'id': request_id,
            'description': 'Internet tezligi sekin',
            'created_at': datetime.now(),
            'priority': 'medium',
            'workflow_type': 'technical_service'
        }

# Mock workflow engine
class MockWorkflowEngine:
    """Mock workflow engine"""
    
    async def transition_workflow(self, request_id: str, action: str, role: str, data: dict):
        """Mock workflow transition"""
        return True

# Mock keyboards
def technical_service_assignment_keyboard(request_id: str, technicians: list, lang: str):
    """Mock technical service assignment keyboard"""
    keyboard = []
    
    for tech in technicians:
        if tech['is_available']:
            status_emoji = "🟢" if tech['is_available'] else "🔴"
            button_text = f"{status_emoji} {tech['full_name']} ({tech['specialization']})"
            keyboard.append([
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"assign_technical_to_technician_{tech['id']}_{request_id}"
                )
            ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Bekor qilish",
            callback_data="cancel_technical_assignment"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_controller_technical_service_router():
    """Get controller technical service router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")
    
    # Initialize mock components
    state_manager = MockStateManager()
    workflow_engine = MockWorkflowEngine()
    
    @router.message(F.text.in_(["🔧 Texnik xizmatlar"]))
    async def show_technical_requests(message: Message, state: FSMContext):
        """Show pending technical service requests"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await send_and_track(
                    message.answer,
                    "Sizda controller huquqi yo'q.",
                    user_id
                )
                return
            
            lang = user.get('language', 'uz')
            
            try:
                # Get pending technical service requests
                requests = await state_manager.get_requests_by_role('controller', 'in_progress')
                
                # Filter for technical service requests
                technical_requests = [
                    req for req in requests 
                    if req['workflow_type'] == 'technical_service'
                ]
                
                if not technical_requests:
                    text = "🔧 Hozirda texnik xizmat so'rovlari yo'q."
                    
                    await send_and_track(
                        message.answer,
                        text,
                        user_id
                    )
                    return
                
                text = f"🔧 <b>Texnik xizmat so'rovlari ({len(technical_requests)} ta):</b>\n\n"
                
                for i, request in enumerate(technical_requests[:10], 1):
                    priority_emoji = {
                        'low': '🟢',
                        'medium': '🟡', 
                        'high': '🟠',
                        'urgent': '🔴'
                    }.get(request['priority'], '⚪')
                    
                    text += (
                        f"{priority_emoji} <b>{i}. ID: {request['id'][:8]}</b>\n"
                        f"📝 {request['description'][:60]}...\n"
                        f"📅 {request['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
                    )
                
                text += "Texnikni tayinlash uchun so'rovni tanlang:"
                
                # Create inline keyboard with requests
                keyboard = []
                for i, request in enumerate(technical_requests[:10], 1):
                    button_text = f"{i}. {request['id'][:8]} - {request['description'][:20]}..."
                    keyboard.append([{
                        'text': button_text,
                        'callback_data': f"assign_technical_request_{request['id']}"
                    }])
                
                reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=btn['text'], callback_data=btn['callback_data'])]
                    for btn in keyboard
                ])
                
                await send_and_track(
                    message.answer,
                    text,
                    user_id,
                    parse_mode='HTML',
                    reply_markup=reply_markup
                )
                
            except Exception as e:
                print(f"Error showing technical requests: {e}")
                error_text = "Xatolik yuz berdi!"
                await send_and_track(
                    message.answer,
                    error_text,
                    user_id
                )
                
        except Exception as e:
            print(f"Error showing technical requests: {e}")
            error_text = "Xatolik yuz berdi!"
            await send_and_track(
                message.answer,
                error_text,
                user_id
            )
    
    @router.callback_query(F.data.startswith("assign_technical_request_"))
    async def show_technician_selection(callback: CallbackQuery):
        """Show available technicians for assignment"""
        user_id = callback.from_user.id
        
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda bu amalni bajarish huquqi yo'q!")
                return
            
            request_id = callback.data.split("_")[-1]
            lang = user.get('language', 'uz')
            
            try:
                # Get request details
                request = await state_manager.get_request(request_id)
                if not request:
                    error_text = "So'rov topilmadi!"
                    await callback.answer(error_text)
                    return
                
                # Get available technicians
                technicians = await get_available_technicians()
                
                if not technicians:
                    no_tech_text = "Mavjud texniklar yo'q!"
                    await callback.answer(no_tech_text)
                    return
                
                text = (
                    f"🔧 <b>Texnik xizmat so'rovi</b>\n\n"
                    f"🆔 ID: {request['id'][:8]}\n"
                    f"📝 Muammo: {request['description']}\n"
                    f"📅 Yaratilgan: {request['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"Texnikni tanlang:"
                )
                
                keyboard = technical_service_assignment_keyboard(request_id, technicians, lang)
                
                await edit_and_track(
                    callback.message.edit_text,
                    text,
                    user_id,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                
            except Exception as e:
                print(f"Error showing technician selection: {e}")
                await callback.answer("Xatolik yuz berdi!")
                
        except Exception as e:
            print(f"Error showing technician selection: {e}")
            await callback.answer("Xatolik yuz berdi!")
    
    @router.callback_query(F.data.startswith("assign_technical_to_technician_"))
    async def assign_technical_to_technician(callback: CallbackQuery):
        """Assign technical request to technician"""
        user_id = callback.from_user.id
        
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Sizda bu amalni bajarish huquqi yo'q!")
                return
            
            # Parse callback data: assign_technical_to_technician_{technician_id}_{request_id}
            parts = callback.data.split("_")
            technician_id = int(parts[4])
            request_id = parts[5]
            
            lang = user.get('language', 'uz')
            
            try:
                # Get technician details
                technicians = await get_available_technicians()
                technician = next((t for t in technicians if t['id'] == technician_id), None)
                
                if not technician:
                    error_text = "Texnik topilmadi!"
                    await callback.answer(error_text)
                    return
                
                # Process workflow transition
                transition_data = {
                    'technician_id': technician_id,
                    'actor_id': user['id'],
                    'assigned_at': str(datetime.now()),
                    'technician_name': technician['full_name']
                }
                
                success = await workflow_engine.transition_workflow(
                    request_id,
                    'assign_technical_to_technician',
                    'controller',
                    transition_data
                )
                
                if success:
                    success_text = (
                        f"✅ <b>Texnik tayinlandi!</b>\n\n"
                        f"👨‍🔧 Texnik: {technician['full_name']}\n"
                        f"🆔 So'rov ID: {request_id[:8]}\n\n"
                        f"Texnikga bildirishnoma yuborildi."
                    )
                    
                    await edit_and_track(
                        callback.message.edit_text,
                        success_text,
                        user_id,
                        parse_mode='HTML'
                    )
                    
                    print(f"Technical request {request_id} assigned to technician {technician_id} by controller {user['id']}")
                    
                else:
                    error_text = "Tayinlashda xatolik!"
                    await callback.answer(error_text)
                
            except Exception as e:
                print(f"Error assigning technical to technician: {e}")
                await callback.answer("Xatolik yuz berdi!")
                
        except Exception as e:
            print(f"Error assigning technical to technician: {e}")
            await callback.answer("Xatolik yuz berdi!")
    
    @router.callback_query(F.data == "cancel_technical_assignment")
    async def cancel_technical_assignment(callback: CallbackQuery):
        """Cancel technical assignment"""
        user_id = callback.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            cancel_text = "❌ Texnik tayinlash bekor qilindi."
            
            await edit_and_track(
                callback.message.edit_text,
                cancel_text,
                user_id
            )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error canceling technical assignment: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    return router
