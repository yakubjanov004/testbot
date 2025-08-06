from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from states.technician_states import TechnicianEquipmentStates

def get_technician_equipment_router():
    """Technician equipment router - Simplified Implementation"""
    router = Router()

    @router.callback_query(F.data == "tech_equipment_request")
    async def tech_equipment_request_handler(callback: CallbackQuery, state: FSMContext):
        """Request equipment from warehouse"""
        try:
            await state.set_state(TechnicianEquipmentStates.waiting_for_equipment_request)
            equipment_text = "📦 Kerakli jihozlar ro'yxatini yozing:"
            await callback.message.edit_text(equipment_text)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.message(TechnicianEquipmentStates.waiting_for_equipment_request)
    async def process_equipment_request(message: Message, state: FSMContext):
        """Process equipment request and send to warehouse"""
        try:
            request_text = (
                f"📦 Jihoz so'rovi\n\n"
                f"👨‍🔧 Texnik: Test Technician\n"
                f"📞 Telefon: +998901234567\n"
                f"📝 Kerakli jihozlar: {message.text}\n"
                f"⏰ Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            
            # Mock sending to warehouse
            success_text = "✅ Jihoz so'rovi yuborildi!"
            await message.answer(success_text)
            await state.clear()
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")
            await state.clear()

    @router.callback_query(F.data == "tech_equipment_status")
    async def equipment_status_handler(callback: CallbackQuery):
        """Show equipment status"""
        try:
            # Mock equipment data
            equipment_status = [
                {"name": "Kabel", "status": "✅ Mavjud", "quantity": "50m"},
                {"name": "Router", "status": "⚠️ Kam", "quantity": "2ta"},
                {"name": "Modem", "status": "✅ Mavjud", "quantity": "15ta"},
                {"name": "Antenna", "status": "❌ Yo'q", "quantity": "0ta"}
            ]
            
            status_text = "📦 Jihozlar holati:\n\n"
            for item in equipment_status:
                status_text += f"{item['name']}: {item['status']} ({item['quantity']})\n"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Yangilash", callback_data="refresh_equipment")]
            ])
            
            await callback.message.edit_text(status_text, reply_markup=keyboard)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "refresh_equipment")
    async def refresh_equipment_handler(callback: CallbackQuery):
        """Refresh equipment status"""
        await equipment_status_handler(callback)

    return router
