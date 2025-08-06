"""
Call Center Supervisor Workflow Management Handler

This module handles workflow management functionality for call center supervisors,
including workflow monitoring, process optimization, and team coordination.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from keyboards.call_center_supervisor_buttons import (
    get_workflow_management_menu, get_process_monitoring_menu,
    get_workflow_optimization_menu, get_team_coordination_menu,
    get_workflow_menu
)
from states.call_center_supervisor_states import CallCenterSupervisorWorkflowStates

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'call_center_supervisor',
        'language': 'uz',
        'full_name': 'Test Supervisor'
    }

async def get_user_lang(user_id: int) -> str:
    """Mock user language"""
    return 'uz'

async def get_role_router(role: str):
    """Mock role router"""
    from aiogram import Router
    return Router()



async def get_call_center_supervisor_orders(supervisor_id: int, limit: int = 50, status: str = None):
    """Mock supervisor orders"""
    return [
        {
            'id': '12345678',
            'status': 'new',
            'priority': 'high',
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'client_name': 'Test Client',
            'description': 'Internet ulanish muammosi'
        },
        {
            'id': '87654321',
            'status': 'in_progress',
            'priority': 'medium',
            'created_at': datetime.now() - timedelta(hours=2),
            'updated_at': datetime.now(),
            'client_name': 'Another Client',
            'description': 'Televizor signallari yo\'q'
        }
    ]

async def get_supervised_staff_performance(supervisor_id: int):
    """Mock staff performance"""
    return [
        {
            'id': 1,
            'full_name': 'Operator 1',
            'total_orders': 15,
            'completed_orders': 12,
            'active_orders': 3
        },
        {
            'id': 2,
            'full_name': 'Operator 2',
            'total_orders': 8,
            'completed_orders': 7,
            'active_orders': 1
        }
    ]

async def get_supervisor_dashboard_stats(supervisor_id: int):
    """Mock dashboard stats"""
    return {
        'total_orders': 25,
        'completed_today': 8,
        'active_orders': 12,
        'issues': 2
    }

async def assign_order_to_staff(order_id: str, staff_id: int, supervisor_id: int, note: str = None):
    """Mock assign order"""
    return True

async def get_workflow_performance_metrics(supervisor_id: int, days: int = 7):
    """Mock performance metrics"""
    return {
        'metrics': {
            'total_processed': 45,
            'completed': 38,
            'issues': 3,
            'avg_processing_hours': 2.5
        },
        'hourly_distribution': {
            9: 5, 10: 8, 11: 12, 12: 6, 13: 4, 14: 7, 15: 9, 16: 6, 17: 3
        }
    }

async def get_workflow_bottlenecks(supervisor_id: int):
    """Mock workflow bottlenecks"""
    return {
        'status_bottlenecks': [
            {'status': 'new', 'count': 5, 'avg_hours_stuck': 1.5},
            {'status': 'in_progress', 'count': 3, 'avg_hours_stuck': 4.2}
        ],
        'overloaded_staff': [
            {'full_name': 'Operator 1', 'active_orders': 8}
        ],
        'priority_issues': {
            'high_priority_waiting': 2
        }
    }

async def get_staff_workload_distribution(supervisor_id: int):
    """Mock workload distribution"""
    return [
        {
            'id': 1,
            'full_name': 'Operator 1',
            'current_workload': 8
        },
        {
            'id': 2,
            'full_name': 'Operator 2',
            'current_workload': 3
        }
    ]

async def optimize_order_assignments(supervisor_id: int, max_assignments: int = 5):
    """Mock optimize assignments"""
    return {
        'assignments_made': 3,
        'total_unassigned': 2,
        'available_staff': 4
    }

def get_call_center_supervisor_workflow_management_router():
    """Get router for call center supervisor workflow management handlers"""
    from utils.role_system import get_role_router
    router = get_role_router("call_center_supervisor")

    @router.message(F.text.in_(["⚙️ Workflow boshqaruvi"]))
    async def workflow_management_menu(message: Message, state: FSMContext):
        """Main workflow management menu"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            
            if not user or user['role'] != 'call_center_supervisor':
                text = "Sizda call center supervisor huquqi yo'q."
                await message.answer(text)
                return
            
            text = f"⚙️ Workflow Boshqaruvi\n\nQuyidagi bo'limlardan birini tanlang:"
            await message.answer(text, reply_markup=get_workflow_menu('uz'))
            
        except Exception as e:
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data.startswith("ccs_workflow_"))
    async def handle_workflow_actions(callback: CallbackQuery, state: FSMContext):
        """Handle workflow management actions"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            action = callback.data.split("_")[-1]
            
            if action == "monitoring":
                await _show_process_monitoring(callback, user['id'])
            elif action == "optimization":
                await _show_workflow_optimization(callback, user['id'])
            elif action == "coordination":
                await _show_team_coordination(callback, user['id'])
            elif action == "analytics":
                await _show_workflow_analytics(callback, user['id'])
            elif action == "automation":
                await _show_automation_options(callback, user['id'])
            else:
                await callback.answer("Noma'lum amal", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ccs_monitor_"))
    async def handle_monitoring_actions(callback: CallbackQuery, state: FSMContext):
        """Handle process monitoring actions"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            monitor_type = callback.data.split("_")[-1]
            
            if monitor_type == "realtime":
                await _show_realtime_monitoring(callback, user['id'])
            elif monitor_type == "bottlenecks":
                await _show_bottleneck_analysis(callback, user['id'])
            elif monitor_type == "performance":
                await _show_performance_monitoring(callback, user['id'])
            elif monitor_type == "alerts":
                await _show_workflow_alerts(callback, user['id'])
            else:
                await callback.answer("Noma'lum monitoring turi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ccs_optimize_"))
    async def handle_optimization_actions(callback: CallbackQuery, state: FSMContext):
        """Handle workflow optimization actions"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            optimize_type = callback.data.split("_")[-1]
            
            if optimize_type == "load":
                await _optimize_workload_distribution(callback, user['id'])
            elif optimize_type == "priority":
                await _optimize_priority_handling(callback, user['id'])
            elif optimize_type == "resources":
                await _optimize_resource_allocation(callback, user['id'])
            elif optimize_type == "schedule":
                await _optimize_scheduling(callback, user['id'])
            else:
                await callback.answer("Noma'lum optimizatsiya turi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ccs_coord_"))
    async def handle_coordination_actions(callback: CallbackQuery, state: FSMContext):
        """Handle team coordination actions"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            coord_type = callback.data.split("_")[-1]
            
            if coord_type == "tasks":
                await _show_task_distribution(callback, user['id'])
            elif coord_type == "communication":
                await _show_communication_optimization(callback, user['id'])
            elif coord_type == "teamwork":
                await _show_teamwork_enhancement(callback, user['id'])
            elif coord_type == "efficiency":
                await _show_team_efficiency(callback, user['id'])
            else:
                await callback.answer("Noma'lum koordinatsiya turi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router


async def _show_process_monitoring(callback: CallbackQuery, supervisor_id: int):
    """Show process monitoring dashboard"""
    try:
        # Get current process status
        orders = await get_call_center_supervisor_orders(supervisor_id, limit=100)
        
        # Analyze current processes
        active_processes = len([o for o in orders if o['status'] in ['new', 'assigned', 'in_progress']])
        completed_today = len([o for o in orders if o['status'] == 'completed' and 
                              o['created_at'].date() == datetime.now().date()])
        issues = len([o for o in orders if o['status'] == 'issue'])
        
        # Calculate average processing time
        completed_orders = [o for o in orders if o['status'] == 'completed' and o.get('updated_at')]
        avg_processing_time = 0
        if completed_orders:
            total_time = sum([(o['updated_at'] - o['created_at']).total_seconds() 
                            for o in completed_orders])
            avg_processing_time = total_time / len(completed_orders) / 3600  # in hours
        
        text = (
            f"📊 Jarayon Monitoringi\n\n"
            f"🔄 FAOL JARAYONLAR:\n"
            f"• Faol buyurtmalar: {active_processes}\n"
            f"• Bugun bajarilgan: {completed_today}\n"
            f"• Muammoli: {issues}\n\n"
            f"⏱️ VAQT TAHLILI:\n"
            f"• O'rtacha ishlov berish: {avg_processing_time:.1f} soat\n\n"
            f"📈 REAL VAQT HOLATI:\n"
            f"• Tizim holati: {'🟢 Normal' if issues < 5 else '🟡 Ehtiyot' if issues < 10 else '🔴 Kritik'}\n"
            f"• Yuklanish: {min(100, active_processes * 2)}%\n\n"
            f"Batafsil monitoring tanlang:"
        )
        
        await callback.message.edit_text(text, reply_markup=get_process_monitoring_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_workflow_optimization(callback: CallbackQuery, supervisor_id: int):
    """Show workflow optimization options"""
    try:
        # Analyze current workflow for optimization opportunities
        staff_performance = await get_supervised_staff_performance(supervisor_id)
        orders = await get_call_center_supervisor_orders(supervisor_id, limit=50)
        
        # Identify optimization opportunities
        overloaded_staff = [s for s in staff_performance if s['total_orders'] > 20]
        underutilized_staff = [s for s in staff_performance if s['total_orders'] < 5]
        high_priority_pending = len([o for o in orders if o.get('priority') == 'high' and o['status'] == 'new'])
        
        text = (
            f"🔧 Workflow Optimizatsiyasi\n\n"
            f"📊 OPTIMIZATSIYA IMKONIYATLARI:\n"
            f"• Ortiqcha yuklangan xodimlar: {len(overloaded_staff)}\n"
            f"• Kam yuklangan xodimlar: {len(underutilized_staff)}\n"
            f"• Yuqori muhimlikdagi kutilayotgan: {high_priority_pending}\n\n"
            f"🎯 TAVSIYA QILINGAN AMALLAR:\n"
        )
        
        # Add recommendations
        if len(overloaded_staff) > 0:
            text += "• Ish yukini qayta taqsimlash\n"
        if high_priority_pending > 0:
            text += "• Muhim arizalarni birinchi navbatda ko'rish\n"
        if len(underutilized_staff) > 0:
            text += "• Resurslarni qayta taqsimlash\n"
        
        text += "\nOptimizatsiya turini tanlang:"
        
        await callback.message.edit_text(text, reply_markup=get_workflow_optimization_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_team_coordination(callback: CallbackQuery, supervisor_id: int):
    """Show team coordination dashboard"""
    try:
        staff_performance = await get_supervised_staff_performance(supervisor_id)
        
        # Analyze team coordination metrics
        total_staff = len(staff_performance)
        active_staff = len([s for s in staff_performance if s['total_orders'] > 0])
        team_efficiency = (sum(s['completed_orders'] for s in staff_performance) / 
                          max(sum(s['total_orders'] for s in staff_performance), 1) * 100)
        
        text = (
            f"👥 Jamoa Koordinatsiyasi\n\n"
            f"📊 JAMOA HOLATI:\n"
            f"• Jami xodimlar: {total_staff}\n"
            f"• Faol xodimlar: {active_staff}\n"
            f"• Jamoa samaradorligi: {team_efficiency:.1f}%\n\n"
            f"🎯 KOORDINATSIYA VAZIFALARI:\n"
            f"• Vazifalarni taqsimlash\n"
            f"• Jamoaviy ishlashni yaxshilash\n"
            f"• Muloqotni optimallashtirish\n"
            f"• Resurslarni muvofiqlashtirish\n\n"
            f"Koordinatsiya turini tanlang:"
        )
        
        await callback.message.edit_text(text, reply_markup=get_team_coordination_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_workflow_analytics(callback: CallbackQuery, supervisor_id: int):
    """Show workflow analytics"""
    try:
        orders = await get_call_center_supervisor_orders(supervisor_id, limit=100)
        
        # Analyze workflow patterns
        hourly_distribution = {}
        status_transitions = {}
        
        for order in orders:
            hour = order['created_at'].hour
            hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1
            
            status = order['status']
            status_transitions[status] = status_transitions.get(status, 0) + 1
        
        # Find peak hours
        peak_hour = max(hourly_distribution.items(), key=lambda x: x[1]) if hourly_distribution else (9, 0)
        
        text = (
            f"📈 Workflow Analitikasi\n\n"
            f"⏰ VAQT TAHLILI:\n"
            f"• Eng yuqori faollik: {peak_hour[0]:02d}:00 ({peak_hour[1]} ariza)\n"
            f"• Ish soatlari taqsimoti:\n"
        )
        
        # Add hourly distribution
        for hour in range(9, 18):  # Working hours
            count = hourly_distribution.get(hour, 0)
            bar = "█" * min(count // 2, 10)
            text += f"  {hour:02d}:00 {bar} {count}\n"
        
        text += f"\n📊 STATUS TAHLILI:\n"
        
        # Add status analysis
        for status, count in sorted(status_transitions.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(orders) * 100) if orders else 0
            text += f"• {status}: {count} ({percentage:.1f}%)\n"
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_automation_options(callback: CallbackQuery, supervisor_id: int):
    """Show workflow automation options"""
    try:
        text = (
            f"🤖 Workflow Avtomatlashtirish\n\n"
            f"🔧 MAVJUD AVTOMATLASHTIRISH:\n"
            f"• Avtomatik tayinlash: Faol\n"
            f"• Muhimlik bo'yicha saralash: Faol\n"
            f"• Eslatmalar: Faol\n\n"
            f"⚙️ QOSHIMCHA IMKONIYATLAR:\n"
            f"• Avtomatik eskalatsiya\n"
            f"• Ish yukini muvozanatlash\n"
            f"• Avtomatik hisobot yaratish\n"
            f"• SLA monitoring\n\n"
            f"🎯 TAVSIYALAR:\n"
            f"• Takrorlanuvchi vazifalarni avtomatlashtirish\n"
            f"• Xatoliklarni kamaytirish\n"
            f"• Samaradorlikni oshirish\n\n"
            f"Avtomatlashtirish sozlamalari tez orada qo'shiladi."
        )
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


# Helper functions for specific workflow operations
async def _show_realtime_monitoring(callback: CallbackQuery, supervisor_id: int):
    """Show real-time monitoring dashboard"""
    try:
        orders = await get_call_center_supervisor_orders(supervisor_id, limit=20)
        
        # Get real-time metrics
        now = datetime.now()
        recent_orders = [o for o in orders if (now - o['created_at']).total_seconds() < 3600]  # Last hour
        
        text = (
            f"📊 Real Vaqt Monitoring\n\n"
            f"⏰ SO'NGGI SOAT ({now.strftime('%H:%M')}):\n"
            f"• Yangi arizalar: {len(recent_orders)}\n"
            f"• Faol jarayonlar: {len([o for o in orders if o['status'] in ['assigned', 'in_progress']])}\n"
            f"• Kutish vaqti: {len([o for o in orders if o['status'] == 'new'])} ariza\n\n"
            f"🔄 JORIY HOLAT:\n"
        )
        
        # Show recent orders
        for order in recent_orders[:5]:
            time_ago = (now - order['created_at']).total_seconds() // 60
            status_emoji = "🆕" if order['status'] == 'new' else "⏳" if order['status'] == 'in_progress' else "✅"
            text += f"{status_emoji} #{order['id']} - {int(time_ago)} daqiqa oldin\n"
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_bottleneck_analysis(callback: CallbackQuery, supervisor_id: int):
    """Show bottleneck analysis"""
    try:
        bottlenecks = await get_workflow_bottlenecks(supervisor_id)
        status_bottlenecks = bottlenecks.get('status_bottlenecks', [])
        overloaded_staff = bottlenecks.get('overloaded_staff', [])
        priority_issues = bottlenecks.get('priority_issues', {})
        
        text = (
            f"🚧 Bottleneck Tahlili\n\n"
            f"⚠️ ANIQLANGAN MUAMMOLAR:\n"
        )
        
        # Status bottlenecks
        if status_bottlenecks:
            text += "📊 Status bo'yicha:\n"
            for bottleneck in status_bottlenecks[:3]:
                status = bottleneck['status']
                count = bottleneck['count']
                hours = bottleneck.get('avg_hours_stuck', 0)
                text += f"• {status}: {count} ta ({hours:.1f} soat)\n"
        
        # Overloaded staff
        if overloaded_staff:
            text += f"\n👥 Ortiqcha yuklangan xodimlar:\n"
            for staff in overloaded_staff[:3]:
                text += f"• {staff['full_name']}: {staff['active_orders']} ta faol\n"
        
        # Priority issues
        high_priority_waiting = priority_issues.get('high_priority_waiting', 0)
        if high_priority_waiting > 0:
            text += f"\n🔴 Yuqori muhimlikdagi kutayotgan: {high_priority_waiting}\n"
        
        if not status_bottlenecks and not overloaded_staff and high_priority_waiting == 0:
            text += "✅ Hozircha bottleneck topilmadi!"
        
        await callback.message.edit_text(text, reply_markup=get_process_monitoring_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_performance_monitoring(callback: CallbackQuery, supervisor_id: int):
    """Show performance monitoring"""
    try:
        metrics_data = await get_workflow_performance_metrics(supervisor_id, days=7)
        metrics = metrics_data.get('metrics', {})
        hourly_dist = metrics_data.get('hourly_distribution', {})
        
        total_processed = metrics.get('total_processed', 0)
        completed = metrics.get('completed', 0)
        completion_rate = (completed / total_processed * 100) if total_processed > 0 else 0
        avg_hours = metrics.get('avg_processing_hours', 0) or 0
        
        text = (
            f"📈 Samaradorlik Monitoringi (7 kun)\n\n"
            f"📊 UMUMIY SAMARADORLIK:\n"
            f"• Jami ishlov berilgan: {total_processed}\n"
            f"• Bajarilgan: {completed}\n"
            f"• Bajarish foizi: {completion_rate:.1f}%\n"
            f"• O'rtacha vaqt: {avg_hours:.1f} soat\n\n"
            f"⏰ SOATLIK FAOLLIK:\n"
        )
        
        # Show hourly distribution
        for hour in range(9, 18):
            count = hourly_dist.get(hour, 0)
            bar = "█" * min(count // 2, 10)
            text += f"{hour:02d}:00 {bar} {count}\n"
        
        await callback.message.edit_text(text, reply_markup=get_process_monitoring_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_workflow_alerts(callback: CallbackQuery, supervisor_id: int):
    """Show workflow alerts"""
    try:
        orders = await get_call_center_supervisor_orders(supervisor_id, limit=50)
        now = datetime.now()
        
        # Generate alerts
        alerts = []
        
        # High priority orders waiting too long
        high_priority_old = [o for o in orders if o.get('priority') == 'high' 
                           and o['status'] == 'new' 
                           and (now - o['created_at']).total_seconds() > 7200]  # 2 hours
        
        if high_priority_old:
            alerts.append({
                'type': 'high_priority_delay',
                'count': len(high_priority_old),
                'message': f"🔴 {len(high_priority_old)} ta yuqori muhimlikdagi ariza 2 soatdan ko'p kutmoqda"
            })
        
        # Orders stuck in progress
        stuck_orders = [o for o in orders if o['status'] == 'in_progress' 
                       and (now - o['created_at']).total_seconds() > 86400]  # 24 hours
        
        if stuck_orders:
            alerts.append({
                'type': 'stuck_orders',
                'count': len(stuck_orders),
                'message': f"⚠️ {len(stuck_orders)} ta buyurtma 24 soatdan ko'p jarayonda"
            })
        
        # Too many new orders
        new_orders = [o for o in orders if o['status'] == 'new']
        if len(new_orders) > 20:
            alerts.append({
                'type': 'too_many_new',
                'count': len(new_orders),
                'message': f"📈 Juda ko'p yangi buyurtmalar: {len(new_orders)}"
            })
        
        text = (
            f"🚨 Workflow Ogohlantirishlari\n\n"
        )
        
        if alerts:
            for alert in alerts:
                text += f"{alert['message']}\n"
        else:
            text += "✅ Hozircha ogohlantirish yo'q!"
        
        text += f"\n⏰ Oxirgi yangilanish: {now.strftime('%H:%M')}"
        
        await callback.message.edit_text(text, reply_markup=get_process_monitoring_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _optimize_workload_distribution(callback: CallbackQuery, supervisor_id: int):
    """Optimize workload distribution among staff"""
    try:
        result = await optimize_order_assignments(supervisor_id, max_assignments=5)
        
        assignments_made = result.get('assignments_made', 0)
        total_unassigned = result.get('total_unassigned', 0)
        available_staff = result.get('available_staff', 0)
        
        if assignments_made > 0:
            text = (
                f"✅ Ish yuki optimizatsiyasi tugallandi!\n\n"
                f"📊 NATIJALAR:\n"
                f"• Tayinlangan buyurtmalar: {assignments_made}\n"
                f"• Jami tayinlanmagan: {total_unassigned}\n"
                f"• Mavjud xodimlar: {available_staff}\n\n"
                f"Ish yuki muvozanatlashtirildi."
            )
        else:
            message = result.get('message', 'No assignments made')
            text = (
                f"ℹ️ Optimizatsiya natijasi:\n\n{message}"
            )
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _optimize_priority_handling(callback: CallbackQuery, supervisor_id: int):
    """Optimize priority handling"""
    try:
        orders = await get_call_center_supervisor_orders(supervisor_id, status='new')
        high_priority = [o for o in orders if o.get('priority') == 'high']
        
        if not high_priority:
            text = (
                "✅ Yuqori muhimlikdagi buyurtmalar yo'q yoki allaqachon tayinlangan."
            )
            await callback.message.edit_text(text)
            await callback.answer()
            return
        
        # Get available staff
        staff_performance = await get_supervised_staff_performance(supervisor_id)
        available_staff = [s for s in staff_performance if s['total_orders'] < 10]
        
        if not available_staff:
            text = (
                "⚠️ Yuqori muhimlikdagi buyurtmalar uchun mavjud xodim yo'q."
            )
            await callback.message.edit_text(text)
            await callback.answer()
            return
        
        # Assign high priority orders to best available staff
        assignments_made = 0
        for order in high_priority[:3]:  # Top 3 high priority orders
            if available_staff:
                # Find staff with best completion rate
                best_staff = max(available_staff, key=lambda s: s['completed_orders'] / max(s['total_orders'], 1))
                
                success = await assign_order_to_staff(order['id'], best_staff['id'], supervisor_id, 
                                                   "High priority optimization assignment")
                if success:
                    assignments_made += 1
                    available_staff.remove(best_staff)
        
        text = (
            f"🎯 Muhimlik Optimizatsiyasi Tugallandi!\n\n"
            f"📊 NATIJALAR:\n"
            f"• Yuqori muhimlikdagi tayinlangan: {assignments_made}\n"
            f"• Jami yuqori muhimlik: {len(high_priority)}\n\n"
            f"Eng yaxshi xodimlarga tayinlandi."
        )
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _optimize_resource_allocation(callback: CallbackQuery, supervisor_id: int):
    """Optimize resource allocation"""
    try:
        workload_data = await get_staff_workload_distribution(supervisor_id)
        
        if not workload_data:
            text = "Resurs taqsimoti ma'lumotlari topilmadi."
            await callback.message.edit_text(text)
            await callback.answer()
            return
        
        # Analyze workload distribution
        total_workload = sum(s['current_workload'] for s in workload_data)
        avg_workload = total_workload / len(workload_data) if workload_data else 0
        
        overloaded = [s for s in workload_data if s['current_workload'] > avg_workload * 1.5]
        underloaded = [s for s in workload_data if s['current_workload'] < avg_workload * 0.5]
        
        text = (
            f"📦 Resurs Taqsimoti Tahlili\n\n"
            f"📊 HOZIRGI HOLAT:\n"
            f"• Jami ish yuki: {total_workload}\n"
            f"• O'rtacha yuk: {avg_workload:.1f}\n"
            f"• Ortiqcha yuklangan: {len(overloaded)}\n"
            f"• Kam yuklangan: {len(underloaded)}\n\n"
            f"🎯 TAVSIYALAR:\n"
        )
        
        if overloaded:
            text += "• Ortiqcha yuklangan xodimlardan vazifalarni qayta taqsimlash\n"
        
        if underloaded:
            text += "• Kam yuklangan xodimlarga qo'shimcha vazifalar berish\n"
        
        if len(overloaded) == 0 and len(underloaded) == 0:
            text += "✅ Resurslar optimal taqsimlangan!"
        
        await callback.message.edit_text(text, reply_markup=get_workflow_optimization_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _optimize_scheduling(callback: CallbackQuery, supervisor_id: int):
    """Optimize scheduling"""
    try:
        metrics_data = await get_workflow_performance_metrics(supervisor_id, days=7)
        hourly_dist = metrics_data.get('hourly_distribution', {})
        
        # Find peak hours
        if hourly_dist:
            peak_hours = sorted(hourly_dist.items(), key=lambda x: x[1], reverse=True)[:3]
            low_hours = sorted(hourly_dist.items(), key=lambda x: x[1])[:3]
        else:
            peak_hours = []
            low_hours = []
        
        text = (
            f"📅 Jadval Optimizatsiyasi\n\n"
            f"⏰ FAOLLIK TAHLILI:\n"
        )
        
        if peak_hours:
            text += "📈 Eng yuqori faollik:\n"
            for hour, count in peak_hours:
                text += f"• {int(hour):02d}:00 - {count} ta ariza\n"
        
        if low_hours:
            text += f"\n📉 Eng past faollik:\n"
            for hour, count in low_hours:
                text += f"• {int(hour):02d}:00 - {count} ta ariza\n"
        
        text += (
            f"\n🎯 JADVAL TAVSIYALARI:\n"
            f"• Yuqori faollik soatlarida ko'proq xodim\n"
            f"• Past faollik soatlarida texnik ishlar\n"
            f"• Tanaffuslarni past faollik vaqtiga moslashtirish\n"
            f"• Navbatchilik jadvalini optimizatsiya qilish"
        )
        
        await callback.message.edit_text(text, reply_markup=get_workflow_optimization_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


# Team coordination helper functions
async def _show_task_distribution(callback: CallbackQuery, supervisor_id: int):
    """Show task distribution interface"""
    try:
        staff_performance = await get_supervised_staff_performance(supervisor_id)
        
        text = (
            f"📋 Vazifa Taqsimoti\n\n"
            f"👥 XODIMLAR HOLATI:\n"
        )
        
        for staff in staff_performance[:5]:
            workload_emoji = "🟢" if staff['total_orders'] < 10 else "🟡" if staff['total_orders'] < 20 else "🔴"
            text += f"{workload_emoji} {staff['full_name']}: {staff['total_orders']} vazifa\n"
        
        text += (
            f"\n🎯 TAQSIMLASH STRATEGIYASI:\n"
            f"• Ish yukini muvozanatlash\n"
            f"• Xodimlar qobiliyatiga mos tayinlash\n"
            f"• Muhimlik darajasini hisobga olish"
        )
        
        await callback.message.edit_text(text, reply_markup=get_team_coordination_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_communication_optimization(callback: CallbackQuery, supervisor_id: int):
    """Show communication optimization"""
    try:
        text = (
            f"💬 Muloqot Optimizatsiyasi\n\n"
            f"📊 HOZIRGI MULOQOT KANALLARI:\n"
            f"• Telegram bot: Faol\n"
            f"• Ichki xabarlar: Faol\n"
            f"• Eslatmalar: Faol\n\n"
            f"🎯 YAXSHILASH TAVSIYALARI:\n"
            f"• Tezkor javob berish\n"
            f"• Aniq ko'rsatmalar berish\n"
            f"• Muntazam holat yangilanishlari\n"
            f"• Feedback tizimini yaxshilash"
        )
        
        await callback.message.edit_text(text, reply_markup=get_team_coordination_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_teamwork_enhancement(callback: CallbackQuery, supervisor_id: int):
    """Show teamwork enhancement options"""
    try:
        text = (
            f"🤝 Jamoaviy Ishlashni Yaxshilash\n\n"
            f"📊 JAMOA SAMARADORLIGI:\n"
            f"• Hamkorlik darajasi: Yaxshi\n"
            f"• Ma'lumot almashish: Faol\n"
            f"• Bir-birini qo'llab-quvvatlash: Yaxshi\n\n"
            f"🎯 YAXSHILASH YO'LLARI:\n"
            f"• Jamoa uchrashuvlari\n"
            f"• Bilim almashish seansları\n"
            f"• Mentorlik dasturlari\n"
            f"• Jamoa building tadbirlari"
        )
        
        await callback.message.edit_text(text, reply_markup=get_team_coordination_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_team_efficiency(callback: CallbackQuery, supervisor_id: int):
    """Show team efficiency metrics"""
    try:
        staff_performance = await get_supervised_staff_performance(supervisor_id)
        
        if not staff_performance:
            text = "Jamoa samaradorligi ma'lumotlari topilmadi."
            await callback.message.edit_text(text)
            await callback.answer()
            return
        
        # Calculate team metrics
        total_orders = sum(s['total_orders'] for s in staff_performance)
        total_completed = sum(s['completed_orders'] for s in staff_performance)
        team_efficiency = (total_completed / total_orders * 100) if total_orders > 0 else 0
        
        text = (
            f"📊 Jamoa Samaradorligi\n\n"
            f"🎯 UMUMIY KO'RSATKICHLAR:\n"
            f"• Jamoa samaradorligi: {team_efficiency:.1f}%\n"
            f"• Jami vazifalar: {total_orders}\n"
            f"• Bajarilgan: {total_completed}\n"
            f"• Faol xodimlar: {len(staff_performance)}\n\n"
            f"👥 INDIVIDUAL NATIJALAR:\n"
        )
        
        # Show top performers
        sorted_staff = sorted(staff_performance, key=lambda s: s['completed_orders'], reverse=True)
        for i, staff in enumerate(sorted_staff[:3], 1):
            efficiency = (staff['completed_orders'] / max(staff['total_orders'], 1) * 100)
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            text += f"{medal} {staff['full_name']}: {efficiency:.1f}%\n"
        
        await callback.message.edit_text(text, reply_markup=get_team_coordination_menu('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)