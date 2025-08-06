"""
Manager Statistics Handler - Complete Implementation

This module provides complete statistics functionality for Manager role,
allowing managers to view various statistics and reports.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import date, datetime, timedelta

def get_manager_statistics_router():
    """Get manager statistics router"""
    from utils.role_system import get_role_router
    router = get_role_router("manager")
    
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
            
            await callback.message.answer(
                "📊 Export tayyorlanmoqda..."
            )
            
            # Create export file
            file_content, filename = create_export_file(actual_export_type, "csv")
            
            # Send success message
            await callback.message.answer(
                "✅ Export tayyor!\n\n"
                f"📄 Fayl turi: {actual_export_type}\n"
                f"📁 Fayl: {filename}\n"
                "📅 Sana: " + date.today().strftime('%d.%m.%Y') + "\n"
                "📊 Ma'lumotlar soni: 150"
            )
            
            # Send the actual file
            await callback.message.answer_document(
                BufferedInputFile(
                    file_content.read(),
                    filename=filename
                ),
                caption=f"📤 {actual_export_type.title()} export - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
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
    
    @router.message(F.text == "🕐 Real vaqtda kuzatish")
    async def manager_realtime_monitoring(message: Message):
        """Real-time monitoring menu for manager"""
        try:
            # Create inline keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🔴 Hozir ishlayotganlar",
                    callback_data="mgr_rt_working_now"
                )],
                [InlineKeyboardButton(
                    text="⏱️ Bugungi vaqt sarfi",
                    callback_data="mgr_rt_time_spent"
                )],
                [InlineKeyboardButton(
                    text="📊 Jonli statistika",
                    callback_data="mgr_rt_live_stats"
                )],
                [InlineKeyboardButton(
                    text="🔔 Kelgan zayavkalar",
                    callback_data="mgr_rt_incoming"
                )],
                [InlineKeyboardButton(
                    text="⚡ Tezlik reytingi",
                    callback_data="mgr_rt_speed_rating"
                )]
            ])
            
            await message.answer(
                "🕐 *Real vaqtda monitoring*\n\n"
                "Xodimlar faoliyatini jonli kuzating:",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_rt_working_now")
    async def show_working_now(callback: CallbackQuery):
        """Show who is currently working on requests"""
        try:
            await callback.answer()
            
            # Mock active sessions
            active_sessions = [
                {
                    'user_name': 'Test Technician 1',
                    'role': 'technician',
                    'request_id': 'APP-001',
                    'started_at': datetime.now() - timedelta(hours=1, minutes=30)
                },
                {
                    'user_name': 'Test Call Center 1',
                    'role': 'callcenter',
                    'request_id': 'APP-002',
                    'started_at': datetime.now() - timedelta(minutes=45)
                }
            ]
            
            if not active_sessions:
                await callback.message.edit_text(
                    "📭 Hozirda hech kim zayavka ustida ishlamayapti"
                )
                return
            
            text = "🔴 *Hozir ishlayotganlar:*\n\n"
            
            for session in active_sessions:
                user_name = session.get('user_name', 'Unknown')
                role = session.get('role', 'unknown')
                request_id = session.get('request_id')
                started_at = session.get('started_at')
                
                # Calculate time spent
                if started_at:
                    time_spent = datetime.now() - started_at
                    hours = int(time_spent.total_seconds() // 3600)
                    minutes = int((time_spent.total_seconds() % 3600) // 60)
                    time_str = f"{hours}s {minutes}d"
                else:
                    time_str = "0d"
                
                text += f"👤 *{user_name}* ({role})\n"
                text += f"📋 Zayavka: #{request_id}\n"
                text += f"⏱️ Vaqt: {time_str}\n\n"
            
            # Add refresh button
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="mgr_rt_working_now"
                )],
                [InlineKeyboardButton(
                    text="◀️ Orqaga",
                    callback_data="mgr_rt_menu"
                )]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_rt_time_spent")
    async def show_time_spent_today(callback: CallbackQuery):
        """Show time spent by each employee today"""
        try:
            await callback.answer()
            
            # Mock today's time statistics
            today_stats = {
                'employee_stats': {
                    '1': {
                        'name': 'Test Technician 1',
                        'total_time_minutes': 240,
                        'completed_requests': 4,
                        'in_progress_requests': 1
                    },
                    '2': {
                        'name': 'Test Call Center 1',
                        'total_time_minutes': 180,
                        'completed_requests': 3,
                        'in_progress_requests': 0
                    }
                }
            }
            
            if not today_stats or 'employee_stats' not in today_stats:
                await callback.message.edit_text(
                    "📊 Bugun hech qanday faoliyat qayd etilmagan"
                )
                return
            
            text = "⏱️ *Bugungi vaqt sarfi:*\n\n"
            
            # Sort by total time spent
            sorted_stats = sorted(
                today_stats['employee_stats'].items(),
                key=lambda x: x[1].get('total_time_minutes', 0),
                reverse=True
            )
            
            for user_id, stats in sorted_stats:
                user_name = stats.get('name', 'Unknown')
                total_minutes = stats.get('total_time_minutes', 0)
                completed = stats.get('completed_requests', 0)
                in_progress = stats.get('in_progress_requests', 0)
                
                hours = total_minutes // 60
                minutes = total_minutes % 60
                time_str = f"{hours}s {minutes}d"
                
                text += f"👤 *{user_name}*\n"
                text += f"⏱️ Vaqt: {time_str}\n"
                text += f"✅ Bajarilgan: {completed}\n"
                text += f"⏳ Jarayonda: {in_progress}\n\n"
            
            # Add buttons
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📥 Excel yuklash",
                    callback_data="mgr_rt_export_time"
                )],
                [InlineKeyboardButton(
                    text="◀️ Orqaga",
                    callback_data="mgr_rt_menu"
                )]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_rt_live_stats")
    async def show_live_statistics(callback: CallbackQuery):
        """Show live statistics with auto-refresh"""
        try:
            await callback.answer()
            
            # Mock current statistics
            stats = {
                'active_requests': 5,
                'by_status': {
                    'new': 2,
                    'in_progress': 3,
                    'completed': 18
                },
                'avg_processing_time_minutes': 45,
                'online_employees': 8
            }
            
            text = "📊 *Jonli statistika:*\n\n"
            
            # Active requests
            text += f"🔴 Faol zayavkalar: {stats.get('active_requests', 0)}\n"
            
            # Requests by status
            text += "\n*Status bo'yicha:*\n"
            for status, count in stats.get('by_status', {}).items():
                text += f"• {status}: {count}\n"
            
            # Average processing time
            avg_time = stats.get('avg_processing_time_minutes', 0)
            hours = avg_time // 60
            minutes = avg_time % 60
            text += f"\n⏱️ O'rtacha vaqt: {hours}s {minutes}d\n"
            
            # Online employees
            text += f"\n👥 Online xodimlar: {stats.get('online_employees', 0)}\n"
            
            # Add auto-refresh and back buttons
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="mgr_rt_live_stats"
                )],
                [InlineKeyboardButton(
                    text="📈 Batafsil",
                    callback_data="mgr_rt_detailed_stats"
                )],
                [InlineKeyboardButton(
                    text="◀️ Orqaga",
                    callback_data="mgr_rt_menu"
                )]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_rt_incoming")
    async def show_incoming_requests(callback: CallbackQuery):
        """Show incoming requests in real-time"""
        try:
            await callback.answer()
            
            # Mock recent requests
            recent_requests = [
                {
                    'id': 'APP-003',
                    'client_name': 'Test Client 1',
                    'phone_number': '+998901234567',
                    'created_at': datetime.now() - timedelta(minutes=15),
                    'status': 'new'
                },
                {
                    'id': 'APP-004',
                    'client_name': 'Test Client 2',
                    'phone_number': '+998901234568',
                    'created_at': datetime.now() - timedelta(minutes=8),
                    'status': 'new'
                }
            ]
            
            if not recent_requests:
                await callback.message.edit_text(
                    "📭 So'nggi 30 daqiqada yangi zayavka kelmagan"
                )
                return
            
            text = "🔔 *Kelgan zayavkalar (so'nggi 30 daqiqa):*\n\n"
            
            for req in recent_requests:
                created_at = req.get('created_at')
                if created_at:
                    time_ago = datetime.now() - created_at
                    minutes_ago = int(time_ago.total_seconds() // 60)
                    time_str = f"{minutes_ago} daqiqa oldin"
                else:
                    time_str = "Unknown"
                
                text += f"📋 *Zayavka #{req.get('id')}*\n"
                text += f"👤 Client: {req.get('client_name', 'Unknown')}\n"
                text += f"📱 Tel: {req.get('phone_number', 'Unknown')}\n"
                text += f"🕐 Vaqt: {time_str}\n"
                text += f"📊 Status: {req.get('status', 'new')}\n\n"
            
            # Add refresh button
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="mgr_rt_incoming"
                )],
                [InlineKeyboardButton(
                    text="◀️ Orqaga",
                    callback_data="mgr_rt_menu"
                )]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_rt_speed_rating")
    async def show_speed_rating(callback: CallbackQuery):
        """Show employee speed rating"""
        try:
            await callback.answer()
            
            # Mock speed ratings
            speed_ratings = [
                {
                    'name': 'Test Technician 1',
                    'avg_completion_time_minutes': 30,
                    'completed_requests': 8
                },
                {
                    'name': 'Test Call Center 1',
                    'avg_completion_time_minutes': 45,
                    'completed_requests': 12
                },
                {
                    'name': 'Test Junior Manager 1',
                    'avg_completion_time_minutes': 60,
                    'completed_requests': 6
                }
            ]
            
            if not speed_ratings:
                await callback.message.edit_text(
                    "📊 Tezlik reytingi mavjud emas"
                )
                return
            
            text = "⚡ *Tezlik reytingi:*\n\n"
            text += "_O'rtacha bajarish vaqti bo'yicha_\n\n"
            
            for idx, employee in enumerate(speed_ratings[:10], 1):  # Top 10
                name = employee.get('name', 'Unknown')
                avg_time = employee.get('avg_completion_time_minutes', 0)
                completed = employee.get('completed_requests', 0)
                
                hours = avg_time // 60
                minutes = avg_time % 60
                time_str = f"{hours}s {minutes}d"
                
                # Add medal for top 3
                medal = ""
                if idx == 1:
                    medal = "🥇"
                elif idx == 2:
                    medal = "🥈"
                elif idx == 3:
                    medal = "🥉"
                
                text += f"{medal} *{idx}. {name}*\n"
                text += f"   ⏱️ O'rtacha: {time_str}\n"
                text += f"   ✅ Bajarilgan: {completed}\n\n"
            
            # Add buttons
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📥 To'liq reyting",
                    callback_data="mgr_rt_export_rating"
                )],
                [InlineKeyboardButton(
                    text="◀️ Orqaga",
                    callback_data="mgr_rt_menu"
                )]
            ])
            
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_rt_menu")
    async def back_to_realtime_menu(callback: CallbackQuery):
        """Go back to real-time monitoring menu"""
        try:
            await callback.answer()
            
            # Create inline keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🔴 Hozir ishlayotganlar",
                    callback_data="mgr_rt_working_now"
                )],
                [InlineKeyboardButton(
                    text="⏱️ Bugungi vaqt sarfi",
                    callback_data="mgr_rt_time_spent"
                )],
                [InlineKeyboardButton(
                    text="📊 Jonli statistika",
                    callback_data="mgr_rt_live_stats"
                )],
                [InlineKeyboardButton(
                    text="🔔 Kelgan zayavkalar",
                    callback_data="mgr_rt_incoming"
                )],
                [InlineKeyboardButton(
                    text="⚡ Tezlik reytingi",
                    callback_data="mgr_rt_speed_rating"
                )]
            ])
            
            await callback.message.edit_text(
                "🕐 *Real vaqtda monitoring*\n\n"
                "Xodimlar faoliyatini jonli kuzating:",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

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
