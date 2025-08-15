"""
Controller Orders Handler
Manages orders for controller
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from filters.role_filter import RoleFilter
from utils.db import get_user_by_telegram_id, get_all_orders, get_orders_by_status, get_single_order_details


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
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            
            # Get orders statistics
            all_orders = await get_all_orders()
            new_orders = [o for o in all_orders if o['status'] == 'Yangi']
            pending_orders = [o for o in all_orders if o['status'] == 'Jarayonda']
            problem_orders = []  # Placeholder: derive from rules or use separate issues table
            
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
            if not user or user.get('role') != 'controller':
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
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            orders = await get_orders_by_status(['pending', 'assigned', 'in_progress'])
            
            text = "⏳ <b>Kutilayotgan buyurtmalar:</b>\n\n"
            
            if orders:
                for order in orders[:10]:
                    client_name = order.get('client_name', 'Noma\'lum')
                    technician_name = order.get('assigned_to', 'Tayinlanmagan')
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
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            # Without a problem flag, show long-pending (demo placeholder)
            issues = []
            
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
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            orders = await get_all_orders(limit=100)
            
            # Statistikani hisoblash
            total_orders = len(orders)
            completed_orders = len([o for o in orders if o['status'] == 'Bajarilgan'])
            pending_orders = len([o for o in orders if o['status'] in ['Yangi', 'Kutilmoqda', 'Jarayonda']])
            in_progress_orders = len([o for o in orders if o['status'] == 'Jarayonda'])
            
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

    # ===== New: "📋 Arizalarni ko'rish" full list with filters and pagination =====
    def _filter_orders(orders: List[Dict[str, Any]], flt: str) -> List[Dict[str, Any]]:
        if flt == 'all':
            return orders
        if flt == 'active':
            return [o for o in orders if o.get('status') in ['Yangi', 'Jarayonda']]
        if flt == 'completed':
            return [o for o in orders if o.get('status') == 'Bajarilgan']
        return orders

    def _orders_list_keyboard(orders: List[Dict[str, Any]], flt: str, page: int, total_pages: int) -> InlineKeyboardMarkup:
        rows = []
        # Order buttons
        for o in orders:
            rows.append([InlineKeyboardButton(
                text=f"{o.get('order_number', f'#{o['id']}')} · {o.get('client_name','N/A')}",
                callback_data=f"ctrl_orders_view_{o['id']}_{flt}_{page}"
            )])
        # Nav row
        nav = []
        if page > 1:
            nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"ctrl_orders_prev_{flt}_{page-1}"))
        nav.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
        if page < total_pages:
            nav.append(InlineKeyboardButton(text="➡️", callback_data=f"ctrl_orders_next_{flt}_{page+1}"))
        rows.append(nav)
        # Filter row
        rows.append([
            InlineKeyboardButton(text=("📋 Hammasi"), callback_data="ctrl_orders_filter_all"),
            InlineKeyboardButton(text=("⏳ Faol"), callback_data="ctrl_orders_filter_active"),
            InlineKeyboardButton(text=("✅ Bajarilgan"), callback_data="ctrl_orders_filter_completed"),
        ])
        # Actions
        rows.append([
            InlineKeyboardButton(text="🔄 Yangilash", callback_data=f"ctrl_orders_refresh_{flt}_{page}"),
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="controllers_back"),
        ])
        return InlineKeyboardMarkup(inline_keyboard=rows)

    async def _render_orders_list(message_or_callback, flt: str = 'all', page: int = 1, per_page: int = 5):
        all_orders = await get_all_orders(limit=200)
        filtered = _filter_orders(all_orders, flt)
        total = len(filtered)
        total_pages = max(1, (total + per_page - 1) // per_page)
        page = max(1, min(page, total_pages))
        start = (page - 1) * per_page
        slice_ = filtered[start:start+per_page]
        text = (
            f"📋 <b>Arizalar ro'yxati</b>\n"
            f"Filtr: {('Hammasi' if flt=='all' else 'Faol' if flt=='active' else 'Bajarilgan')} · Sahifa {page}/{total_pages}\n\n"
        )
        if slice_:
            for o in slice_:
                text += (f"🔹 <b>{o.get('order_number', f'#{o['id']}')}</b> — {o.get('client_name','N/A')} · {o.get('status','')}\n")
        else:
            text += "Hozircha ma'lumot yo'q"
        kb = _orders_list_keyboard(slice_, flt, page, total_pages)
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(text, reply_markup=kb, parse_mode='HTML')
        else:
            await message_or_callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')

    # ===== Single-order detailed view helpers =====
    def _order_detail_keyboard(flt: str, index: int, total: int) -> InlineKeyboardMarkup:
        rows = []
        nav = []
        if index > 0:
            nav.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"ctrl_orders_nav_prev_{flt}_{index-1}"))
        nav.append(InlineKeyboardButton(text=f"{index+1}/{total}", callback_data="noop"))
        if index < total - 1:
            nav.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"ctrl_orders_nav_next_{flt}_{index+1}"))
        if nav:
            rows.append(nav)
        rows.append([
            InlineKeyboardButton(text="📋 Hammasi", callback_data="ctrl_orders_filter_all"),
            InlineKeyboardButton(text="⏳ Faol", callback_data="ctrl_orders_filter_active"),
            InlineKeyboardButton(text="✅ Bajarilgan", callback_data="ctrl_orders_filter_completed"),
        ])
        rows.append([
            InlineKeyboardButton(text="🔄 Yangilash", callback_data=f"ctrl_orders_refresh_detail_{flt}_{index}"),
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data="controllers_back"),
        ])
        return InlineKeyboardMarkup(inline_keyboard=rows)

    async def _render_order_detail(message_or_callback, flt: str = 'all', index: int = 0):
        all_orders = await get_all_orders(limit=200)
        filtered = _filter_orders(all_orders, flt)
        total = len(filtered)
        if total == 0:
            text = "📋 <b>Arizalar</b>\nHozircha ma'lumot yo'q"
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📋 Hammasi", callback_data="ctrl_orders_filter_all"),
                 InlineKeyboardButton(text="⏳ Faol", callback_data="ctrl_orders_filter_active"),
                 InlineKeyboardButton(text="✅ Bajarilgan", callback_data="ctrl_orders_filter_completed")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="controllers_back")]
            ])
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=kb, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')
            return
        index = max(0, min(index, total - 1))
        o = filtered[index]
        text = (
            f"📄 <b>Ariza ma'lumotlari</b>\n\n"
            f"🔢 <b>Raqam:</b> {o.get('order_number', f'#{o['id']}')}\n"
            f"👤 <b>Mijoz:</b> {o.get('client_name','N/A')}\n"
            f"🛠 <b>Xizmat:</b> {o.get('service_type','-')}\n"
            f"📅 <b>Sana:</b> {o.get('created_at','-')}\n"
            f"📌 <b>Status:</b> {o.get('status','-')}\n"
            f"⚡ <b>Ustuvorlik:</b> {o.get('priority','-')}\n"
            f"👨‍💼 <b>Mas'ul:</b> {o.get('assigned_to','-')}\n"
            f"📝 <b>Izoh:</b> {o.get('description','Yo\'q')}\n"
            f"\n📊 <b>#{index+1}/{total}</b>"
        )
        kb = _order_detail_keyboard(flt, index, total)
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(text, reply_markup=kb, parse_mode='HTML')
        else:
            await message_or_callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')

    @router.message(F.text.in_(["📋 Arizalarni ko'rish"]))
    async def controller_view_orders(message: Message, state: FSMContext):
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            await _render_order_detail(message, flt='all', index=0)
        except Exception:
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_orders_filter_all")
    async def orders_filter_all(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await _render_order_detail(callback, flt='all', index=0)

    @router.callback_query(F.data == "ctrl_orders_filter_active")
    async def orders_filter_active(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await _render_order_detail(callback, flt='active', index=0)

    @router.callback_query(F.data == "ctrl_orders_filter_completed")
    async def orders_filter_completed(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await _render_order_detail(callback, flt='completed', index=0)

    @router.callback_query(lambda c: c.data.startswith("ctrl_orders_nav_prev_"))
    async def orders_nav_prev(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        parts = callback.data.split("_")
        flt = parts[4]
        index = parts[5]
        await _render_order_detail(callback, flt=flt, index=int(index))

    @router.callback_query(lambda c: c.data.startswith("ctrl_orders_nav_next_"))
    async def orders_nav_next(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        parts = callback.data.split("_")
        flt = parts[4]
        index = parts[5]
        await _render_order_detail(callback, flt=flt, index=int(index))

    @router.callback_query(lambda c: c.data.startswith("ctrl_orders_refresh_detail_"))
    async def orders_refresh_detail(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        parts = callback.data.split("_")
        flt = parts[4]
        index = parts[5]
        await _render_order_detail(callback, flt=flt, index=int(index))

    @router.callback_query(lambda c: c.data.startswith("ctrl_orders_view_"))
    async def orders_view(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            parts = callback.data.split("_")
            # ctrl orders view {id} {flt} {page}
            order_id = int(parts[3])
            flt = parts[4]
            page = int(parts[5])
            order = await get_single_order_details(order_id)
            text = (
                f"📄 <b>Ariza ma'lumotlari</b>\n\n"
                f"🔢 <b>Raqam:</b> {order.get('order_number')}\n"
                f"👤 <b>Mijoz:</b> {order.get('client_name')}\n"
                f"🛠 <b>Xizmat:</b> {order.get('service_type')}\n"
                f"📅 <b>Sana:</b> {order.get('created_at')}\n"
                f"📌 <b>Status:</b> {order.get('status')}\n"
                f"⚡ <b>Ustuvorlik:</b> {order.get('priority')}\n"
                f"👨‍💼 <b>Mas'ul:</b> {order.get('assigned_to')}\n"
                f"📝 <b>Izoh:</b> {order.get('description')}\n"
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Ro'yxatga qaytish", callback_data=f"ctrl_orders_back_{flt}_{page}")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="controllers_back")],
            ])
            await callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')
        except Exception:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(lambda c: c.data.startswith("ctrl_orders_back_"))
    async def orders_back_to_list(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        _, _, _, flt, page = callback.data.split("_")
        await _render_orders_list(callback, flt=flt, page=int(page))
 
    return router
