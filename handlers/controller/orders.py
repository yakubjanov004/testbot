from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from utils.reply_utils import (
    send_or_edit_message,
    answer_callback_query,
    reply_with_error,
    reply_with_success,
    reply_with_info,
    send_list_message,
    clear_message_state
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

async def get_all_orders(limit: int = 50):
    """Mock all orders data"""
    return [
        {
            'id': 1,
            'status': 'new',
            'client_name': 'Client 1',
            'description': 'Test order 1',
            'created_at': '2024-01-15 10:30:00'
        },
        {
            'id': 2,
            'status': 'assigned',
            'client_name': 'Client 2',
            'description': 'Test order 2',
            'created_at': '2024-01-15 11:00:00'
        },
        {
            'id': 3,
            'status': 'completed',
            'client_name': 'Client 3',
            'description': 'Test order 3',
            'created_at': '2024-01-15 09:00:00'
        }
    ]

async def get_orders_by_status(statuses: list):
    """Mock orders by status"""
    all_orders = await get_all_orders()
    return [order for order in all_orders if order['status'] in statuses]

async def update_order_priority(order_id: int, priority: str):
    """Mock update order priority"""
    return True

async def get_unresolved_issues():
    """Mock unresolved issues"""
    return [
        {
            'id': 1,
            'client_name': 'Client 1',
            'description': 'Problem with order 1',
            'days_pending': 3
        },
        {
            'id': 2,
            'client_name': 'Client 2',
            'description': 'Problem with order 2',
            'days_pending': 5
        }
    ]

async def get_single_order_details(order_id: int):
    """Mock single order details"""
    return {
        'id': order_id,
        'status': 'new',
        'client_name': f'Client {order_id}',
        'description': f'Test order {order_id}',
        'created_at': '2024-01-15 10:30:00',
        'priority': 'normal'
    }

# Removed duplicate get_role_router - using centralized version from utils.role_system

# Mock keyboards
def orders_control_menu(lang: str):
    """Mock orders control menu keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_controllers")
        ]
    ])

def order_priority_keyboard(order_id: int):
    """Mock order priority keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔴 Yuqori", callback_data=f"priority_high_{order_id}"),
            InlineKeyboardButton(text="🟡 O'rtacha", callback_data=f"priority_medium_{order_id}")
        ],
        [
            InlineKeyboardButton(text="🟢 Past", callback_data=f"priority_low_{order_id}")
        ],
        [
            InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_orders")
        ]
    ])

def back_to_controllers_menu():
    """Mock back to controllers menu keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_controllers")]
    ])

# Mock states
class ControllerOrdersStates:
    orders_control = "orders_control"
    viewing_orders = "viewing_orders"
    order_details = "order_details"

def get_controller_orders_router():
    """Get controller orders router"""
    from utils.role_system import get_role_router
    router = get_role_router("controller")

    @router.message(F.text.in_(["📋 Buyurtmalar nazorati"]))
    async def orders_control_menu_handler(message: Message, state: FSMContext):
        """Buyurtmalar nazorati menyusi"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                return await reply_with_error(message, state, "Sizda controller huquqi yo'q.")
                
            lang = user.get('language', 'uz')
            await state.set_state(ControllerOrdersStates.orders_control)
            orders = await get_all_orders(limit=50)
            status_counts = {}
            for order in orders:
                status = order['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            text = (
                "📋 <b>Buyurtmalar nazorati</b>\n\n"
                "📊 <b>Holat bo'yicha:</b>\n"
                f"• Yangi: {status_counts.get('new', 0)}\n"
                f"• Tayinlangan: {status_counts.get('assigned', 0)}\n"
                f"• Jarayonda: {status_counts.get('in_progress', 0)}\n"
                f"• Bajarilgan: {status_counts.get('completed', 0)}\n"
                f"• Bekor qilingan: {status_counts.get('cancelled', 0)}\n\n"
                "Kerakli amalni tanlang:"
            )
            
            await send_or_edit_message(
                message,
                text,
                state,
                reply_markup=orders_control_menu(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in orders_control_menu_handler: {e}")
            await reply_with_error(message, state, "Xatolik yuz berdi")

    @router.message(F.text.in_(["🆕 Yangi buyurtmalar"]))
    async def show_new_orders(message: Message, state: FSMContext):
        """Yangi buyurtmalarni ko'rsatish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                return await reply_with_error(message, state, "Sizda controller huquqi yo'q.")
            
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
            
            await send_or_edit_message(
                message,
                text,
                state,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in show_new_orders: {e}")
            await reply_with_error(message, state, "Xatolik yuz berdi")

    @router.message(F.text.in_(["⏳ Kutilayotgan"]))
    async def show_pending_orders(message: Message, state: FSMContext):
        """Kutilayotgan buyurtmalarni ko'rsatish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                return await reply_with_error(message, state, "Sizda controller huquqi yo'q.")
            
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
            
            await send_or_edit_message(
                message,
                text,
                state,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in show_pending_orders: {e}")
            await reply_with_error(message, state, "Xatolik yuz berdi")

    @router.message(F.text.in_(["🔴 Muammoli buyurtmalar"]))
    async def show_problem_orders(message: Message, state: FSMContext):
        """Muammoli buyurtmalarni ko'rsatish"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                return await reply_with_error(message, state, "Sizda controller huquqi yo'q.")
            
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
            
            await send_or_edit_message(
                message,
                text,
                state,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in show_problem_orders: {e}")
            await reply_with_error(message, state, "Xatolik yuz berdi")

    @router.message(F.text.in_(["📊 Buyurtmalar hisoboti"]))
    async def orders_report(message: Message, state: FSMContext):
        """Buyurtmalar hisoboti"""
        user_id = message.from_user.id
        
        try:
            user = await get_user_by_telegram_id(user_id)
            if not user or user['role'] != 'controller':
                return await reply_with_error(message, state, "Sizda controller huquqi yo'q.")
            
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
            
            await send_or_edit_message(
                message,
                text,
                state,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in orders_report: {e}")
            await reply_with_error(message, state, "Xatolik yuz berdi")

    return router
