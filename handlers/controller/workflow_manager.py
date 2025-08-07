"""
Controller Workflow Manager Handler
Manages workflow management for controller
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from filters.role_filter import RoleFilter
from keyboards.controllers_buttons import (
    get_workflow_manager_keyboard,
    get_workflow_navigation_keyboard
)

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
    """Mock get user language"""
    return 'uz'

async def get_workflow_statistics():
    """Mock get workflow statistics"""
    return {
        'total_workflows': 25,
        'active_workflows': 8,
        'completed_workflows': 15,
        'pending_workflows': 2,
        'avg_completion_time': '3.2 soat',
        'success_rate': 92,
        'efficiency_score': 4.6
    }

async def get_active_workflows():
    """Mock get active workflows"""
    return [
        {
            'id': 1,
            'workflow_name': 'Internet ulanish jarayoni',
            'workflow_type': 'connection',
            'status': 'active',
            'current_step': 'Texnik tayinlash',
            'progress': 60,
            'assigned_to': 'Aziz Karimov',
            'created_at': '2024-01-15 10:30',
            'estimated_completion': '2024-01-15 16:30'
        },
        {
            'id': 2,
            'workflow_name': 'TV xizmati sozlash',
            'workflow_type': 'tv_service',
            'status': 'active',
            'current_step': 'Xizmatni sinab ko\'rish',
            'progress': 80,
            'assigned_to': 'Malika Yusupova',
            'created_at': '2024-01-15 09:15',
            'estimated_completion': '2024-01-15 14:15'
        },
        {
            'id': 3,
            'workflow_name': 'Texnik xizmat',
            'workflow_type': 'maintenance',
            'status': 'active',
            'current_step': 'Muammoni hal qilish',
            'progress': 40,
            'assigned_to': 'Bekzod Toirov',
            'created_at': '2024-01-15 08:45',
            'estimated_completion': '2024-01-15 17:45'
        }
    ]

def get_workflow_manager_router():
    """Get controller workflow manager router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["⚙️ Workflow boshqaruvi", "⚙️ Управление процессами"]))
    async def view_workflow_manager(message: Message, state: FSMContext):
        """Handle workflow manager view"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            workflow_stats = await get_workflow_statistics()
            
            workflow_text = (
                "⚙️ <b>Workflow boshqaruvi</b>\n\n"
                "📊 <b>Umumiy statistika:</b>\n"
                f"• Jami workflow: {workflow_stats['total_workflows']}\n"
                f"• Faol workflow: {workflow_stats['active_workflows']}\n"
                f"• Bajarilgan: {workflow_stats['completed_workflows']}\n"
                f"• Kutilayotgan: {workflow_stats['pending_workflows']}\n"
                f"• O'rtacha bajarish vaqti: {workflow_stats['avg_completion_time']}\n"
                f"• Muvaffaqiyat darajasi: {workflow_stats['success_rate']}%\n"
                f"• Samaradorlik balli: {workflow_stats['efficiency_score']}/5\n\n"
                "Kerakli bo'limni tanlang:"
            )
            
            keyboard = get_workflow_manager_keyboard(lang)
            
            await message.answer(
                workflow_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in view_workflow_manager: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data == "view_workflow_statistics")
    async def view_workflow_statistics(callback: CallbackQuery, state: FSMContext):
        """View detailed workflow statistics"""
        try:
            await callback.answer()
            
            # Get detailed statistics
            stats = await get_workflow_statistics()
            
            stats_text = (
                "📊 <b>Workflow statistikasi - To'liq ma'lumot</b>\n\n"
                "📈 <b>Asosiy ko'rsatkichlar:</b>\n"
                f"🆔 <b>Jami arizalar:</b> {stats['total_applications']}\n"
                f"⏳ <b>Kutilmoqda:</b> {stats['pending']}\n"
                f"🔄 <b>Jarayonda:</b> {stats['in_progress']}\n"
                f"✅ <b>Bajarilgan:</b> {stats['completed']}\n"
                f"❌ <b>Bekor qilingan:</b> {stats['cancelled']}\n\n"
                f"⏰ <b>O'rtacha ishlov berish vaqti:</b> {stats['avg_processing_time']}\n"
                f"📈 <b>Muvaffaqiyat darajasi:</b> {stats['success_rate']}\n\n"
                "📊 <b>Analitika:</b>\n"
                "• Eng ko'p ariza: Ulanish xizmati\n"
                "• Eng tez bajariladigan: Call Center\n"
                "• Eng sekin: Texnik xizmat"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_workflow_manager")]
            ])
            
            await callback.message.edit_text(stats_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "view_active_workflows")
    async def view_active_workflows(callback: CallbackQuery, state: FSMContext):
        """View active workflows"""
        try:
            await callback.answer()
            
            # Get active workflows
            workflows = await get_active_workflows()
            
            if not workflows:
                no_workflows_text = (
                    "📭 Faol workflowlar mavjud emas."
                    if callback.from_user.language_code == 'uz' else
                    "📭 Нет активных процессов."
                )
                
                await callback.message.edit_text(
                    text=no_workflows_text,
                    reply_markup=get_controller_back_keyboard('uz')
                )
                return
            
            # Show first workflow
            await show_workflow_details(callback, workflows[0], workflows, 0)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    async def show_workflow_details(callback, workflow, workflows, index):
        """Show workflow details with navigation"""
        try:
            # Format status
            status_emoji = {
                'active': '🟢',
                'inactive': '🔴',
                'maintenance': '🟡'
            }.get(workflow['status'], '⚪')
            
            status_text = {
                'active': 'Faol',
                'inactive': 'Faol emas',
                'maintenance': 'Texnik xizmat'
            }.get(workflow['status'], 'Noma\'lum')
            
            # To'liq ma'lumot
            text = (
                f"⚙️ <b>Workflow ma'lumotlari - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Workflow ID:</b> {workflow['id']}\n"
                f"📋 <b>Nomi:</b> {workflow['name']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"📊 <b>Arizalar soni:</b> {workflow['applications_count']}\n"
                f"⏰ <b>O'rtacha vaqt:</b> {workflow['avg_time']}\n"
                f"📈 <b>Muvaffaqiyat darajasi:</b> {workflow['success_rate']}\n\n"
                f"📊 <b>Workflow #{index + 1} / {len(workflows)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_workflows_navigation_keyboard(index, len(workflows))
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "workflow_prev")
    async def show_previous_workflow(callback: CallbackQuery, state: FSMContext):
        """Show previous workflow"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_workflow_index', 0)
            
            workflows = await get_active_workflows()
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_workflow_index=new_index)
                await show_workflow_details(callback, workflows[new_index], workflows, new_index)
            else:
                await callback.answer("Bu birinchi workflow")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "workflow_next")
    async def show_next_workflow(callback: CallbackQuery, state: FSMContext):
        """Show next workflow"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_workflow_index', 0)
            
            workflows = await get_active_workflows()
            
            if current_index < len(workflows) - 1:
                new_index = current_index + 1
                await state.update_data(current_workflow_index=new_index)
                await show_workflow_details(callback, workflows[new_index], workflows, new_index)
            else:
                await callback.answer("Bu oxirgi workflow")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

def get_workflows_navigation_keyboard(current_index: int, total_workflows: int):
    """Create navigation keyboard for workflows"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="workflow_prev"
        ))
    
    # Next button
    if current_index < total_workflows - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="workflow_next"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifawfmanager", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)