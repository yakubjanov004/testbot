"""
Manager States

This module defines all state classes for the Manager role.
"""

from aiogram.fsm.state import State, StatesGroup


class ManagerMainMenuStates(StatesGroup):
    """Main menu states for manager"""
    main_menu = State()


class ManagerApplicationStates(StatesGroup):
    """Application states for manager"""
    viewing_applications = State()
    entering_application_number = State()
    viewing_application_details = State()


class ManagerFilterStates(StatesGroup):
    """Filter states for manager"""
    selecting_filter = State()
    entering_filter_value = State()
    selecting_filter_type = State()


class ManagerInboxStates(StatesGroup):
    """Inbox states for manager"""
    viewing_messages = State()
    entering_message_number = State()
    viewing_message_details = State()
    entering_comment = State()


class ManagerNotificationStates(StatesGroup):
    """Notification states for manager"""
    sending_notification = State()
    selecting_notification_type = State()
    sending_notification_message = State()


class ManagerStatusStates(StatesGroup):
    """Status states for manager"""
    changing_status = State()
    entering_status_value = State()


class ManagerTechnicianAssignmentStates(StatesGroup):
    """Technician assignment states for manager"""
    selecting_technician = State()
    confirming_assignment = State()


class ManagerWordDocumentStates(StatesGroup):
    """Word document states for manager"""
    creating_document = State()
    selecting_document_type = State() 