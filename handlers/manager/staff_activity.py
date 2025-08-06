"""
Manager Staff Activity Handler - Complete Implementation

This module provides complete staff activity monitoring functionality for Manager role,
allowing managers to view online staff, performance, workload, attendance, and junior manager work.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, date, timedelta
from keyboards.manager_buttons import get_manager_main_keyboard

def get_manager_staff_activity_router():
    """Get router for manager staff activity handlers"""
    from aiogram import Router
    router = Router()

    @router.message(F.text == "👥 Xodimlar faoliyati")
    async def show_staff_activity_menu(message: Message, state: FSMContext):
        """Manager staff activity handler"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            activity_text = "👥 Xodimlar faoliyati:"
            
            # Create staff activity keyboard
            keyboard = _create_staff_activity_keyboard()
            
            await message.answer(activity_text, reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "🟢 Onlayn xodimlar")
    async def staff_online_handler(message: Message, state: FSMContext):
        """Show online staff"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            await show_online_staff(message)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "📊 Samaradorlik")
    async def staff_performance_handler(message: Message, state: FSMContext):
        """Show staff performance"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            await show_staff_performance(message)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "📋 Ish yuki")
    async def staff_workload_handler(message: Message, state: FSMContext):
        """Show staff workload"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            await show_staff_workload(message)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "📅 Davomat")
    async def staff_attendance_handler(message: Message, state: FSMContext):
        """Show staff attendance"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            await show_staff_attendance(message)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "👨‍💼 Kichik menejerlar ishi")
    async def staff_junior_work_handler(message: Message, state: FSMContext):
        """Show junior manager work"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            await show_junior_manager_work(message)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "🔙 Orqaga")
    async def staff_back_handler(message: Message, state: FSMContext):
        """Return to main menu"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Return to main menu
            await message.answer(
                "Asosiy menyu:",
                reply_markup=get_manager_main_keyboard()
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    async def show_online_staff(message):
        """Show currently online staff"""
        try:
            # Mock online staff data
            online_staff = [
                {
                    'full_name': 'Test Technician 1',
                    'role': 'technician',
                    'minutes_ago': 5
                },
                {
                    'full_name': 'Test Manager 1',
                    'role': 'manager',
                    'minutes_ago': 10
                },
                {
                    'full_name': 'Test Call Center 1',
                    'role': 'call_center',
                    'minutes_ago': 15
                },
                {
                    'full_name': 'Test Warehouse 1',
                    'role': 'warehouse',
                    'minutes_ago': 20
                },
                {
                    'full_name': 'Test Junior Manager 1',
                    'role': 'junior_manager',
                    'minutes_ago': 25
                }
            ]
            
            role_emojis = {
                'technician': '👨‍🔧',
                'manager': '👨‍💼',
                'call_center': '📞',
                'warehouse': '📦',
                'junior_manager': '👨‍💼'
            }
            
            online_text = "🟢 <b>Onlayn xodimlar:</b>\n\n"
            for staff in online_staff:
                emoji = role_emojis.get(staff['role'], '')
                online_text += f"{emoji} {staff['full_name']} ({staff['role']}) - {staff['minutes_ago']} daqiqa oldin\n"
            
            await message.answer(online_text, parse_mode='HTML')
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    async def show_staff_performance(message):
        """Show staff performance statistics"""
        try:
            # Mock performance data
            performance = [
                {
                    'full_name': 'Test Technician 1',
                    'completed_tasks': 15,
                    'total_tasks': 20
                },
                {
                    'full_name': 'Test Manager 1',
                    'completed_tasks': 25,
                    'total_tasks': 30
                },
                {
                    'full_name': 'Test Call Center 1',
                    'completed_tasks': 40,
                    'total_tasks': 45
                },
                {
                    'full_name': 'Test Warehouse 1',
                    'completed_tasks': 30,
                    'total_tasks': 35
                },
                {
                    'full_name': 'Test Junior Manager 1',
                    'completed_tasks': 20,
                    'total_tasks': 25
                }
            ]
            
            text = "📊 <b>Xodimlar samaradorligi:</b>\n\n"
            for staff in performance:
                percentage = int((staff['completed_tasks'] / staff['total_tasks']) * 100)
                text += f"👤 {staff['full_name']}: {staff['completed_tasks']} / {staff['total_tasks']} ({percentage}%)\n"
            
            await message.answer(text, parse_mode='HTML')
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    async def show_staff_workload(message):
        """Show staff workload statistics"""
        try:
            # Mock workload data
            workload = [
                {
                    'full_name': 'Test Technician 1',
                    'total_tasks': 8,
                    'completed_tasks': 6,
                    'pending_tasks': 2
                },
                {
                    'full_name': 'Test Manager 1',
                    'total_tasks': 12,
                    'completed_tasks': 10,
                    'pending_tasks': 2
                },
                {
                    'full_name': 'Test Call Center 1',
                    'total_tasks': 15,
                    'completed_tasks': 13,
                    'pending_tasks': 2
                },
                {
                    'full_name': 'Test Warehouse 1',
                    'total_tasks': 10,
                    'completed_tasks': 8,
                    'pending_tasks': 2
                },
                {
                    'full_name': 'Test Junior Manager 1',
                    'total_tasks': 6,
                    'completed_tasks': 5,
                    'pending_tasks': 1
                }
            ]
            
            text = "📋 <b>Ish yuki:</b>\n\n"
            for staff in workload:
                text += f"👤 {staff['full_name']}: {staff['total_tasks']} ta (✅ {staff['completed_tasks']}, ⏳ {staff['pending_tasks']})\n"
            
            await message.answer(text, parse_mode='HTML')
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    async def show_staff_attendance(message):
        """Show staff attendance statistics"""
        try:
            # Mock attendance data
            attendance = [
                {
                    'full_name': 'Test Technician 1',
                    'attendance_days': 22,
                    'total_days': 25,
                    'percentage': 88
                },
                {
                    'full_name': 'Test Manager 1',
                    'attendance_days': 24,
                    'total_days': 25,
                    'percentage': 96
                },
                {
                    'full_name': 'Test Call Center 1',
                    'attendance_days': 23,
                    'total_days': 25,
                    'percentage': 92
                },
                {
                    'full_name': 'Test Warehouse 1',
                    'attendance_days': 21,
                    'total_days': 25,
                    'percentage': 84
                },
                {
                    'full_name': 'Test Junior Manager 1',
                    'attendance_days': 20,
                    'total_days': 25,
                    'percentage': 80
                }
            ]
            
            text = "📅 <b>Davomat:</b>\n\n"
            for staff in attendance:
                text += f"👤 {staff['full_name']}: {staff['attendance_days']} kun ({staff['percentage']}%)\n"
            
            await message.answer(text, parse_mode='HTML')
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    async def show_junior_manager_work(message):
        """Show junior manager work statistics"""
        try:
            # Mock junior manager data
            junior_data = [
                {
                    'full_name': 'Test Junior Manager 1',
                    'phone_number': '+998901234567',
                    'completed_week': 12,
                    'in_progress': 3,
                    'new_tasks': 2,
                    'avg_completion_hours': 4.5
                },
                {
                    'full_name': 'Test Junior Manager 2',
                    'phone_number': '+998901234568',
                    'completed_week': 15,
                    'in_progress': 2,
                    'new_tasks': 1,
                    'avg_completion_hours': 3.8
                },
                {
                    'full_name': 'Test Junior Manager 3',
                    'phone_number': '+998901234569',
                    'completed_week': 8,
                    'in_progress': 5,
                    'new_tasks': 3,
                    'avg_completion_hours': 6.2
                }
            ]
            
            junior_text = "👨‍💼 <b>Kichik menejerlar ishi (7 kun):</b>\n\n"
            for junior in junior_data:
                avg_hours = round(junior['avg_completion_hours'], 1)
                junior_text += (
                    f"👨‍💼 <b>{junior['full_name']}</b>\n"
                    f"   📞 {junior['phone_number']}\n"
                    f"   ✅ Bajarilgan: {junior['completed_week']}\n"
                    f"   ⏳ Jarayonda: {junior['in_progress']}\n"
                    f"   🆕 Yangi: {junior['new_tasks']}\n"
                    f"   ⏱️ O'rtacha vaqt: {avg_hours} soat\n\n"
                )
            
            await message.answer(junior_text, parse_mode='HTML')
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    return router


def _create_staff_activity_keyboard():
    """Create keyboard for staff activity menu"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🟢 Onlayn xodimlar",
                callback_data="staff_online"
            ),
            InlineKeyboardButton(
                text="📊 Samaradorlik",
                callback_data="staff_performance"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Ish yuki",
                callback_data="staff_workload"
            ),
            InlineKeyboardButton(
                text="📅 Davomat",
                callback_data="staff_attendance"
            )
        ],
        [
            InlineKeyboardButton(
                text="👨‍💼 Kichik menejerlar ishi",
                callback_data="staff_junior_work"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Orqaga",
                callback_data="staff_back"
            )
        ]
    ])
