from datetime import datetime

# Mock functions to replace utils and database imports
async def get_users_by_role(role: str):
    """Mock get users by role"""
    if role == 'manager':
        return [
            {
                'id': 1,
                'full_name': 'Test Manager',
                'phone_number': '+998901234567',
                'role': 'manager',
                'is_active': True
            }
        ]
    elif role == 'technician':
        return [
            {
                'id': 2,
                'full_name': 'Test Technician',
                'phone_number': '+998901234568',
                'role': 'technician',
                'is_active': True
            }
        ]
    return []

async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567'
    }

async def create_word_document_record(request_id: str, document_type: str, user_id: int, order_data: dict = None):
    """Create word_documents record when a request is created"""
    try:
        # Start enhanced time tracking for word document creation
        # Mock time tracking
        pass
        
        # Track workflow transition for word document creation
        # Mock workflow transition
        pass
        
        # Prepare document data
        document_data = {
            "request_id": request_id,
            "document_type": document_type,
            "application_date": datetime.now().date(),
            "application_time": datetime.now().time(),
            "created_by": user_id,
            "order_data": order_data or {}
        }
        
        # Mock word document ID
        word_doc_id = f"doc_{request_id}_{int(datetime.now().timestamp())}"
        
        # Track application handling
        # Mock application tracking
        pass
        
        # Update enhanced statistics
        # Mock statistics generation
        pass
        
        # Log word document creation
        # Mock audit logging
        pass
        
        # End enhanced time tracking
        # Mock time tracking end
        pass
        
        return word_doc_id
        
    except Exception as e:
        # Mock audit logging for errors
        pass
        return None

async def format_group_zayavka_message(order_type, public_id, user, phone, address, description, tariff=None, abonent_type=None, abonent_id=None, geo=None, media=None, user_id=None):
    """Format group notification message for both connection and service requests - SHORT VERSION"""
    
    try:
        # Start enhanced time tracking for message formatting
        if user_id:
            # Mock time tracking
            pass
            
            # Track workflow transition for message formatting
            # Mock workflow transition
            pass
        
        if order_type == 'service':
            title = '🛠️ <b>YANGI TEXNIK XIZMAT ARIZASI</b>'
            emoji = '🛠️'
        else:
            title = '🔌 <b>YANGI ARIZA</b>'
            emoji = '🔌'
        
        # Only essential user info
        user_name = user.get('full_name', 'N/A') if user else 'N/A'
        user_phone = phone or user.get('phone_number', 'N/A') if user else 'N/A'
        
        # Essential info only
        essential_info = []
        if address:
            essential_info.append(f"📍 {address}")
        if description:
            # Truncate description if too long
            desc = description[:100] + "..." if len(description) > 100 else description
            essential_info.append(f"📝 {desc}")
        if tariff:
            essential_info.append(f"💳 {tariff}")
        if abonent_id:
            essential_info.append(f"🆔 {abonent_id}")
        
        # Status indicators for service requests
        status_info = []
        if order_type == 'service':
            if geo:
                status_info.append("📍 Lokatsiya yuborilgan")
            if media:
                status_info.append("🖼 Media yuborilgan")
        
        status_text = " ".join(status_info) if status_info else ""
        
        msg = (
            f"{title}\n"
            f"🆔 <b>ID:</b> {public_id or 'N/A'}\n"
            f"👤 <b>Ismi:</b> {user_name}\n"
            f"📞 <b>Telefoni:</b> {user_phone}\n"
            f"{chr(10).join(essential_info)}\n"
            f"{status_text}\n"
            f"⏰ {datetime.now().strftime('%H:%M')}"
        )
        
        # Track application handling
        if user_id and public_id:
            # Mock application tracking
            pass
        
        # Update enhanced statistics
        if user_id:
            # Mock statistics generation
            pass
        
        # Log message formatting
        if user_id:
            # Mock audit logging
            pass
        
        # End enhanced time tracking
        if user_id:
            # Mock time tracking end
            pass
        
        return msg
        
    except Exception as e:
        if user_id:
            # Mock audit logging for errors
            pass
        # Return basic message on error
        return f"❌ Xatolik: {order_type} arizasi formati"

async def validate_group_notification_config(group_id, user_id=None):
    """Validate group notification configuration"""
    try:
        # Start enhanced time tracking for validation
        if user_id:
            # Mock time tracking
            pass
            
            # Track workflow transition for validation
            # Mock workflow transition
            pass
        
        # Basic validation
        if not group_id:
            return False, "Group ID is missing"
        
        # Track application handling
        if user_id:
            # Mock application tracking
            pass
        
        # Update enhanced statistics
        if user_id:
            # Mock statistics generation
            pass
        
        # Log validation
        if user_id:
            # Mock audit logging
            pass
        
        # End enhanced time tracking
        if user_id:
            # Mock time tracking end
            pass
        
        return True, "Configuration is valid"
        
    except Exception as e:
        if user_id:
            # Mock audit logging for errors
            pass
        return False, f"Validation error: {str(e)}"

async def format_notification_error_message(error_type, details, user_id=None):
    """Format error message for notifications"""
    try:
        # Start enhanced time tracking for error formatting
        if user_id:
            # Mock time tracking
            pass
            
            # Track workflow transition for error formatting
            # Mock workflow transition
            pass
        
        error_messages = {
            'group_not_found': '❌ Guruh topilmadi',
            'permission_denied': '❌ Ruxsat yo\'q',
            'message_too_long': '❌ Xabar juda uzun',
            'invalid_format': '❌ Noto\'g\'ri format',
            'network_error': '❌ Tarmoq xatosi',
            'unknown_error': '❌ Noma\'lum xatolik'
        }
        
        error_msg = error_messages.get(error_type, error_messages['unknown_error'])
        if details:
            error_msg += f": {details}"
        
        # Track application handling
        if user_id:
            # Mock application tracking
            pass
        
        # Update enhanced statistics
        if user_id:
            # Mock statistics generation
            pass
        
        # Log error formatting
        if user_id:
            # Mock audit logging
            pass
        
        # End enhanced time tracking
        if user_id:
            # Mock time tracking end
            pass
        
        return error_msg
        
    except Exception as e:
        if user_id:
            # Mock audit logging for errors
            pass
        return "❌ Xatolik yuz berdi"

async def send_short_role_notification(request_id: str, order_type: str, user: dict, user_id: int):
    """Send short notification to users by role - just client info and request ID"""
    try:
        # Start enhanced time tracking for short notification
        # Mock time tracking
        pass
        
        # Track workflow transition for short notification
        # Mock workflow transition
        pass
        
        # Determine target role based on order type
        target_role = "manager" if order_type == "connection" else "controller"
        
        # Get users with target role
        target_users = await get_users_by_role(target_role)
        
        if not target_users:
            return False
        
        # Format short notification message (1 line)
        client_name = user.get('full_name', 'N/A') if user else 'N/A'
        short_id = request_id[:8] if request_id else 'N/A'
        
        if order_type == "connection":
            notification_msg = f"🔌 Client: {client_name} | ID: {short_id}"
        else:
            notification_msg = f"🛠️ Client: {client_name} | ID: {short_id}"
        
        # Track application handling
        await application_tracker.track_application_handling(
            application_id=request_id,
            handler_id=user_id,
            action=f"short_{order_type}_notification_sent_to_{target_role}"
        )
        
        # Update enhanced statistics
        await statistics_manager.generate_role_based_statistics('client', 'daily')
        
        # Log successful short notification
        await audit_logger.log_user_action(
            user_id=user_id,
            action="short_notification_sent",
            details={
                "request_id": request_id,
                "order_type": order_type,
                "target_role": target_role,
                "success_count": len(target_users),
                "total_target_users": len(target_users)
            }
        )
        
        # End enhanced time tracking
        await time_tracker.end_role_tracking(
            request_id=f"short_notification_{request_id}",
            user_id=user_id,
            notes=f"Short notification sent to {len(target_users)} {target_role} users"
        )
        
        return True
        
    except Exception as e:
        await audit_logger.log_system_event(
            event_type="short_notification_error",
            description=f"Error in send_short_role_notification: {str(e)}",
            severity="error"
        )
        return False
