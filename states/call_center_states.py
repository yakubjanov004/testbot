"""
Call Center States (Additional)

This module defines additional state classes for the Call Center role.
"""

from aiogram.fsm.state import State, StatesGroup





class CallCenterDirectResolutionStates(StatesGroup):
    """Direct resolution states for call center"""
    selecting_problem_type = State()
    entering_resolution = State()


class CallCenterChatStates(StatesGroup):
    """Chat states for call center"""
    waiting_for_reply = State()
    viewing_chat = State()
    selecting_chat = State()


class CallCenterMainMenuStates(StatesGroup):
    """Main menu states for call center"""
    main_menu = State()
    chat_menu = State()
    orders_menu = State()
    clients_menu = State()
    feedback_menu = State()
    statistics_menu = State()


class CallCenterClientsStates(StatesGroup):
    """Clients states for call center"""
    clients = State()
    waiting_for_search_query = State()
    waiting_for_client_data = State()
    waiting_for_client_id = State()
    viewing_client_profile = State()
    editing_client = State()


class CallCenterFeedbackStates(StatesGroup):
    """Feedback states for call center"""
    feedback = State()
    waiting_for_feedback_data = State()
    waiting_for_search_query = State() 


class CallCenterClientSearchStates(StatesGroup):
    """Client search states for call center (controller-like)"""
    selecting_client_search_method = State()
    entering_phone = State()
    entering_name = State()
    entering_client_id = State()
    entering_new_client_name = State()
    selecting_client = State()


class CallCenterConnectionOrderStates(StatesGroup):
    """Connection order creation states for call center (client-like)"""
    selecting_region = State()
    selecting_connection_type = State()
    selecting_tariff = State()
    entering_address = State()
    asking_for_geo = State()
    waiting_for_geo = State()
    confirming_connection = State()


class CallCenterServiceOrderStates(StatesGroup):
    """Service order creation states for call center (client-like)"""
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


class CallCenterStandaloneSearchStates(StatesGroup):
    """Standalone client search states for call center main menu search"""
    selecting_method = State()
    entering_phone = State()
    entering_name = State()
    entering_id = State()
    selecting_client = State() 