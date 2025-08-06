"""
Role System - Complete Implementation

This module handles role-based routing and user role detection
for the Alfa Connect bot.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from loader import get_user_role, get_bot

def get_role_router(role: str):
    """Get router for specific role"""
    router = Router()
    
    # No role filtering - allow all handlers to work normally
    return router

async def show_role_menu(message: Message, user_role: str):
    """Show appropriate menu based on user role"""
    user_id = message.from_user.id
    
    if user_role == 'admin':
        await show_admin_menu(message)
    elif user_role == 'manager':
        await show_manager_menu(message)
    elif user_role == 'client':
        await show_client_menu(message)
    elif user_role == 'technician':
        await show_technician_menu(message)
    elif user_role == 'warehouse':
        await show_warehouse_menu(message)
    elif user_role == 'call_center':
        await show_call_center_menu(message)
    elif user_role == 'call_center_supervisor':
        await show_call_center_supervisor_menu(message)
    elif user_role == 'junior_manager':
        await show_junior_manager_menu(message)
    elif user_role == 'controller':
        await show_controller_menu(message)
    else:
        await show_default_menu(message)

async def show_admin_menu(message: Message):
    """Show admin menu"""
    from keyboards.admin_buttons import get_admin_main_keyboard
    
    text = "👨‍💼 Admin paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_admin_main_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

async def show_manager_menu(message: Message):
    """Show manager menu"""
    from keyboards.manager_buttons import get_manager_main_keyboard
    
    text = "👨‍💼 Menejer paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_manager_main_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

async def show_client_menu(message: Message):
    """Show client menu"""
    from keyboards.client_buttons import get_client_main_keyboard
    
    text = "👤 Mijoz paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_client_main_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

async def show_technician_menu(message: Message):
    """Show technician menu"""
    from keyboards.technician_buttons import get_technician_main_keyboard
    
    text = "👨‍🔧 Texnik paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_technician_main_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

async def show_warehouse_menu(message: Message):
    """Show warehouse menu"""
    from keyboards.warehouse_buttons import get_warehouse_main_keyboard
    
    text = "📦 Ombor paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_warehouse_main_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

async def show_call_center_menu(message: Message):
    """Show call center menu"""
    from keyboards.call_center_buttons import get_call_center_main_keyboard
    
    text = "📞 Call Center paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_call_center_main_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

async def show_call_center_supervisor_menu(message: Message):
    """Show call center supervisor menu"""
    from keyboards.call_center_supervisor_buttons import get_call_center_supervisor_main_keyboard
    
    text = "👨‍💼 Call Center Supervisor paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_call_center_supervisor_main_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

async def show_junior_manager_menu(message: Message):
    """Show junior manager menu"""
    from keyboards.junior_manager_buttons import get_junior_manager_main_keyboard
    
    text = "👨‍💼 Kichik Menejer paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_junior_manager_main_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

async def show_controller_menu(message: Message):
    """Show controller menu"""
    from keyboards.controllers_buttons import get_controller_main_keyboard
    
    text = "🎛️ Kontroller paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_controller_main_keyboard()
    
    await message.answer(text, reply_markup=keyboard)

async def show_default_menu(message: Message):
    """Show default menu for unknown roles"""
    text = "👋 Xush kelibsiz!\n\nSizning rolingiz hali aniqlanmagan. Iltimos, administrator bilan bog'laning."
    
    await message.answer(text) 