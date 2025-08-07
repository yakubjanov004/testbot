"""
Applications Callbacks Handler - Soddalashtirilgan versiya

Bu modul manager uchun arizalar bilan bog'liq callback funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.manager_states import ManagerApplicationStates
from keyboards.manager_buttons import (
    get_manager_main_keyboard,
    get_application_actions_keyboard,
    get_application_navigation_keyboard
)
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter

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

async def answer_and_cleanup(callback: CallbackQuery, text: str, **kwargs):
    """Mock answer and cleanup"""
    await callback.answer(text, **kwargs)

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

# Mock service request
async def get_service_request(request_id: str):
    """Mock get service request"""
    return {
        'id': request_id,
        'workflow_type': 'connection_request',
        'created_by_staff': False,
        'contact_info': {
            'full_name': 'Test Client',
            'phone': '+998901234567'
        },
        'description': 'Test ariza',
        'location': 'Test manzil'
    }

# Mock word generator
class MockWordGenerator:
    """Mock word generator"""
    async def generate_act_document(self, request_id: str, document_type: str):
        """Mock generate act document"""
        print(f"Mock: Generating {document_type} document for request {request_id}")
        return f"/tmp/mock_document_{request_id}.docx"

def get_manager_applications_callbacks_router():
    """Router for applications callback functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.callback_query(F.data == "back_to_applications")
    async def back_to_applications(callback: CallbackQuery, state: FSMContext):
        """Manager back to applications handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            text = "Arizalar menyusiga qaytdingiz."
            
            # Inline keyboard ishlatish
            keyboard_buttons = [
                [
                    InlineKeyboardButton(
                        text="📋 Hammasini ko'rish",
                        callback_data="mgr_view_all_applications"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔎 ID bo'yicha ko'rish",
                        callback_data="mgr_view_by_id"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Asosiy menyu",
                        callback_data="mgr_back_to_main"
                    )
                ]
            ]
            
            keyboard = get_application_navigation_keyboard(lang=user.get('language', 'uz'))
            
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            await callback.answer()
            await state.clear()
            
        except Exception as e:
            print(f"Error in back_to_applications: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_view_all_applications")
    async def view_all_applications_callback(callback: CallbackQuery, state: FSMContext):
        """Manager view all applications callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Use workflow access control to get filtered requests for manager role
            access_control = MockWorkflowAccessControl()
            requests = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager'
            )
            
            if not requests:
                text = "Hozircha hech qanday ariza yo'q."
                keyboard_buttons = [
                    [
                        InlineKeyboardButton(
                            text="⬅️ Orqaga",
                            callback_data="back_to_applications"
                        )
                    ]
                ]
                keyboard = get_application_navigation_keyboard(lang=user.get('language', 'uz'))
                
                await callback.message.edit_text(
                    text=text,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = requests[current_index]
            
            # Status belgilarini aniqlash
            status_emoji = {
                'created': '🆕',
                'in_progress': '⏳',
                'completed': '✅',
                'cancelled': '❌'
            }.get(current_request.get('current_status', 'created'), '📋')
            
            workflow_type = current_request.get('workflow_type', 'unknown')
            workflow_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(workflow_type, '📋')
            
            # Zayavka turini formatlash
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Qo\'ng\'iroq markazi'
            }.get(workflow_type, 'Noma\'lum')
            
            # Mijoz ma'lumotlari
            client_name = current_request.get('contact_info', {}).get('full_name', 'N/A') if isinstance(current_request.get('contact_info'), dict) else 'N/A'
            client_phone = current_request.get('contact_info', {}).get('phone', 'N/A') if isinstance(current_request.get('contact_info'), dict) else 'N/A'
            
            # Vaqt ma'lumotlari
            created_at = current_request.get('created_at', 'N/A')
            updated_at = current_request.get('updated_at', 'N/A')
            
            # Vaqt hisoblash
            total_duration = "N/A"
            if created_at and created_at != 'N/A':
                try:
                    if isinstance(created_at, str):
                        created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    else:
                        created_dt = created_at
                    
                    current_time = datetime.now()
                    if created_dt.tzinfo is None:
                        created_dt = created_dt.replace(tzinfo=None)
                    
                    duration = current_time - created_dt
                    total_hours = int(duration.total_seconds() // 3600)
                    total_minutes = int((duration.total_seconds() % 3600) // 60)
                    
                    if total_hours > 0:
                        total_duration = f"{total_hours}s {total_minutes}d"
                    else:
                        total_duration = f"{total_minutes} daqiqa"
                except Exception as e:
                    print(f"Error calculating duration: {e}")
                    total_duration = "N/A"
            
            # Izoh va diagnostika
            description = current_request.get('description', 'Izoh yo\'q')
            location = current_request.get('location', 'Manzil ko\'rsatilmagan')
            
            # Joriy rol va status
            current_role = current_request.get('role_current', 'Noma\'lum')
            current_status = current_request.get('current_status', 'Noma\'lum')
            
            # Status matnini formatlash
            status_text = {
                'created': 'Yaratilgan',
                'in_progress': 'Jarayonda',
                'completed': 'Tugallangan',
                'cancelled': 'Bekor qilingan'
            }.get(current_status, current_status)
            
            text = f"""
📋 <b>Ariza #{current_index + 1} / {len(requests)}</b>

{status_emoji}{workflow_emoji} <b>{client_name}</b>
   📋 ID: {current_request['id'][:8]}...
   🏷️ Turi: {workflow_type_text}
   📊 Status: {status_text}
   👤 Joriy rol: {current_role}

📞 <b>Mijoz ma'lumotlari:</b>
   • Nomi: {client_name}
   • Telefon: {client_phone}
   • Manzil: {location}

⏰ <b>Vaqt ma'lumotlari:</b>
   • Yaratilgan: {created_at}
   • Yangilangan: {updated_at}
   • Umumiy vaqt: {total_duration}

📝 <b>Izoh va diagnostika:</b>
   {description}

🔧 <b>Texnik ma'lumotlar:</b>
   • Workflow type: {workflow_type}
   • Current status: {current_status}
   • Role current: {current_role}
"""
            
            # Asosiy tugmalar
            keyboard_buttons = []
            if current_request.get('current_status') != 'completed':
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="👨‍💼 Junior menejerga berish",
                        callback_data=f"assign_junior_{current_request['id'][:8]}"
                    )
                ])
            
            # Word hujjat tugmasi (barcha statuslar uchun)
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="📄 Word hujjat olish",
                    callback_data=f"mgr_word_doc_{current_request['id'][:20]}"
                )
            ])
            
            # Navigatsiya tugmalari
            if len(requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_application"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_application"
                    )
                ])
            
            keyboard = get_application_navigation_keyboard(lang=user.get('language', 'uz'))
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_application_index=current_index)
            
            try:
                await callback.message.edit_text(
                    text=text,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
            except Exception as e:
                if "message is not modified" in str(e):
                    await callback.answer()
                else:
                    await callback.message.edit_text(
                        text=text,
                        reply_markup=keyboard,
                        parse_mode='HTML'
                    )
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in view_all_applications_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_view_by_id")
    async def view_by_id_callback(callback: CallbackQuery, state: FSMContext):
        """Manager view by ID callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            text = "Ariza ID raqamini kiriting :"
            
            keyboard_buttons = [
                [
                    InlineKeyboardButton(
                        text="⬅️ Orqaga",
                        callback_data="back_to_applications"
                    )
                ]
            ]
            keyboard = get_application_navigation_keyboard(lang=user.get('language', 'uz'))
            
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            await state.set_state(ManagerApplicationStates.waiting_for_id)
            await callback.answer()
            
        except Exception as e:
            print(f"Error in view_by_id_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_back_to_main")
    async def back_to_main_callback(callback: CallbackQuery, state: FSMContext):
        """Manager back to main callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            text = "Asosiy menyuga qaytdingiz."
            
            # Yangi xabar yuborish (edit_text emas)
            await callback.message.answer(text, reply_markup=get_manager_main_keyboard(lang))
            await callback.answer()
            await state.clear()
            
        except Exception as e:
            print(f"Error in back_to_main_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("mgr_word_doc_"))
    async def manager_generate_word(callback: CallbackQuery):
        """Manager uchun Word hujjat yaratish"""
        try:
            lang = await get_user_lang(callback.from_user.id)
            request_id = callback.data.replace("mgr_word_doc_", "")
            
            # Get request details to determine document type
            request = await get_service_request(request_id)
            
            if not request:
                await callback.answer(
                    "❌ Zayavka topilmadi",
                    show_alert=True
                )
                return
            
            # Determine document type based on workflow
            doc_type = 'connection'
            if request.get('workflow_type') == 'technical_service':
                doc_type = 'technical_service'
            elif request.get('created_by_staff'):
                doc_type = 'staff_created'
            
            # Generate ACT document
            word_generator = MockWordGenerator()
            file_path = await word_generator.generate_act_document(
                request_id=request_id,
                document_type=doc_type
            )
            
            if file_path:
                # Send document
                await callback.message.answer_document(
                    open(file_path, 'rb'),
                    caption=f"📄 Xizmat buyurtmasi #{request_id}"
                )
                
                await callback.answer(
                    "✅ Word hujjat yuborildi"
                )
            else:
                await callback.answer(
                    "❌ Hujjat yaratishda xatolik",
                    show_alert=True
                )
        except Exception as e:
            print(f"Error generating Word document: {e}")
            await callback.answer(
                "❌ Xatolik yuz berdi",
                show_alert=True
            )

    @router.callback_query(F.data == "mgr_prev_application")
    async def prev_application_callback(callback: CallbackQuery, state: FSMContext):
        """Manager previous application callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            # Get current index from state
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Decrease index
            current_index = max(0, current_index - 1)
            
            # Update state
            await state.update_data(current_application_index=current_index)
            
            # Trigger view all applications with new index
            await view_all_applications_callback(callback, state)
            
        except Exception as e:
            print(f"Error in prev_application_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_next_application")
    async def next_application_callback(callback: CallbackQuery, state: FSMContext):
        """Manager next application callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            # Get current index from state
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Get total applications count
            access_control = MockWorkflowAccessControl()
            requests = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager'
            )
            
            # Increase index
            current_index = min(len(requests) - 1, current_index + 1)
            
            # Update state
            await state.update_data(current_application_index=current_index)
            
            # Trigger view all applications with new index
            await view_all_applications_callback(callback, state)
            
        except Exception as e:
            print(f"Error in next_application_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router 