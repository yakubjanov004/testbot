"""
Controller States

This module defines all state classes for the Controller role.
"""

from aiogram.fsm.state import State, StatesGroup


class ControllerMainMenuStates(StatesGroup):
    """Main menu states for controller"""
    main_menu = State()
    export_selection = State()
    export_format_selection = State()


class ControllerStates(StatesGroup):
    """General states for controller"""
    viewing_requests = State()
    entering_request_number = State()
    viewing_request_details = State()


class ControllerApplicationStates(StatesGroup):
    """Application states for controller (search and common)"""
    selecting_client_search_method = State()
    entering_phone = State()
    entering_name = State()
    entering_client_id = State()
    entering_new_client_name = State()
    selecting_client = State()
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


# Controller flows mirroring client flows (DB-less)
class ControllerServiceOrderStates(StatesGroup):
    """Service order creation states for controller (client-like)"""
    selecting_region = State()
    selecting_order_type = State()
    waiting_for_abonent_id = State()
    entering_description = State()
    asking_for_media = State()
    waiting_for_media = State()
    entering_address = State()
    asking_for_location = State()
    waiting_for_location = State()
    confirming_order = State()


class ControllerConnectionOrderStates(StatesGroup):
    """Connection order creation states for controller (client-like)"""
    selecting_region = State()
    selecting_connection_type = State()
    selecting_tariff = State()
    entering_address = State()
    asking_for_geo = State()
    waiting_for_geo = State()
    confirming_connection = State() 