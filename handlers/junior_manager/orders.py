"""
Junior Manager Orders Handler - Soddalashtirilgan versiya

Bu modul junior manager uchun buyurtmalar va arizalar boshqaruvi funksionalligini o'z ichiga oladi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567'
    }

async def send_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock send and track"""
    return await message_func(text, **kwargs)

async def edit_and_track(message_func, text: str, user_id: int, **kwargs):
    """Mock edit and track"""
    return await message_func(text, **kwargs)

async def get_junior_manager_orders(junior_manager_id: int, limit: int = 50):
    """Mock junior manager orders"""
    from datetime import datetime
    return [
        {
            'id': 1,
            'client_name': 'Aziz Karimov',
            'client_phone': '+998901234567',
            'address': 'Tashkent, Chorsu',
            'description': 'Internet ulanish arizasi',
            'priority': 'medium',
            'status': 'pending',
            'created_at': datetime.now()
        },
        {
            'id': 2,
            'client_name': 'Malika Toshmatova',
            'client_phone': '+998901234568',
            'address': 'Tashkent, Yunusabad',
            'description': 'TV signal muammosi',
            'priority': 'high',
            'status': 'in_progress',
            'created_at': datetime.now()
        }
    ]

async def get_order_details(order_id: int):
    """Mock get order details"""
    return {
        'id': order_id,
        'client_name': 'Aziz Karimov',
        'client_phone': '+998901234567',
        'address': 'Tashkent, Chorsu',
        'description': 'Internet ulanish arizasi',
        'status': 'pending',
        'priority': 'medium',
        'created_at': datetime.now()
    }

async def update_order_status(order_id: int, status: str):
    """Mock update order status"""
    return True

# Mock keyboard functions
def get_orders_menu_keyboard(lang: str = 'uz'):
    """Mock orders menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Barcha arizalar", callback_data="jm_orders_all"),
            InlineKeyboardButton(text="⏳ Kutilayotgan", callback_data="jm_orders_pending")
        ],
        [
            InlineKeyboardButton(text="🔄 Jarayonda", callback_data="jm_orders_progress"),
            InlineKeyboardButton(text="✅ Bajarilgan", callback_data="jm_orders_completed")
        ],
        [
            InlineKeyboardButton(text="🔍 Qidirish", callback_data="jm_orders_search"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="jm_orders_stats")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_main")
        ]
    ])

def get_order_details_keyboard(order_id: int, lang: str = 'uz'):
    """Mock order details keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📞 Mijozni chaqirish", callback_data=f"jm_call_client_{order_id}"),
            InlineKeyboardButton(text="📝 Izoh qo'shish", callback_data=f"jm_add_comment_{order_id}")
        ],
        [
            InlineKeyboardButton(text="🔄 Holatni o'zgartirish", callback_data=f"jm_change_status_{order_id}"),
            InlineKeyboardButton(text="📤 Controllerga yuborish", callback_data=f"jm_forward_{order_id}")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_orders")
        ]
    ])

# Mock states
from aiogram.fsm.state import State, StatesGroup

class JuniorManagerOrdersStates(StatesGroup):
    viewing_orders = State()
    viewing_order_details = State()
    adding_comment = State()
    changing_status = State()

def get_junior_manager_orders_router():
    """Get router for junior manager orders handlers"""
    router = Router()

    @router.message(F.text.in_(["📋 Zayavkalarni ko'rish"]))
    async def view_orders(message: Message, state: FSMContext):
        """Show orders menu for junior manager"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await send_and_track(
                    message.answer,
                    "Sizda ruxsat yo'q.",
                    message.from_user.id
                )
                return

            lang = user.get('language', 'uz')
            
            # Build orders menu text
            text = """📋 **Zayavkalar boshqaruvi**

Mavjud arizalarni ko'rish va boshqarish uchun quyidagi bo'limlardan birini tanlang:"""
            
            # Create keyboard
            keyboard = get_orders_menu_keyboard(lang)
            
            # Send message
            await send_and_track(
                message.answer,
                text,
                message.from_user.id,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in view_orders: {e}")
            await send_and_track(
                message.answer,
                "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
                message.from_user.id
            )

    @router.callback_query(F.data.startswith("jm_orders_"))
    async def handle_orders_actions(callback: CallbackQuery, state: FSMContext):
        """Handle orders action buttons"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            action = callback.data.split("_")[-1]
            
            if action == "all":
                await _show_all_orders(callback, user['id'], lang)
            elif action == "pending":
                await _show_pending_orders(callback, user['id'], lang)
            elif action == "progress":
                await _show_progress_orders(callback, user['id'], lang)
            elif action == "completed":
                await _show_completed_orders(callback, user['id'], lang)
            elif action == "search":
                await _show_search_orders(callback, lang)
            elif action == "stats":
                await _show_orders_stats(callback, user['id'], lang)
            else:
                await callback.answer("Noto'g'ri amal", show_alert=True)
            
        except Exception as e:
            print(f"Error in handle_orders_actions: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("view_order:"))
    async def view_order_details(callback: CallbackQuery, state: FSMContext):
        """View specific order details"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'junior_manager':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            order_id = int(callback.data.split(":")[-1])
            
            # Get order details
            order_details = await get_order_details(order_id)
            if not order_details:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Build order details text
            status_emoji = _get_status_emoji(order_details.get('status', 'pending'))
            priority_emoji = "⚡" if order_details.get('priority') == 'urgent' else "📋"
            
            text = f"""📋 **Ariza #{order_details['id']}**

👤 **Mijoz:** {order_details.get('client_name', 'N/A')}
📱 **Telefon:** {order_details.get('client_phone', 'N/A')}
📍 **Manzil:** {order_details.get('address', 'N/A')}
📝 **Izoh:** {order_details.get('description', 'N/A')}
⚡ **Daraja:** {priority_emoji} {order_details.get('priority', 'medium')}
📊 **Holat:** {status_emoji} {order_details.get('status', 'pending')}
📅 **Sana:** {order_details.get('created_at', 'N/A')}"""
            
            # Create keyboard
            keyboard = get_order_details_keyboard(order_id, lang)
            
            await edit_and_track(
                callback.message.edit_text,
                text,
                callback.from_user.id,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in view_order_details: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    async def _show_all_orders(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show all orders"""
        try:
            orders = await get_junior_manager_orders(junior_manager_id, limit=1000)
            
            if orders:
                text = f"""📋 **Barcha arizalar ({len(orders)} ta)**

"""
                for order in orders[:10]:  # Show first 10
                    status_emoji = _get_status_emoji(order.get('status', 'pending'))
                    text += f"{status_emoji} **#{order['id']}** - {order.get('client_name', 'N/A')}\n"
                
                if len(orders) > 10:
                    text += f"\n... va yana {len(orders) - 10} ta ariza"
            else:
                text = "📋 Hozircha arizalar yo'q"
            
            # Create keyboard
            keyboard = _create_orders_list_keyboard(orders[:5], lang)
            
            await edit_and_track(
                callback.message.edit_text,
                text,
                callback.from_user.id,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_all_orders: {e}")

    async def _show_pending_orders(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show pending orders"""
        try:
            orders = await get_junior_manager_orders(junior_manager_id, limit=1000)
            pending_orders = [order for order in orders if order.get('status') == 'pending']
            
            if pending_orders:
                text = f"""⏳ **Kutilayotgan arizalar ({len(pending_orders)} ta)**

"""
                for order in pending_orders[:10]:
                    text += f"⏳ **#{order['id']}** - {order.get('client_name', 'N/A')}\n"
                
                if len(pending_orders) > 10:
                    text += f"\n... va yana {len(pending_orders) - 10} ta ariza"
            else:
                text = "⏳ Kutilayotgan arizalar yo'q"
            
            # Create keyboard
            keyboard = _create_orders_list_keyboard(pending_orders[:5], lang)
            
            await edit_and_track(
                callback.message.edit_text,
                text,
                callback.from_user.id,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_pending_orders: {e}")

    async def _show_progress_orders(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show in-progress orders"""
        try:
            orders = await get_junior_manager_orders(junior_manager_id, limit=1000)
            progress_orders = [order for order in orders if order.get('status') == 'in_progress']
            
            if progress_orders:
                text = f"""🔄 **Jarayondagi arizalar ({len(progress_orders)} ta)**

"""
                for order in progress_orders[:10]:
                    text += f"🔄 **#{order['id']}** - {order.get('client_name', 'N/A')}\n"
                
                if len(progress_orders) > 10:
                    text += f"\n... va yana {len(progress_orders) - 10} ta ariza"
            else:
                text = "🔄 Jarayondagi arizalar yo'q"
            
            # Create keyboard
            keyboard = _create_orders_list_keyboard(progress_orders[:5], lang)
            
            await edit_and_track(
                callback.message.edit_text,
                text,
                callback.from_user.id,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_progress_orders: {e}")

    async def _show_completed_orders(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show completed orders"""
        try:
            orders = await get_junior_manager_orders(junior_manager_id, limit=1000)
            completed_orders = [order for order in orders if order.get('status') == 'completed']
            
            if completed_orders:
                text = f"""✅ **Bajarilgan arizalar ({len(completed_orders)} ta)**

"""
                for order in completed_orders[:10]:
                    text += f"✅ **#{order['id']}** - {order.get('client_name', 'N/A')}\n"
                
                if len(completed_orders) > 10:
                    text += f"\n... va yana {len(completed_orders) - 10} ta ariza"
            else:
                text = "✅ Bajarilgan arizalar yo'q"
            
            # Create keyboard
            keyboard = _create_orders_list_keyboard(completed_orders[:5], lang)
            
            await edit_and_track(
                callback.message.edit_text,
                text,
                callback.from_user.id,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_completed_orders: {e}")

    async def _show_search_orders(callback: CallbackQuery, lang: str):
        """Show search orders menu"""
        text = """🔍 **Arizalarni qidirish**

Arizalarni qidirish uchun quyidagi usullardan birini tanlang:"""
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📱 Telefon raqam", callback_data="jm_search_by_phone"),
                InlineKeyboardButton(text="👤 Mijoz ismi", callback_data="jm_search_by_name")
            ],
            [
                InlineKeyboardButton(text="📅 Sana", callback_data="jm_search_by_date"),
                InlineKeyboardButton(text="📋 ID", callback_data="jm_search_by_id")
            ],
            [
                InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_orders")
            ]
        ])
        
        await edit_and_track(
            callback.message.edit_text,
            text,
            callback.from_user.id,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    async def _show_orders_stats(callback: CallbackQuery, junior_manager_id: int, lang: str):
        """Show orders statistics"""
        try:
            orders = await get_junior_manager_orders(junior_manager_id, limit=1000)
            
            total_orders = len(orders)
            pending_orders = len([o for o in orders if o.get('status') == 'pending'])
            progress_orders = len([o for o in orders if o.get('status') == 'in_progress'])
            completed_orders = len([o for o in orders if o.get('status') == 'completed'])
            
            text = f"""📊 **Arizalar statistikasi**

📋 **Jami arizalar:** {total_orders}
⏳ **Kutilayotgan:** {pending_orders}
🔄 **Jarayonda:** {progress_orders}
✅ **Bajarilgan:** {completed_orders}

📈 **Bajarilish foizi:** {(completed_orders/total_orders*100) if total_orders > 0 else 0:.1f}%"""
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="📊 Batafsil", callback_data="jm_detailed_stats"),
                    InlineKeyboardButton(text="📈 Grafik", callback_data="jm_stats_chart")
                ],
                [
                    InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_orders")
                ]
            ])
            
            await edit_and_track(
                callback.message.edit_text,
                text,
                callback.from_user.id,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
            
        except Exception as e:
            print(f"Error in _show_orders_stats: {e}")

    def _create_orders_list_keyboard(orders: List, lang: str) -> InlineKeyboardMarkup:
        """Create orders list keyboard"""
        keyboard = []
        
        for order in orders:
            keyboard.append([
                InlineKeyboardButton(
                    text=f"📋 #{order['id']} - {order.get('client_name', 'N/A')}",
                    callback_data=f"view_order:{order['id']}"
                )
            ])
        
        keyboard.append([
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="jm_back_to_orders")
        ])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def _get_status_emoji(status: str) -> str:
        """Get status emoji"""
        status_emojis = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'cancelled': '❌'
        }
        return status_emojis.get(status, '📋')

    return router 

router = get_junior_manager_orders_router() 
