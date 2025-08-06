"""
Controller States

This module defines all state classes for the Controller role.
"""

from aiogram.fsm.state import State, StatesGroup


class ControllerMainMenuStates(StatesGroup):
    """Main menu states for controller"""
    main_menu = State()


class ControllerStates(StatesGroup):
    """General states for controller"""
    viewing_requests = State()
    entering_request_number = State()
    viewing_request_details = State()


class ControllerApplicationStates(StatesGroup):
    """Application states for controller"""
    entering_phone = State()
    entering_name = State()
    entering_description = State()
    entering_location = State()
    selecting_priority = State()
    confirming_application = State()


class ControllerOrdersStates(StatesGroup):
    """Order states for controller"""
    viewing_orders = State()
    entering_order_number = State()
    viewing_order_details = State()


class ControllerQualityStates(StatesGroup):
    """Quality states for controller"""
    viewing_quality = State()
    entering_quality_assessment = State()


class ControllerReportsStates(StatesGroup):
    """Reports states for controller"""
    viewing_reports = State()
    selecting_report_type = State()


class ControllerSettingsStates(StatesGroup):
    """Settings states for controller"""
    selecting_language = State()


class ControllerTechnicianStates(StatesGroup):
    """Technician states for controller"""
    selecting_technician = State()
    confirming_assignment = State()


class ControllerRequestStates(StatesGroup):
    """Request states for controller"""
    waiting_for_technician = State()
    waiting_for_comment = State() 