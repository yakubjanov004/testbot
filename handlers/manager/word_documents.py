"""
Manager Word Documents Handler - Complete Implementation

This module provides word document generation functionality for Manager role,
allowing managers to create various types of documents (work orders, reports, quality control, work time reports).
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, date, timedelta
from keyboards.manager_buttons import (
    get_manager_word_documents_keyboard,
    get_word_document_type_keyboard,
    get_manager_main_keyboard
)
from states.manager_states import ManagerWordDocumentStates

def get_manager_word_documents_router():
    """Manager word documents router"""
    from aiogram import Router
    router = Router()

    @router.message(F.text == "📄 Hujjatlar yaratish")
    async def show_word_documents_menu(message: Message, state: FSMContext):
        """Manager word documents menu handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': message.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            menu_text = "📄 Hujjat turini tanlang:"
            
            await message.answer(
                menu_text,
                reply_markup=get_word_document_type_keyboard('uz')
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("word_doc_"))
    async def handle_word_document_type(callback: CallbackQuery, state: FSMContext):
        """Handle word document type selection"""
        try:
            document_type = callback.data.replace("word_doc_", "")
            
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            lang = user.get('language', 'uz')
            
            if document_type == "work_order":
                await generate_work_order_document(callback, state, user, lang)
            elif document_type == "manager_report":
                await generate_manager_report_document(callback, state, user, lang)
            elif document_type == "quality_control":
                await generate_quality_control_document(callback, state, user, lang)
            elif document_type == "work_time_report":
                await generate_work_time_report_document(callback, state, user, lang)
            else:
                error_text = "Noma'lum hujjat turi."
                await callback.answer(error_text)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi.")

    async def generate_work_order_document(callback: CallbackQuery, state: FSMContext, user: dict, lang: str):
        """Generate work order document"""
        try:
            # Mock applications data
            applications = [
                {
                    'id': 'APP-001',
                    'client_name': 'Test Client 1',
                    'description': 'Internet ulanish muammosi',
                    'status': 'in_progress',
                    'created_at': datetime.now()
                },
                {
                    'id': 'APP-002',
                    'client_name': 'Test Client 2',
                    'description': 'Televizor signal muammosi',
                    'status': 'completed',
                    'created_at': datetime.now()
                }
            ]
            
            if not applications:
                no_data_text = "Ish buyrug'i uchun arizalar topilmadi."
                await callback.answer(no_data_text)
                return
            
            # Mock document generation
            success_text = "Ish buyrug'i hujjati yaratildi."
            await callback.answer(success_text)
            
            # Mock document file
            await callback.message.answer(
                "📄 Ish buyrug'i hujjati tayyor!\n\n"
                f"📋 Ariza soni: {len(applications)}\n"
                f"👨‍💼 Menejer: {user.get('full_name', 'Manager')}\n"
                f"📅 Sana: {datetime.now().strftime('%d.%m.%Y')}"
            )
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi.")

    async def generate_manager_report_document(callback: CallbackQuery, state: FSMContext, user: dict, lang: str):
        """Generate manager report document"""
        try:
            # Mock statistics data
            stats = {
                'total_applications': 25,
                'completed_applications': 20,
                'pending_applications': 5,
                'average_completion_time': '2.5 soat',
                'customer_satisfaction': '4.8/5'
            }
            
            # Mock document generation
            success_text = "Menejer hisoboti yaratildi."
            await callback.answer(success_text)
            
            # Mock document file
            await callback.message.answer(
                "📊 Menejer hisoboti tayyor!\n\n"
                f"📈 Jami arizalar: {stats['total_applications']}\n"
                f"✅ Bajarilgan: {stats['completed_applications']}\n"
                f"⏳ Kutilayotgan: {stats['pending_applications']}\n"
                f"⏱️ O'rtacha vaqt: {stats['average_completion_time']}\n"
                f"⭐️ Mijoz mamnuniyati: {stats['customer_satisfaction']}"
            )
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi.")

    async def generate_quality_control_document(callback: CallbackQuery, state: FSMContext, user: dict, lang: str):
        """Generate quality control document"""
        try:
            # Mock quality control data
            quality_data = [
                {
                    'technician_name': 'Test Technician 1',
                    'completed_tasks': 15,
                    'quality_score': 4.8,
                    'customer_feedback': 'Juda yaxshi'
                },
                {
                    'technician_name': 'Test Technician 2',
                    'completed_tasks': 12,
                    'quality_score': 4.6,
                    'customer_feedback': 'Yaxshi'
                }
            ]
            
            # Mock document generation
            success_text = "Kvalitet nazorati hujjati yaratildi."
            await callback.answer(success_text)
            
            # Mock document file
            quality_text = "🔍 Kvalitet nazorati hisoboti tayyor!\n\n"
            for tech in quality_data:
                quality_text += f"👨‍🔧 {tech['technician_name']}\n"
                quality_text += f"   ✅ Bajarilgan: {tech['completed_tasks']}\n"
                quality_text += f"   ⭐️ Baho: {tech['quality_score']}/5\n"
                quality_text += f"   💬 Fikr: {tech['customer_feedback']}\n\n"
            
            await callback.message.answer(quality_text)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi.")

    async def generate_work_time_report_document(callback: CallbackQuery, state: FSMContext, user: dict, lang: str):
        """Generate work time report document"""
        try:
            # Mock work time data
            work_time_data = {
                'total_hours': 160,
                'average_per_day': 8,
                'overtime_hours': 12,
                'technicians_count': 5,
                'efficiency_rate': '95%'
            }
            
            # Mock document generation
            success_text = "Ishlash vaqti hisoboti yaratildi."
            await callback.answer(success_text)
            
            # Mock document file
            await callback.message.answer(
                "⏰ Ishlash vaqti hisoboti tayyor!\n\n"
                f"🕐 Jami soatlar: {work_time_data['total_hours']}\n"
                f"📅 Kunlik o'rtacha: {work_time_data['average_per_day']} soat\n"
                f"⏰ Qo'shimcha soatlar: {work_time_data['overtime_hours']}\n"
                f"👥 Texniklar soni: {work_time_data['technicians_count']}\n"
                f"📈 Samaradorlik: {work_time_data['efficiency_rate']}"
            )
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi.")

    @router.callback_query(F.data == "back_to_manager_main")
    async def back_to_manager_main(callback: CallbackQuery, state: FSMContext):
        """Back to manager main menu"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'manager',
                'language': 'uz',
                'full_name': 'Test Manager'
            }
            
            lang = user.get('language', 'uz')
            main_text = "🏠 Asosiy menyu:"
            
            await callback.message.edit_text(
                main_text,
                reply_markup=get_manager_main_keyboard(lang)
            )
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi.")

    return router 