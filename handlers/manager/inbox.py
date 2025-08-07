"""
Manager Inbox Handler - To'liq yangilangan versiya

Bu modul manager uchun inbox funksionalligini o'z ichiga oladi.
To'liq mock data, pagination va kichik menejerga yuborish funksiyasi bilan.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

# Mock database functions
async def get_users_by_role(role: str):
    """Mock get users by role"""
    if role == 'junior_manager':
        return [
            {
                'id': 2,
                'full_name': 'Ahmad Toshmatov',
                'phone_number': '+998901234568',
                'role': 'junior_manager',
                'is_active': True
            },
            {
                'id': 3,
                'full_name': 'Malika Karimova',
                'phone_number': '+998901234569',
                'role': 'junior_manager',
                'is_active': True
            },
            {
                'id': 4,
                'full_name': 'Jasur Rahimov',
                'phone_number': '+998901234570',
                'role': 'junior_manager',
                'is_active': True
            },
            {
                'id': 5,
                'full_name': 'Dilfuza Abdullayeva',
                'phone_number': '+998901234571',
                'role': 'junior_manager',
                'is_active': True
            }
        ]
    return []

# Mock workflow engine
class MockWorkflowEngine:
    """Mock workflow engine"""
    async def get_workflow_status(self, request_id: str):
        """Mock get workflow status"""
        return {
            'current_status': 'created',
            'current_role': 'manager'
        }
    
    async def transition_workflow(self, request_id: str, action: str, role: str, data: dict):
        """Mock workflow transition"""
        print(f"Mock: Transitioning workflow {request_id} with action {action} by {role}")
        return True

# Mock state manager with comprehensive data
class MockStateManager:
    """Mock state manager with complete application data"""
    async def get_request(self, request_id: str):
        """Mock get request with complete details"""
        from datetime import datetime, timedelta
        now = datetime.now()
        
        # Comprehensive mock data for different request types
        mock_requests = {
            'req_001_2024_01_15': {
                'id': 'req_001_2024_01_15',
                'workflow_type': 'connection_request',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Aziz Karimov',
                    'phone': '+998901234567',
                    'phone_number': '+998901234567',
                    'email': 'aziz.karimov@example.com'
                },
                'created_at': now - timedelta(hours=2),
                'description': 'Internet ulanish arizasi\nTariff: 100 Mbps\nB2C mijoz\nManzil: Tashkent, Chorsu tumani, 15-uy\nQo\'shimcha ma\'lumot: Yangi uy, optic kabel kerak',
                'location': 'Tashkent, Chorsu tumani, 15-uy',
                'priority': 'high',
                'tariff': '100 Mbps',
                'connection_type': 'B2C',
                'equipment_needed': 'Router, optic kabel',
                'estimated_cost': '500,000 so\'m',
                'expected_completion': '3-5 kun'
            },
            'req_002_2024_01_16': {
                'id': 'req_002_2024_01_16',
                'workflow_type': 'technical_service',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Malika Toshmatova',
                    'phone': '+998901234568',
                    'phone_number': '+998901234568',
                    'email': 'malika.toshmatova@example.com'
                },
                'created_at': now - timedelta(hours=1, minutes=30),
                'description': 'TV signal yo\'q\nKabel uzilgan\nManzil: Tashkent, Yunusabad tumani, 45-uy\nMuammo: TV kanallar ko\'rinmayapti',
                'location': 'Tashkent, Yunusabad tumani, 45-uy',
                'priority': 'medium',
                'service_type': 'TV signal repair',
                'equipment_needed': 'Yangi kabel',
                'estimated_cost': '150,000 so\'m',
                'expected_completion': '1-2 kun'
            },
            'req_003_2024_01_17': {
                'id': 'req_003_2024_01_17',
                'workflow_type': 'connection_request',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Jasur Rahimov',
                    'phone': '+998901234569',
                    'phone_number': '+998901234569',
                    'email': 'jasur.rahimov@company.uz'
                },
                'created_at': now - timedelta(minutes=45),
                'description': 'Internet ulanish arizasi\nTariff: 50 Mbps\nB2B mijoz\nManzil: Tashkent, Sergeli tumani, 78-uy\nKompaniya: "Rahimov Trading" LLC',
                'location': 'Tashkent, Sergeli tumani, 78-uy',
                'priority': 'normal',
                'tariff': '50 Mbps',
                'connection_type': 'B2B',
                'company_name': 'Rahimov Trading LLC',
                'equipment_needed': 'Router, switch',
                'estimated_cost': '800,000 so\'m',
                'expected_completion': '5-7 kun'
            },
            'req_004_2024_01_18': {
                'id': 'req_004_2024_01_18',
                'workflow_type': 'call_center_direct',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Dilfuza Karimova',
                    'phone': '+998901234570',
                    'phone_number': '+998901234570',
                    'email': 'dilfuza.karimova@example.com'
                },
                'created_at': now - timedelta(minutes=20),
                'description': 'Internet sekin ishlaydi\nTezlik past\nManzil: Tashkent, Chilanzar tumani, 23-uy\nMuammo: Download tezligi 1 Mbps',
                'location': 'Tashkent, Chilanzar tumani, 23-uy',
                'priority': 'high',
                'service_type': 'Speed optimization',
                'current_speed': '1 Mbps',
                'expected_speed': '50 Mbps',
                'estimated_cost': '200,000 so\'m',
                'expected_completion': '2-3 kun'
            },
            'req_005_2024_01_19': {
                'id': 'req_005_2024_01_19',
                'workflow_type': 'technical_service',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Asadbek Abdullayev',
                    'phone': '+998901234571',
                    'phone_number': '+998901234571',
                    'email': 'asadbek.abdullayev@example.com'
                },
                'created_at': now - timedelta(minutes=10),
                'description': 'Router ishlamayapti\nYangi router kerak\nManzil: Tashkent, Shayxontohur tumani, 67-uy\nMuammo: Router yonib-o\'chib turadi',
                'location': 'Tashkent, Shayxontohur tumani, 67-uy',
                'priority': 'urgent',
                'service_type': 'Router replacement',
                'equipment_needed': 'Yangi router',
                'estimated_cost': '300,000 so\'m',
                'expected_completion': '1 kun'
            },
            'req_006_2024_01_20': {
                'id': 'req_006_2024_01_20',
                'workflow_type': 'connection_request',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Shahnoza Mirzayeva',
                    'phone': '+998901234572',
                    'phone_number': '+998901234572',
                    'email': 'shahnoza.mirzayeva@example.com'
                },
                'created_at': now - timedelta(minutes=5),
                'description': 'Internet ulanish arizasi\nTariff: 200 Mbps\nB2C mijoz\nManzil: Tashkent, Yakkasaroy tumani, 89-uy\nQo\'shimcha: Gaming uchun yuqori tezlik kerak',
                'location': 'Tashkent, Yakkasaroy tumani, 89-uy',
                'priority': 'high',
                'tariff': '200 Mbps',
                'connection_type': 'B2C',
                'equipment_needed': 'Gaming router, optic kabel',
                'estimated_cost': '750,000 so\'m',
                'expected_completion': '4-6 kun'
            },
            'req_007_2024_01_21': {
                'id': 'req_007_2024_01_21',
                'workflow_type': 'technical_service',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Bobur Turgunov',
                    'phone': '+998901234573',
                    'phone_number': '+998901234573',
                    'email': 'bobur.turgunov@example.com'
                },
                'created_at': now - timedelta(minutes=3),
                'description': 'WiFi signal kuchsiz\nSignal kuchaytirgich kerak\nManzil: Tashkent, Mirabad tumani, 34-uy\nMuammo: Uyning narigi qismida signal yo\'q',
                'location': 'Tashkent, Mirabad tumani, 34-uy',
                'priority': 'medium',
                'service_type': 'WiFi signal booster',
                'equipment_needed': 'WiFi extender',
                'estimated_cost': '250,000 so\'m',
                'expected_completion': '2-3 kun'
            },
            'req_008_2024_01_22': {
                'id': 'req_008_2024_01_22',
                'workflow_type': 'connection_request',
                'current_status': 'created',
                'role_current': 'manager',
                'contact_info': {
                    'full_name': 'Zarina Usmanova',
                    'phone': '+998901234574',
                    'phone_number': '+998901234574',
                    'email': 'zarina.usmanova@company.uz'
                },
                'created_at': now - timedelta(minutes=1),
                'description': 'Internet ulanish arizasi\nTariff: 150 Mbps\nB2B mijoz\nManzil: Tashkent, Bektemir tumani, 12-uy\nKompaniya: "Usmanova Solutions" LLC',
                'location': 'Tashkent, Bektemir tumani, 12-uy',
                'priority': 'normal',
                'tariff': '150 Mbps',
                'connection_type': 'B2B',
                'company_name': 'Usmanova Solutions LLC',
                'equipment_needed': 'Router, switch, UPS',
                'estimated_cost': '1,200,000 so\'m',
                'expected_completion': '7-10 kun'
            }
        }
        
        return mock_requests.get(request_id, {
            'id': request_id,
            'workflow_type': 'connection_request',
            'current_status': 'created',
            'role_current': 'manager',
            'contact_info': {
                'full_name': 'Test Client',
                'phone': '+998901234567',
                'phone_number': '+998901234567',
                'email': 'test@example.com'
            },
            'created_at': now,
            'description': 'Test ariza',
            'location': 'Test manzil',
            'priority': 'normal',
            'tariff': '50 Mbps',
            'connection_type': 'B2C',
            'equipment_needed': 'Router',
            'estimated_cost': '400,000 so\'m',
            'expected_completion': '3-5 kun'
        })

# Mock inbox manager with comprehensive data
class MockInboxManager:
    """Mock inbox manager with complete data"""
    async def get_role_inbox(self, role: str, limit: int = 50):
        """Mock get role inbox with comprehensive data"""
        from datetime import datetime
        return [
            {
                'id': 1,
                'application_id': 'req_001_2024_01_15',
                'title': '🔴 Muhim: Internet ulanish arizasi',
                'description': 'Aziz Karimov - 100 Mbps tariff, B2C mijoz, Chorsu tumani',
                'priority': 'high',
                'time_ago': '2 soat oldin',
                'status': 'created',
                'workflow_type': 'connection_request'
            },
            {
                'id': 2,
                'application_id': 'req_002_2024_01_16',
                'title': '🔧 TV signal muammosi',
                'description': 'Malika Toshmatova - kabel uzilgan, Yunusabad tumani',
                'priority': 'medium',
                'time_ago': '1 soat 30 daqiqa oldin',
                'status': 'created',
                'workflow_type': 'technical_service'
            },
            {
                'id': 3,
                'application_id': 'req_003_2024_01_17',
                'title': '🔌 Yangi internet ulanish',
                'description': 'Jasur Rahimov - 50 Mbps tariff, B2B mijoz, Sergeli tumani',
                'priority': 'normal',
                'time_ago': '45 daqiqa oldin',
                'status': 'created',
                'workflow_type': 'connection_request'
            },
            {
                'id': 4,
                'application_id': 'req_004_2024_01_18',
                'title': '🚨 Internet sekin ishlaydi',
                'description': 'Dilfuza Karimova - tezlik past, Chilanzar tumani',
                'priority': 'high',
                'time_ago': '20 daqiqa oldin',
                'status': 'created',
                'workflow_type': 'call_center_direct'
            },
            {
                'id': 5,
                'application_id': 'req_005_2024_01_19',
                'title': '⚡ Router ishlamayapti',
                'description': 'Asadbek Abdullayev - yangi router kerak, Shayxontohur tumani',
                'priority': 'urgent',
                'time_ago': '10 daqiqa oldin',
                'status': 'created',
                'workflow_type': 'technical_service'
            },
            {
                'id': 6,
                'application_id': 'req_006_2024_01_20',
                'title': '🎮 Gaming internet ulanish',
                'description': 'Shahnoza Mirzayeva - 200 Mbps tariff, Yakkasaroy tumani',
                'priority': 'high',
                'time_ago': '5 daqiqa oldin',
                'status': 'created',
                'workflow_type': 'connection_request'
            },
            {
                'id': 7,
                'application_id': 'req_007_2024_01_21',
                'title': '📶 WiFi signal kuchsiz',
                'description': 'Bobur Turgunov - signal kuchaytirgich kerak, Mirabad tumani',
                'priority': 'medium',
                'time_ago': '3 daqiqa oldin',
                'status': 'created',
                'workflow_type': 'technical_service'
            },
            {
                'id': 8,
                'application_id': 'req_008_2024_01_22',
                'title': '🏢 B2B internet ulanish',
                'description': 'Zarina Usmanova - 150 Mbps tariff, B2B mijoz, Bektemir tumani',
                'priority': 'normal',
                'time_ago': '1 daqiqa oldin',
                'status': 'created',
                'workflow_type': 'connection_request'
            }
        ]
    
    async def mark_as_read(self, message_id: int):
        """Mock mark as read"""
        print(f"Mock: Marking message {message_id} as read")

# Mock workflow access control
class MockWorkflowAccessControl:
    """Mock workflow access control"""
    async def get_filtered_requests_for_role(self, user_id: int, user_role: str, **kwargs):
        """Mock get filtered requests for role"""
        from datetime import datetime, timedelta
        now = datetime.now()
        
        # Return all mock requests
        state_manager = MockStateManager()
        requests = []
        
        for i in range(1, 9):
            request_id = f'req_{i:03d}_2024_01_{15+i-1}'
            request = await state_manager.get_request(request_id)
            if request:
                requests.append(request)
        
        return requests
    
    async def validate_workflow_action(self, user_id: int, user_role: str, action: str, **kwargs):
        """Mock validate workflow action"""
        return True, "OK"

# Mock application queries
async def get_comments_for_role(request_id: str, role: str):
    """Mock get comments for role"""
    return [
        {
            'commenter': 'Test Manager',
            'comment': 'Test izoh',
            'created_at': datetime.now(),
            'comment_type': 'manager_comment'
        }
    ]

async def add_role_comment(request_id: str, user_id: int, comment: str, role: str):
    """Mock add role comment"""
    print(f"Mock: Adding comment to request {request_id} by user {user_id}")
    return True

# Mock word document queries
class MockWordDocumentQueries:
    """Mock word document queries"""
    async def update_manager_data(self, request_id: str, manager_data: dict):
        """Mock update manager data"""
        print(f"Mock: Updating manager data for request {request_id}")

def get_manager_inbox_router():
    """Get manager inbox router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.callback_query(F.data.startswith("open_inbox_"))
    async def handle_inbox_notification(callback: CallbackQuery, state: FSMContext):
        """Handle inbox notification button click"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id_short = callback.data.replace("open_inbox_", "")
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                return
            
            # Show inbox
            await show_manager_inbox_from_notification(callback.message, state, request_id_short)
            
        except Exception as e:
            print(f"Error handling inbox notification: {e}")
            await callback.answer("Xatolik yuz berdi")
    
    async def show_manager_inbox_from_notification(message: Message, state: FSMContext, target_request_id: str = None):
        """Show manager inbox with focus on specific request"""
        try:
            user = await get_user_by_telegram_id(message.chat.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            
            # Get inbox messages from inbox manager
            inbox_manager = MockInboxManager()
            inbox_messages = await inbox_manager.get_role_inbox('manager', limit=50)
            
            if not inbox_messages:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            # Find target request index if specified
            target_index = 0
            if target_request_id:
                for i, msg in enumerate(inbox_messages):
                    if msg['application_id'].startswith(target_request_id):
                        target_index = i
                        # Mark as read
                        await inbox_manager.mark_as_read(msg['id'])
                        break
            
            # Get full request details
            requests = []
            for msg in inbox_messages:
                access_control = MockWorkflowAccessControl()
                request_details = await access_control.get_filtered_requests_for_role(
                    user_id=user['id'],
                    user_role='manager',
                    request_ids=[msg['application_id']]
                )
                if request_details:
                    req = request_details[0]
                    req['inbox_message'] = msg
                    requests.append(req)
            
            if not requests:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            await state.update_data(
                inbox_requests=requests,
                current_index=target_index
            )
            
            await display_manager_request(message, state, requests, target_index, lang, user)
            
        except Exception as e:
            print(f"Error in show_manager_inbox_from_notification: {e}")

    @router.message(F.text.in_(["📥 Inbox"]))
    async def show_manager_inbox(message: Message, state: FSMContext):
        """Manager inbox handler"""
        try:
            # Check user role first - only process if user is manager
            from loader import get_user_role
            user_role = get_user_role(message.from_user.id)
            if user_role != 'manager':
                return  # Skip processing for non-manager users
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            
            access_control = MockWorkflowAccessControl()
            requests = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager',
                status_filter='created'
            )
            # Filter by role_current as well (defensive)
            requests = [r for r in requests if r.get('role_current') == 'manager']
            
            print(f"Manager {user['id']} got {len(requests)} requests")
            
            if not requests:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            await state.update_data(
                inbox_requests=requests,
                current_index=0
            )
            
            await display_manager_request(message, state, requests, 0, lang, user)
            
        except Exception as e:
            print(f"Error in show_manager_inbox: {str(e)}")
            lang = await get_user_lang(message.from_user.id) if hasattr(message, 'from_user') else 'uz'
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    async def display_manager_request(event, state: FSMContext, requests, index, lang, user):
        """Display a single request with complete details and manager action buttons"""
        try:
            req = requests[index]
            full_id = req['id']
            short_id = full_id[:8]
            
            print(f"Displaying request {short_id} for user {user['id']}")
            
            # Get workflow status for this request
            workflow_engine = MockWorkflowEngine()
            workflow_status = await workflow_engine.get_workflow_status(full_id)
            if workflow_status:
                req['workflow_status'] = workflow_status['current_status']
                req['workflow_role'] = workflow_status['current_role']
            
            state_manager = MockStateManager()
            request = await state_manager.get_request(full_id)
            
            if not request:
                print(f"Request {full_id} not found in database")
                text = "Ariza tafsilotlari topilmadi"
                if hasattr(event, 'answer'):
                    await event.answer(text)
                else:
                    await event.edit_text(text)
                return
            
            print(f"Request {short_id} found: {request['workflow_type']}, {request['current_status']}")
            
            # Check if this request has inbox message info
            inbox_msg = req.get('inbox_message')
            
            # Format request display
            workflow_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(request['workflow_type'], '📋')
            
            status_emoji = {
                'created': '🆕',
                'assigned_to_manager': '👨‍💼',
                'in_progress': '⏳',
                'completed': '✅',
                'cancelled': '❌',
                'assigned_to_junior_manager': '👨‍💼',
                'sent_to_warehouse': '📦',
                'warehouse_completed': '✅',
                'returned_to_technician': '🔧'
            }.get(request['current_status'], '📋')
            
            client_name = request['contact_info'].get('full_name', 'N/A') if isinstance(request['contact_info'], dict) else 'N/A'

            # Get contact info
            phone_number = request['contact_info'].get('phone_number', 'N/A') if isinstance(request['contact_info'], dict) else 'N/A'
            if phone_number == 'N/A':
                phone_number = request['contact_info'].get('phone', 'N/A') if isinstance(request['contact_info'], dict) else 'N/A'
            
            address = request.get('location') or request['contact_info'].get('address', 'N/A') if isinstance(request['contact_info'], dict) else 'N/A'
            
            # Get priority emoji
            priority_emoji = {
                'urgent': '🚨',
                'high': '🔴',
                'medium': '🟡', 
                'normal': '🟢',
                'low': '🔵'
            }.get(request['priority'], '🟢')
            
            # Get workflow type name
            workflow_name = {
                'connection_request': 'Ulanish',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Qo\'ng\'iroq markazi'
            }.get(request['workflow_type'], request['workflow_type'])
            
            # Format date
            created_date = request['created_at'].strftime('%d.%m.%Y %H:%M') if hasattr(request['created_at'], 'strftime') else str(request['created_at'])
            
            # Get additional details
            tariff_info = request.get('tariff', 'N/A')
            connection_type = request.get('connection_type', 'N/A')
            equipment_needed = request.get('equipment_needed', 'N/A')
            estimated_cost = request.get('estimated_cost', 'N/A')
            expected_completion = request.get('expected_completion', 'N/A')
            company_name = request.get('company_name', '')
            
            # Get status name in Uzbek
            status_name = {
                'created': 'Yaratilgan',
                'assigned_to_manager': 'Menejerga tayinlangan',
                'in_progress': 'Jarayonda',
                'completed': 'Tugallangan',
                'cancelled': 'Bekor qilingan',
                'assigned_to_junior_manager': 'Kichik menejerga tayinlangan',
                'sent_to_warehouse': 'Omborxona yuborilgan',
                'warehouse_completed': 'Omborxona tugallangan',
                'returned_to_technician': 'Texnikga qaytarilgan'
            }.get(request['current_status'], request['current_status'])
            
            # Add inbox message info if available
            inbox_info = ""
            if inbox_msg:
                inbox_priority_emoji = {
                    'urgent': '🚨',
                    'high': '❗',
                    'medium': '⚡',
                    'low': '💬'
                }.get(inbox_msg.get('priority', 'medium'), '💬')
                
                inbox_info = (
                    f"\n📥 <b>Inbox xabari:</b>\n"
                    f"{inbox_priority_emoji} {inbox_msg.get('title', '')}\n"
                    f"📝 {inbox_msg.get('description', '')}\n"
                    f"⏰ {inbox_msg.get('time_ago', '')}\n"
                )
            
            # Comprehensive text with all information
            text = (
                f"{workflow_emoji} <b>Manager Inbox</b>\n"
                f"{inbox_info}"
                f"\n🆔 <b>ID:</b> {short_id}-{full_id[8:12].upper()}\n"
                f"📋 <b>Tur:</b> {workflow_name}\n"
                f"🔗 <b>Ulanish turi:</b> {connection_type}\n"
                f"📊 <b>Tarif:</b> {tariff_info}\n"
                f"👤 <b>Mijoz:</b> {client_name}\n"
                f"📞 <b>Telefon:</b> {phone_number}\n"
                f"📍 <b>Manzil:</b> {address}\n"
                f"📅 <b>Yaratilgan:</b> {created_date}\n"
                f"{priority_emoji} <b>Muhimlik:</b> {request['priority'].title()}\n"
                f"{status_emoji} <b>Holat:</b> {status_name}\n"
                f"📝 <b>Tavsif:</b> {request['description'][:150]}{'...' if request['description'] and len(request['description']) > 150 else request['description'] or 'Yoq'}\n"
            )
            
            # Add additional details if available
            if equipment_needed != 'N/A':
                text += f"🔧 <b>Kerakli jihozlar:</b> {equipment_needed}\n"
            if estimated_cost != 'N/A':
                text += f"💰 <b>Taxminiy narx:</b> {estimated_cost}\n"
            if expected_completion != 'N/A':
                text += f"⏱ <b>Taxminiy muddat:</b> {expected_completion}\n"
            if company_name:
                text += f"🏢 <b>Kompaniya:</b> {company_name}\n"
            
            text += f"\n<i>📊 Ariza {index + 1}/{len(requests)}</i>"
            
            print(f"Generated text for request {short_id}: {text[:100]}...")
            print(f"Full text length: {len(text)}")
            
            # Create action buttons
            buttons = []
            
            # Debug: Print request details for troubleshooting
            print(f"Request type: {request.get('workflow_type')}, Role: {request.get('role_current')}")
            
            # Assignment button (only for connection requests)
            if request.get('workflow_type') == 'connection_request' and request.get('role_current') == 'manager':
                buttons.append([
                    InlineKeyboardButton(
                        text="📨 Kichik menejerga yuborish",
                        callback_data=f"mgr_assign_jm_{full_id}"
                    )
                ])
                print(f"Added assignment button for request {short_id}")
            else:
                print(f"No assignment button for request {short_id} - Type: {request.get('workflow_type')}, Role: {request.get('role_current')}")
            
            # Navigation buttons
            nav_buttons = []
            
            # Previous button
            if index > 0:
                nav_buttons.append(
                    InlineKeyboardButton(
                        text="⬅️ Oldingi",
                        callback_data=f"mgr_prev_{index}"
                    )
                )
            
            # Next button
            if index < len(requests) - 1:
                nav_buttons.append(
                    InlineKeyboardButton(
                        text="Keyingi ➡️",
                        callback_data=f"mgr_next_{index}"
                    )
                )
            
            # Add navigation buttons if they exist
            if nav_buttons:
                buttons.append(nav_buttons)
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            print(f"Sending message for request {short_id}")
            try:
                # Check if this is a callback query (inline keyboard event)
                if hasattr(event, 'message') and hasattr(event, 'from_user'):
                    # This is a CallbackQuery - edit the existing message
                    await event.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                    print(f"Successfully edited message for request {short_id}")
                else:
                    # This is a Message - send new message
                    await event.answer(text, reply_markup=keyboard, parse_mode='HTML')
                    print(f"Successfully sent new message for request {short_id}")
            except Exception as e:
                print(f"Error sending message for request {short_id}: {e}")
                if "message can't be edited" in str(e):
                    # If edit fails, try to send a new message
                    if hasattr(event, 'message') and hasattr(event, 'from_user'):
                        # For callback events, try to send a new message via bot
                        from aiogram import Bot
                        bot = Bot.get_current()
                        await bot.send_message(event.from_user.id, text, reply_markup=keyboard, parse_mode='HTML')
                        print(f"Sent new message via bot for request {short_id}")
                    else:
                        # For message events, try answer again
                        await event.answer(text, reply_markup=keyboard, parse_mode='HTML')
                        print(f"Sent new message for request {short_id}")
                else:
                    raise
            
        except Exception as e:
            print(f"Error in display_manager_request: {e}")
            error_text = "Xatolik yuz berdi"
            try:
                if hasattr(event, 'message') and hasattr(event.message, 'edit_text'):
                    await event.message.edit_text(error_text)
                elif hasattr(event, 'edit_text'):
                    await event.edit_text(error_text)
                else:
                    print("Cannot display error message - no edit_text method available")
            except Exception as edit_error:
                print(f"Error editing message: {edit_error}")

    @router.callback_query(F.data.startswith("mgr_assign_jm_"))
    async def assign_to_junior_manager(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            full_id = callback.data.replace("mgr_assign_jm_", "")
            short_id = full_id[:8]
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get available junior managers
            junior_managers = await get_users_by_role('junior_manager')
            
            if not junior_managers:
                await callback.message.edit_text("Kichik menejerlar topilmadi")
                return
            
            # Create selection keyboard
            buttons = []
            for jm in junior_managers:
                buttons.append([InlineKeyboardButton(
                    text=f"👨‍💼 {jm.get('full_name', 'N/A')}",
                    callback_data=f"mgr_confirm_jm_{full_id}_{jm['id']}"
                )])
            
            text = (
                f"👨‍💼 <b>Kichik menjer tanlang</b>\n\n"
                f"📝 Ariza ID: {short_id}\n\n"
                f"Quyidagi kichik menejerlardan birini tanlang:"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in assign_to_junior_manager: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("mgr_confirm_jm_"))
    async def confirm_junior_manager_assignment(callback: CallbackQuery, state: FSMContext):
        try:
            parts = callback.data.replace("mgr_confirm_jm_", "").split("_")
            full_id = parts[0]
            junior_manager_id = int(parts[1])
            short_id = full_id[:8]
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Always use full_id from callback data as current_request_id
            current_request_id = full_id
            
            data = await state.get_data()
            
            if not current_request_id:
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Initialize workflow engine and perform assignment
            workflow_engine = MockWorkflowEngine()
            
            # Prepare assignment data
            transition_data = {
                'actor_id': user['id'],
                'junior_manager_id': junior_manager_id,
                'assigned_at': str(datetime.now()),
                'comments': f"Assigned to junior manager by manager {user.get('full_name', 'N/A')}"
            }
            
            success = await workflow_engine.transition_workflow(
                current_request_id,
                "assign_to_junior_manager",
                'manager',
                transition_data
            )
            
            if success:
                # Update word document with manager data
                word_queries = MockWordDocumentQueries()
                
                manager_data = {
                    'manager_name': user.get('full_name', 'N/A'),
                    'manager_id': user['id'],
                    'assigned_junior_manager': 'Test Junior Manager',
                    'assignment_date': datetime.now().isoformat()
                }
                
                await word_queries.update_manager_data(current_request_id, manager_data)
                print(f"Word document updated with manager data for request {current_request_id}")
                
                text = (
                    f"✅ <b>Tayinlash muvaffaqiyatli!</b>\n\n"
                    f"📝 Ariza ID: {short_id}\n"
                    f"👨‍💼 Kichik menjerga yuborildi\n\n"
                    f"Ariza sizning inboxingizdan o'chirilib, kichik menejer inboxiga o'tdi."
                )
                
                await callback.message.edit_text(text, parse_mode='HTML')
                
                # Remove the request from current session
                requests = data.get('inbox_requests', [])
                updated_requests = [r for r in requests if r['id'] != current_request_id]
                current_index = data.get('current_index', 0)
                
                if updated_requests:
                    # Adjust index if needed
                    if current_index >= len(updated_requests):
                        current_index = len(updated_requests) - 1
                    
                    await state.update_data(
                        inbox_requests=updated_requests,
                        current_index=current_index
                    )
                    
                    # Show next request after 2 seconds
                    import asyncio
                    await asyncio.sleep(2)
                    await display_manager_request(callback, state, updated_requests, current_index, lang, user)
                else:
                    await state.clear()
                    
                await callback.answer()
            else:
                await callback.answer("Tayinlashda xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in confirm_junior_manager_assignment: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("mgr_prev_"))
    async def navigate_previous(callback: CallbackQuery, state: FSMContext):
        """Navigate to previous request"""
        try:
            await callback.answer()
            
            # Extract index from callback data
            current_index = int(callback.data.replace("mgr_prev_", ""))
            new_index = current_index - 1
            
            if new_index < 0:
                await callback.answer("Birinchi ariza", show_alert=True)
                return
            
            # Get user and data
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            data = await state.get_data()
            requests = data.get('inbox_requests', [])
            
            if not requests or new_index >= len(requests):
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            # Update current index
            await state.update_data(current_index=new_index)
            
            # Display the previous request
            await display_manager_request(callback, state, requests, new_index, lang, user)
            
        except Exception as e:
            print(f"Error in navigate_previous: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("mgr_next_"))
    async def navigate_next(callback: CallbackQuery, state: FSMContext):
        """Navigate to next request"""
        try:
            await callback.answer()
            
            # Extract index from callback data
            current_index = int(callback.data.replace("mgr_next_", ""))
            new_index = current_index + 1
            
            # Get user and data
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            data = await state.get_data()
            requests = data.get('inbox_requests', [])
            
            if not requests or new_index >= len(requests):
                await callback.answer("Oxirgi ariza", show_alert=True)
                return
            
            # Update current index
            await state.update_data(current_index=new_index)
            
            # Display the next request
            await display_manager_request(callback, state, requests, new_index, lang, user)
            
        except Exception as e:
            print(f"Error in navigate_next: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router
