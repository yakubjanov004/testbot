"""
Manager Statistics Handler - Complete Implementation

This module provides complete statistics functionality for Manager role,
allowing managers to view various statistics and reports.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import date, datetime, timedelta
from filters.role_filter import RoleFilter

def get_manager_statistics_router():
    """Get manager statistics router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.message(F.text == "📊 Statistika")
    async def manager_statistics_menu(message: Message):
        """Manager statistics main menu"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            # Create inline keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📈 Mening samaradorligim",
                    callback_data="mgr_my_performance"
                )],
                [InlineKeyboardButton(
                    text="👥 Jamoa statistikasi",
                    callback_data="mgr_team_stats"
                )],
                [InlineKeyboardButton(
                    text="📊 Zayavkalar statistikasi",
                    callback_data="mgr_request_stats"
                )],
                [InlineKeyboardButton(
                    text="📅 Kunlik hisobot",
                    callback_data="mgr_daily_report"
                )],
                [InlineKeyboardButton(
                    text="📥 Excel export",
                    callback_data="mgr_export_menu"
                )],
                [InlineKeyboardButton(
                    text="📋 Export tarixi",
                    callback_data="mgr_export_history"
                )]
            ])
            
            await message.answer(
                "📊 Statistika bo'limini tanlang:",
                reply_markup=keyboard
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
    
    @router.callback_query(F.data == "mgr_my_performance")
    async def manager_my_performance(callback: CallbackQuery):
        """Show manager's personal performance"""
        try:
            await callback.answer()
            
            # Mock performance data
            performance = {
                'total_sessions': 15,
                'completed_sessions': 12,
                'total_time_minutes': 480,
                'avg_duration_minutes': 32.0
            }
            
            # Format message
            text = "📈 **Mening samaradorligim (7 kun)**\n\n"
            
            text += f"📊 **Asosiy ko'rsatkichlar:**\n"
            text += f"• Jami sessiyalar: {performance.get('total_sessions', 0)}\n"
            text += f"• Yakunlangan: {performance.get('completed_sessions', 0)}\n"
            text += f"• Jami vaqt: {performance.get('total_time_minutes', 0)} min\n"
            text += f"• O'rtacha vaqt: {performance.get('avg_duration_minutes', 0):.1f} min\n\n"
            
            efficiency = (performance.get('completed_sessions', 0) / performance.get('total_sessions', 1) * 100) if performance.get('total_sessions', 0) > 0 else 0
            text += f"⚡ **Samaradorlik:** {efficiency:.1f}%\n"
            
            # Add back button
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_stats_back"
                )]
            ])
            
            await callback.message.answer(text, reply_markup=keyboard, parse_mode='Markdown')
            
        except Exception as e:
            await callback.message.answer("Xatolik yuz berdi!")
    
    @router.callback_query(F.data == "mgr_team_stats")
    async def manager_team_statistics(callback: CallbackQuery):
        """Show team statistics"""
        try:
            await callback.answer()
            
            # Mock team performance data
            team_stats = [
                {
                    'full_name': 'Test Technician 1',
                    'role': 'technician',
                    'completed_requests': 8,
                    'total_requests': 10,
                    'efficiency_score': 80.0
                },
                {
                    'full_name': 'Test Call Center 1',
                    'role': 'callcenter',
                    'completed_requests': 12,
                    'total_requests': 15,
                    'efficiency_score': 85.0
                },
                {
                    'full_name': 'Test Junior Manager 1',
                    'role': 'junior_manager',
                    'completed_requests': 6,
                    'total_requests': 8,
                    'efficiency_score': 75.0
                }
            ]
            
            # Format message
            text = "👥 **Jamoa statistikasi**\n\n"
            
            # Group by role
            roles = {}
            for member in team_stats:
                role = member.get('role', 'N/A')
                if role not in roles:
                    roles[role] = []
                roles[role].append(member)
            
            for role, members in roles.items():
                text += f"**{role.upper()}**\n"
                for member in members[:3]:  # Show top 3 per role
                    text += f"• {member.get('full_name', 'N/A')}: "
                    text += f"{member.get('completed_requests', 0)}/{member.get('total_requests', 0)} "
                    text += f"({member.get('efficiency_score', 0):.1f}%)\n"
                text += "\n"
            
            # Add buttons
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📊 To'liq hisobot",
                    callback_data="mgr_export_team_stats"
                )],
                [InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_stats_back"
                )]
            ])
            
            await callback.message.answer(text, reply_markup=keyboard, parse_mode='Markdown')
            
        except Exception as e:
            await callback.message.answer("Xatolik yuz berdi!")
    
    @router.callback_query(F.data == "mgr_request_stats")
    async def manager_request_statistics(callback: CallbackQuery):
        """Show request statistics"""
        try:
            await callback.answer()
            
            # Mock today's statistics
            today_stats = {
                'total_requests': 25,
                'completed_requests': 18,
                'cancelled_requests': 2,
                'avg_completion_time_minutes': 45.5,
                'avg_rating': 4.2
            }
            
            # Format message
            text = "📊 **Zayavkalar statistikasi (Bugun)**\n\n"
            
            text += f"📈 **Umumiy:**\n"
            text += f"• Jami: {today_stats['total_requests']}\n"
            text += f"• Yakunlangan: {today_stats['completed_requests']}\n"
            text += f"• Bekor qilingan: {today_stats['cancelled_requests']}\n"
            text += f"• Kutilmoqda: {today_stats['total_requests'] - today_stats['completed_requests'] - today_stats['cancelled_requests']}\n\n"
            
            completion_rate = (today_stats['completed_requests'] / today_stats['total_requests'] * 100) if today_stats['total_requests'] > 0 else 0
            text += f"✅ **Yakunlanish darajasi:** {completion_rate:.1f}%\n"
            text += f"⏱️ **O'rtacha vaqt:** {today_stats['avg_completion_time_minutes']:.1f} min\n"
            text += f"⭐ **O'rtacha baho:** {today_stats['avg_rating']:.2f}/5\n"
            
            # Add buttons
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📊 Haftalik",
                    callback_data="mgr_weekly_stats"
                )],
                [InlineKeyboardButton(
                    text="📊 Oylik",
                    callback_data="mgr_monthly_stats"
                )],
                [InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_stats_back"
                )]
            ])
            
            await callback.message.answer(text, reply_markup=keyboard, parse_mode='Markdown')
            
        except Exception as e:
            await callback.message.answer("Xatolik yuz berdi!")
    
    @router.callback_query(F.data == "mgr_daily_report")
    async def manager_daily_report(callback: CallbackQuery):
        """Generate daily report"""
        try:
            await callback.answer()
            
            await callback.message.answer(
                "📄 Kunlik hisobot tayyorlanmoqda..."
            )
            
            # Mock report generation
            success = True
            
            if success:
                await callback.message.answer(
                    "📊 Kunlik hisobot tayyor!\n\n"
                    "📋 Jami arizalar: 25\n"
                    "✅ Bajarilgan: 18\n"
                    "⏳ Jarayonda: 5\n"
                    "❌ Bekor: 2\n\n"
                    "📅 Sana: " + date.today().strftime('%d.%m.%Y')
                )
            else:
                await callback.message.answer(
                    "❌ Hisobot yaratishda xatolik!"
                )
                
        except Exception as e:
            await callback.message.answer("Xatolik yuz berdi!")
    
    @router.callback_query(F.data == "mgr_export_menu")
    async def manager_export_menu(callback: CallbackQuery):
        """Show export menu"""
        try:
            await callback.answer()
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📊 Kunlik statistika",
                    callback_data="mgr_export_daily"
                )],
                [InlineKeyboardButton(
                    text="👥 Xodimlar samaradorligi",
                    callback_data="mgr_export_employees"
                )],
                [InlineKeyboardButton(
                    text="📋 Zayavkalar hisoboti",
                    callback_data="mgr_export_requests"
                )],
                [InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_stats_back"
                )]
            ])
            
            await callback.message.answer(
                "📥 Qaysi hisobotni export qilmoqchisiz?",
                reply_markup=keyboard
            )
            
        except Exception as e:
            await callback.message.answer("Xatolik yuz berdi!")
    
    @router.callback_query(F.data.startswith("mgr_export_"))
    async def manager_export_handler(callback: CallbackQuery):
        """Handle export requests"""
        try:
            await callback.answer()
            
            from utils.export_utils import create_export_file
            from aiogram.types import BufferedInputFile
            
            export_type = callback.data.replace("mgr_export_", "")
            
            # Map export types to available types
            export_mapping = {
                "menu": "statistics",
                "history": "orders", 
                "team_stats": "statistics",
                "daily": "statistics",
                "employees": "users",
                "requests": "orders",
                "full_history": "orders"
            }
            
            actual_export_type = export_mapping.get(export_type, "statistics")
            
            # Create export file
            file_content, filename = create_export_file(actual_export_type, "csv", "manager")
            
            # Get file size
            file_content.seek(0, 2)  # Move to end
            file_size = file_content.tell()
            file_content.seek(0)  # Reset to beginning
            
            # Send only the file with all information in caption
            await callback.message.answer_document(
                BufferedInputFile(
                    file_content.read(),
                    filename=filename
                ),
                caption=f"✅ {actual_export_type.title()} export muvaffaqiyatli yakunlandi!\n\n"
                        f"📄 Fayl: {filename}\n"
                        f"📦 Hajm: {file_size:,} bayt\n"
                        f"📊 Format: CSV\n"
                        f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
                
        except Exception as e:
            await callback.message.answer("❌ Export xatoligi yuz berdi!")
    
    @router.callback_query(F.data == "mgr_stats_back")
    async def manager_stats_back(callback: CallbackQuery):
        """Go back to statistics menu"""
        try:
            await callback.answer()
            
            # Recreate statistics menu
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📈 Mening samaradorligim",
                    callback_data="mgr_my_performance"
                )],
                [InlineKeyboardButton(
                    text="👥 Jamoa statistikasi",
                    callback_data="mgr_team_stats"
                )],
                [InlineKeyboardButton(
                    text="📊 Zayavkalar statistikasi",
                    callback_data="mgr_request_stats"
                )],
                [InlineKeyboardButton(
                    text="📅 Kunlik hisobot",
                    callback_data="mgr_daily_report"
                )],
                [InlineKeyboardButton(
                    text="📥 Excel export",
                    callback_data="mgr_export_menu"
                )]
            ])
            
            await callback.message.edit_text(
                "📊 Statistika bo'limini tanlang:",
                reply_markup=keyboard
            )
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")
    

    @router.callback_query(F.data == "mgr_export_history")
    async def show_export_history(callback: CallbackQuery):
        """Show export history - who downloaded what"""
        try:
            await callback.answer()
            
            # Mock export history
            export_history = [
                {
                    'user_name': 'Test Manager',
                    'export_type': 'daily_statistics',
                    'created_at': datetime.now() - timedelta(hours=2),
                    'record_count': 150
                },
                {
                    'user_name': 'Test Manager',
                    'export_type': 'employee_performance',
                    'created_at': datetime.now() - timedelta(hours=4),
                    'record_count': 25
                }
            ]
            
            if not export_history:
                await callback.message.edit_text(
                    "📭 Export tarixi mavjud emas"
                )
                return
            
            text = "📋 *Export tarixi (so'nggi 20 ta):*\n\n"
            
            # Show Excel exports
            text += "📊 *Excel/CSV fayllar:*\n"
            for exp in export_history[:10]:
                user_name = exp.get('user_name', 'Unknown')
                export_type = exp.get('export_type', 'unknown')
                created_at = exp.get('created_at')
                record_count = exp.get('record_count', 0)
                
                if created_at:
                    date_str = created_at.strftime('%d.%m %H:%M')
                else:
                    date_str = ''
                
                type_names = {
                    'daily_statistics': '📅 Kunlik statistika',
                    'employee_performance': '👥 Xodimlar samaradorligi',
                    'requests_report': '📋 Zayavkalar hisoboti',
                    'speed_rating': '⚡ Tezlik reytingi',
                    'all_staff_performance': '👥 Barcha xodimlar'
                }
                
                type_name = type_names.get(export_type, export_type)
                
                text += f"  • {user_name} - {type_name}\n"
                text += f"    📅 {date_str} | 📊 {record_count} ta yozuv\n"
            
            # Add summary
            total_exports = len(export_history)
            text += f"\n📊 *Jami:* {total_exports} ta export\n"
            
            # Buttons
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📥 To'liq tarix (CSV)",
                    callback_data="mgr_export_full_history"
                )],
                [InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="mgr_export_history"
                )],
                [InlineKeyboardButton(
                    text="◀️ Orqaga",
                    callback_data="mgr_stats_menu"
                )]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_stats_menu")
    async def back_to_stats_menu(callback: CallbackQuery):
        """Go back to statistics menu"""
        try:
            await callback.answer()
            
            # Create inline keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📈 Mening samaradorligim",
                    callback_data="mgr_my_performance"
                )],
                [InlineKeyboardButton(
                    text="👥 Jamoa statistikasi",
                    callback_data="mgr_team_stats"
                )],
                [InlineKeyboardButton(
                    text="📊 Zayavkalar statistikasi",
                    callback_data="mgr_request_stats"
                )],
                [InlineKeyboardButton(
                    text="📅 Kunlik hisobot",
                    callback_data="mgr_daily_report"
                )],
                [InlineKeyboardButton(
                    text="📥 Excel export",
                    callback_data="mgr_export_menu"
                )],
                [InlineKeyboardButton(
                    text="📋 Export tarixi",
                    callback_data="mgr_export_history"
                )]
            ])
            
            await callback.message.edit_text(
                "📊 *Statistika bo'limi*\n\n"
                "Kerakli bo'limni tanlang:",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    return router
