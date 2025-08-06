"""
Controller Orders Handler
Manages orders for controller
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from filters.role_filter import RoleFilter

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

async def get_all_orders(limit: int = 50):
    """Mock get all orders"""
    return [
        {
            'id': 1,
            'order_number': 'ORD-001',
            'client_name': 'Test Client 1',
            'service_type': 'Internet xizmati',
            'status': 'Yangi',
            'priority': 'Yuqori',
            'created_at': '2024-01-15 10:30',
            'assigned_to': 'Aziz Karimov'
        },
        {
            'id': 2,
            'order_number': 'ORD-002',
            'client_name': 'Test Client 2',
            'service_type': 'TV xizmati',
            'status': 'Jarayonda',
            'priority': 'O\'rta',
            'created_at': '2024-01-15 09:15',
            'assigned_to': 'Malika Yusupova'
        }
    ]

async def get_orders_by_status(statuses: list):
    """Mock get orders by status"""
    return await get_all_orders()

async def update_order_priority(order_id: int, priority: str):
    """Mock update order priority"""
    return True

async def get_unresolved_issues():
    """Mock get unresolved issues"""
    return [
        {
            'id': 1,
            'order_number': 'ORD-003',
            'client_name': 'Test Client 3',
            'issue_type': 'Texnik muammo',
            'description': 'Internet uzulish',
            'priority': 'Shoshilinch',
            'created_at': '2024-01-15 08:00'
        }
    ]

async def get_single_order_details(order_id: int):
    """Mock get single order details"""
    return {
        'id': order_id,
        'order_number': f'ORD-{order_id:03d}',
        'client_name': f'Test Client {order_id}',
        'service_type': 'Internet xizmati',
        'status': 'Yangi',
        'priority': 'Yuqori',
        'created_at': '2024-01-15 10:30',
        'assigned_to': 'Aziz Karimov',
        'description': 'Test order description'
    }

def orders_control_menu(lang: str):
    """Create orders control menu"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🆕 Yangi buyurtmalar", callback_data="new_orders"),
            InlineKeyboardButton(text="⏳ Kutilayotgan", callback_data="pending_orders")
        ],
        [
            InlineKeyboardButton(text="🔴 Muammoli buyurtmalar", callback_data="problem_orders"),
            InlineKeyboardButton(text="📊 Buyurtmalar hisoboti", callback_data="orders_report")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_controllers")
        ]
    ])

def order_priority_keyboard(order_id: int):
    """Create order priority keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🟢 Past", callback_data=f"priority_low_{order_id}"),
            InlineKeyboardButton(text="🟡 O'rta", callback_data=f"priority_medium_{order_id}")
        ],
        [
            InlineKeyboardButton(text="🟠 Yuqori", callback_data=f"priority_high_{order_id}"),
            InlineKeyboardButton(text="🔴 Shoshilinch", callback_data=f"priority_urgent_{order_id}")
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_orders")
        ]
    ])

def back_to_controllers_menu():
    """Create back to controllers menu"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_controllers")]
    ])

class ControllerOrdersStates:
    orders_control = "orders_control"
    viewing_orders = "viewing_orders"
    order_details = "order_details"

def get_controller_orders_router():
    """Get controller orders router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📋 Buyurtmalar nazorati"]))
    async def orders_control_menu_handler(message: Message, state: FSMContext):
        """Handle orders control menu"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            # Get orders statistics
            all_orders = await get_all_orders()
            new_orders = [o for o in all_orders if o['status'] == 'Yangi']
            pending_orders = [o for o in all_orders if o['status'] == 'Jarayonda']
            problem_orders = await get_unresolved_issues()
            
            stats_text = (
                "📋 <b>Buyurtmalar nazorati</b>\n\n"
                "📊 <b>Statistika:</b>\n"
                f"• Jami buyurtmalar: {len(all_orders)}\n"
                f"• Yangi buyurtmalar: {len(new_orders)}\n"
                f"• Kutilayotgan: {len(pending_orders)}\n"
                f"• Muammoli: {len(problem_orders)}\n\n"
                "Kerakli bo'limni tanlang:"
            )
            
            await message.answer(
                stats_text,
                reply_markup=orders_control_menu(lang),
                parse_mode='HTML'
            )
            await state.set_state(ControllerOrdersStates.orders_control)
            
        except Exception as e:
            print(f"Error in orders_control_menu_handler: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["🆕 Yangi buyurtmalar"]))
    async def show_new_orders(message: Message, state: FSMContext):
        """Yangi buyurtmalarni ko'rsatish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            orders = await get_orders_by_status(['new'])
            
            text = "🆕 <b>Yangi buyurtmalar:</b>\n\n"
            
            if orders:
                for order in orders[:10]:  # Faqat 10 tasini ko'rsatish
                    client_name = order.get('client_name', 'Noma\'lum')
                    created_at = order.get('created_at', '')
                    description = order.get('description', '')[:50] + "..." if len(order.get('description', '')) > 50 else order.get('description', '')
                    
                    text += f"🔹 <b>#{order['id']}</b> - {client_name}\n"
                    text += f"📝 {description}\n"
                    text += f"📅 {created_at}\n\n"
            else:
                no_orders_text = "Yangi buyurtmalar yo'q"
                text += no_orders_text
            
            await message.answer(
                text,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in show_new_orders: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["⏳ Kutilayotgan"]))
    async def show_pending_orders(message: Message, state: FSMContext):
        """Kutilayotgan buyurtmalarni ko'rsatish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            orders = await get_orders_by_status(['pending', 'assigned'])
            
            text = "⏳ <b>Kutilayotgan buyurtmalar:</b>\n\n"
            
            if orders:
                for order in orders[:10]:
                    client_name = order.get('client_name', 'Noma\'lum')
                    technician_name = order.get('technician_name', 'Tayinlanmagan')
                    created_at = order.get('created_at', '')
                    
                    text += f"🔸 <b>#{order['id']}</b> - {client_name}\n"
                    text += f"👨‍🔧 Texnik: {technician_name}\n"
                    text += f"📅 {created_at}\n\n"
            else:
                no_orders_text = "Kutilayotgan buyurtmalar yo'q"
                text += no_orders_text
            
            await message.answer(
                text,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in show_pending_orders: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["🔴 Muammoli buyurtmalar"]))
    async def show_problem_orders(message: Message, state: FSMContext):
        """Muammoli buyurtmalarni ko'rsatish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            issues = await get_unresolved_issues()
            
            text = "🔴 <b>Muammoli buyurtmalar:</b>\n\n"
            
            if issues:
                for issue in issues[:10]:
                    client_name = issue.get('client_name', 'Noma\'lum')
                    days_pending = issue.get('days_pending', 0)
                    description = issue.get('description', '')[:50] + "..." if len(issue.get('description', '')) > 50 else issue.get('description', '')
                    
                    text += f"🔴 <b>#{issue['id']}</b> - {client_name}\n"
                    text += f"📝 {description}\n"
                    
                    pending_text = "kun kutmoqda"
                    text += f"⏱️ {days_pending} {pending_text}\n\n"
            else:
                no_issues_text = "Muammoli buyurtmalar yo'q"
                text += no_issues_text
            
            await message.answer(
                text,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in show_problem_orders: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.message(F.text.in_(["📊 Buyurtmalar hisoboti"]))
    async def orders_report(message: Message, state: FSMContext):
        """Buyurtmalar hisoboti"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            orders = await get_all_orders(limit=100)
            
            # Statistikani hisoblash
            total_orders = len(orders)
            completed_orders = len([o for o in orders if o['status'] == 'completed'])
            pending_orders = len([o for o in orders if o['status'] in ['new', 'pending', 'assigned']])
            in_progress_orders = len([o for o in orders if o['status'] == 'in_progress'])
            
            completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
            
            text = f"""📊 <b>Buyurtmalar hisoboti</b>

📈 <b>Umumiy ko'rsatkichlar:</b>
• Jami buyurtmalar: {total_orders}
• Bajarilgan: {completed_orders}
• Jarayonda: {in_progress_orders}
• Kutilayotgan: {pending_orders}

📊 <b>Samaradorlik:</b>
• Bajarish foizi: {completion_rate:.1f}%

📅 <b>Sana:</b> {message.date.strftime('%d.%m.%Y %H:%M')}"""
            
            await message.answer(
                text,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in orders_report: {e}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    return router
