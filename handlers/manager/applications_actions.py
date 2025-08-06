"""
Applications Actions Handler - Soddalashtirilgan versiya

Bu modul manager uchun arizalar bilan bog'liq amallar funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
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

async def get_users_by_role(role: str):
    """Mock get users by role"""
    if role == 'junior_manager':
        return [
            {
                'id': 2,
                'full_name': 'Ahmad Toshmatov',
                'phone_number': '+998901234568',
                'role': 'junior_manager',
                'is_active': True
            },
            {
                'id': 3,
                'full_name': 'Malika Karimova',
                'phone_number': '+998901234569',
                'role': 'junior_manager',
                'is_active': True
            },
            {
                'id': 4,
                'full_name': 'Jahongir Azimov',
                'phone_number': '+998901234570',
                'role': 'junior_manager',
                'is_active': True
            }
        ]
    return []

async def answer_and_cleanup(callback: CallbackQuery, text: str, **kwargs):
    """Mock answer and cleanup"""
    await callback.answer(text, **kwargs)

# Mock workflow engine
class MockWorkflowEngine:
    """Mock workflow engine"""
    async def transition_workflow(self, request_id: str, action: str, role: str, data: dict):
        """Mock workflow transition"""
        print(f"Mock: Transitioning workflow {request_id} with action {action} by {role}")
        return True

# Mock workflow action enum
class WorkflowAction:
    ASSIGN_TO_JUNIOR_MANAGER = "assign_to_junior_manager"

def get_manager_applications_actions_router():
    """Router for applications actions functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.callback_query(F.data.startswith("assign_junior_"))
    async def assign_to_junior_manager(callback: CallbackQuery, state: FSMContext):
        """Manager assign to junior manager handler"""
        try:
            request_id_short = callback.data.replace("assign_junior_", "")
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            if not user or user['role'] != 'manager':
                await callback.answer("Sizda ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Get available junior managers
            junior_managers = await get_users_by_role('junior_manager')
            
            if not junior_managers:
                await callback.answer("Junior menejerlar topilmadi", show_alert=True)
                return
            
            # Create selection keyboard
            buttons = []
            for jm in junior_managers:
                buttons.append([InlineKeyboardButton(
                    text=f"👨‍💼 {jm.get('full_name', 'N/A')}",
                    callback_data=f"confirm_assign_{request_id_short}_{jm['id']}"
                )])
            
            buttons.append([InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data="back_to_applications"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            text = f"Junior menejer tanlang (Ariza: {request_id_short}):"
            
            await callback.message.edit_text(text, reply_markup=keyboard)
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in assign_to_junior_manager: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("confirm_assign_"))
    async def confirm_assignment(callback: CallbackQuery, state: FSMContext):
        """Confirm assignment to junior manager"""
        try:
            parts = callback.data.replace("confirm_assign_", "").split("_")
            request_id_short = parts[0]
            junior_manager_id = int(parts[1])
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            if not user or user['role'] != 'manager':
                await callback.answer("Sizda ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Initialize mock workflow engine
            workflow_engine = MockWorkflowEngine()
            
            # Perform workflow transition to assign to junior manager
            transition_data = {
                'actor_id': user['id'],
                'junior_manager_id': junior_manager_id,
                'comments': f"Assigned to junior manager by manager {user.get('full_name', 'N/A')}"
            }
            
            success = await workflow_engine.transition_workflow(
                request_id_short,
                WorkflowAction.ASSIGN_TO_JUNIOR_MANAGER,
                'manager',
                transition_data
            )
            
            if success:
                text = f"✅ Ariza {request_id_short} junior menejerga biriktirildi!"
                
                await callback.message.edit_text(text)
                
                await callback.answer()
                
            else:
                await callback.answer("Biriktirish amalga oshmadi", show_alert=True)
            
        except Exception as e:
            print(f"Error in confirm_assignment: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("assign_technician_"))
    async def assign_to_technician(callback: CallbackQuery, state: FSMContext):
        """Manager assign to technician handler"""
        try:
            request_id_short = callback.data.replace("assign_technician_", "")
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            if not user or user['role'] != 'manager':
                await callback.answer("Sizda ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Mock technicians data
            technicians = [
                {
                    'id': 5,
                    'full_name': 'Umar Toshmatov',
                    'specialization': 'Internet',
                    'is_available': True
                },
                {
                    'id': 6,
                    'full_name': 'Aziz Karimov',
                    'specialization': 'TV',
                    'is_available': True
                },
                {
                    'id': 7,
                    'full_name': 'Malik Azimov',
                    'specialization': 'Equipment',
                    'is_available': True
                }
            ]
            
            if not technicians:
                await callback.answer("Texniklar topilmadi", show_alert=True)
                return
            
            # Create selection keyboard
            buttons = []
            for tech in technicians:
                buttons.append([InlineKeyboardButton(
                    text=f"🔧 {tech.get('full_name', 'N/A')} ({tech.get('specialization', 'N/A')})",
                    callback_data=f"confirm_assign_tech_{request_id_short}_{tech['id']}"
                )])
            
            buttons.append([InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data="back_to_applications"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            text = f"Texnik tanlang (Ariza: {request_id_short}):"
            
            await callback.message.edit_text(text, reply_markup=keyboard)
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error in assign_to_technician: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("confirm_assign_tech_"))
    async def confirm_technician_assignment(callback: CallbackQuery, state: FSMContext):
        """Confirm assignment to technician"""
        try:
            parts = callback.data.replace("confirm_assign_tech_", "").split("_")
            request_id_short = parts[0]
            technician_id = int(parts[1])
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            if not user or user['role'] != 'manager':
                await callback.answer("Sizda ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Initialize mock workflow engine
            workflow_engine = MockWorkflowEngine()
            
            # Perform workflow transition to assign to technician
            transition_data = {
                'actor_id': user['id'],
                'technician_id': technician_id,
                'comments': f"Assigned to technician by manager {user.get('full_name', 'N/A')}"
            }
            
            success = await workflow_engine.transition_workflow(
                request_id_short,
                "assign_to_technician",
                'manager',
                transition_data
            )
            
            if success:
                text = f"✅ Ariza {request_id_short} texnikka biriktirildi!"
                
                await callback.message.edit_text(text)
                
                await callback.answer()
                
            else:
                await callback.answer("Biriktirish amalga oshmadi", show_alert=True)
            
        except Exception as e:
            print(f"Error in confirm_technician_assignment: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("approve_application_"))
    async def approve_application(callback: CallbackQuery, state: FSMContext):
        """Manager approve application handler"""
        try:
            request_id_short = callback.data.replace("approve_application_", "")
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            if not user or user['role'] != 'manager':
                await callback.answer("Sizda ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Initialize mock workflow engine
            workflow_engine = MockWorkflowEngine()
            
            # Perform workflow transition to approve application
            transition_data = {
                'actor_id': user['id'],
                'comments': f"Application approved by manager {user.get('full_name', 'N/A')}"
            }
            
            success = await workflow_engine.transition_workflow(
                request_id_short,
                "approve_application",
                'manager',
                transition_data
            )
            
            if success:
                text = f"✅ Ariza {request_id_short} tasdiqlandi!"
                
                await callback.message.edit_text(text)
                
                await callback.answer()
                
            else:
                await callback.answer("Tasdiqlash amalga oshmadi", show_alert=True)
            
        except Exception as e:
            print(f"Error in approve_application: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("reject_application_"))
    async def reject_application(callback: CallbackQuery, state: FSMContext):
        """Manager reject application handler"""
        try:
            request_id_short = callback.data.replace("reject_application_", "")
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            if not user or user['role'] != 'manager':
                await callback.answer("Sizda ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Initialize mock workflow engine
            workflow_engine = MockWorkflowEngine()
            
            # Perform workflow transition to reject application
            transition_data = {
                'actor_id': user['id'],
                'comments': f"Application rejected by manager {user.get('full_name', 'N/A')}"
            }
            
            success = await workflow_engine.transition_workflow(
                request_id_short,
                "reject_application",
                'manager',
                transition_data
            )
            
            if success:
                text = f"❌ Ariza {request_id_short} rad etildi!"
                
                await callback.message.edit_text(text)
                
                await callback.answer()
                
            else:
                await callback.answer("Rad etish amalga oshmadi", show_alert=True)
            
        except Exception as e:
            print(f"Error in reject_application: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("hold_application_"))
    async def hold_application(callback: CallbackQuery, state: FSMContext):
        """Manager hold application handler"""
        try:
            request_id_short = callback.data.replace("hold_application_", "")
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            if not user or user['role'] != 'manager':
                await callback.answer("Sizda ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Initialize mock workflow engine
            workflow_engine = MockWorkflowEngine()
            
            # Perform workflow transition to hold application
            transition_data = {
                'actor_id': user['id'],
                'comments': f"Application put on hold by manager {user.get('full_name', 'N/A')}"
            }
            
            success = await workflow_engine.transition_workflow(
                request_id_short,
                "hold_application",
                'manager',
                transition_data
            )
            
            if success:
                text = f"⏸️ Ariza {request_id_short} to'xtatildi!"
                
                await callback.message.edit_text(text)
                
                await callback.answer()
                
            else:
                await callback.answer("To'xtatish amalga oshmadi", show_alert=True)
            
        except Exception as e:
            print(f"Error in hold_application: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("complete_application_"))
    async def complete_application(callback: CallbackQuery, state: FSMContext):
        """Manager complete application handler"""
        try:
            request_id_short = callback.data.replace("complete_application_", "")
            user = await get_user_by_telegram_id(callback.from_user.id)
            
            if not user or user['role'] != 'manager':
                await callback.answer("Sizda ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Initialize mock workflow engine
            workflow_engine = MockWorkflowEngine()
            
            # Perform workflow transition to complete application
            transition_data = {
                'actor_id': user['id'],
                'comments': f"Application completed by manager {user.get('full_name', 'N/A')}"
            }
            
            success = await workflow_engine.transition_workflow(
                request_id_short,
                "complete_application",
                'manager',
                transition_data
            )
            
            if success:
                text = f"✅ Ariza {request_id_short} bajarildi!"
                
                await callback.message.edit_text(text)
                
                await callback.answer()
                
            else:
                await callback.answer("Bajarish amalga oshmadi", show_alert=True)
            
        except Exception as e:
            print(f"Error in complete_application: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router