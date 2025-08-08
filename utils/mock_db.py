from typing import Dict, Any, List
from datetime import datetime

# In-memory mock storage
_users: Dict[int, Dict[str, Any]] = {}
_orders: Dict[int, List[Dict[str, Any]]] = {}


def create_or_get_user(telegram_id: int) -> Dict[str, Any]:
    user = _users.get(telegram_id)
    if not user:
        user = {
            'telegram_id': telegram_id,
            'language': 'uz',
            'phone_number': None,
            'full_name': None,
            'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        _users[telegram_id] = user
    return user


def get_user(telegram_id: int) -> Dict[str, Any] | None:
    return _users.get(telegram_id)


def is_registered(telegram_id: int) -> bool:
    user = _users.get(telegram_id)
    return bool(user and user.get('phone_number') and user.get('full_name'))


def set_language(telegram_id: int, language: str) -> None:
    user = create_or_get_user(telegram_id)
    user['language'] = language


def set_phone(telegram_id: int, phone_number: str) -> None:
    user = create_or_get_user(telegram_id)
    user['phone_number'] = phone_number


def set_full_name(telegram_id: int, full_name: str) -> None:
    user = create_or_get_user(telegram_id)
    user['full_name'] = full_name


def update_user_field(telegram_id: int, field: str, value: Any) -> None:
    user = create_or_get_user(telegram_id)
    user[field] = value


def _ensure_mock_orders(telegram_id: int) -> None:
    if telegram_id in _orders:
        return
    # Create 5 mock orders
    orders = [
        {
            'id': 1,
            'type': 'service',
            'status': 'active',
            'created_at': '2024-01-15 10:30:00',
            'description': "Internet tezligi sekin",
            'region': "Toshkent shahri",
            'address': "Chilanzar tumani, 15-uy",
            'request_id': 'TX_12345678'
        },
        {
            'id': 2,
            'type': 'connection',
            'status': 'completed',
            'created_at': '2024-01-10 14:20:00',
            'description': "Yangi ulanish",
            'region': "Toshkent viloyati",
            'address': "Zangiota tumani, 25-uy",
            'request_id': 'UL_87654321'
        },
        {
            'id': 3,
            'type': 'service',
            'status': 'pending',
            'created_at': '2024-01-12 09:15:00',
            'description': "TV signal yo'q",
            'region': "Andijon",
            'address': "Andijon shahri, 8-uy",
            'request_id': 'TX_11223344'
        },
        {
            'id': 4,
            'type': 'connection',
            'status': 'active',
            'created_at': '2024-01-08 16:45:00',
            'description': "Uy internet ulanishi",
            'region': "Farg'ona",
            'address': "Farg'ona shahri, 12-uy",
            'request_id': 'UL_55667788'
        },
        {
            'id': 5,
            'type': 'service',
            'status': 'completed',
            'created_at': '2024-01-05 11:30:00',
            'description': 'Router muammosi',
            'region': 'Samarqand',
            'address': 'Samarqand shahri, 30-uy',
            'request_id': 'TX_99887766'
        }
    ]
    _orders[telegram_id] = orders


def get_user_orders(telegram_id: int, page: int = 1, limit: int = 5) -> Dict[str, Any]:
    _ensure_mock_orders(telegram_id)
    orders = _orders[telegram_id]
    start = (page - 1) * limit
    end = start + limit
    paginated_orders = orders[start:end]
    return {
        'orders': paginated_orders,
        'total': len(orders),
        'page': page,
        'total_pages': (len(orders) + limit - 1) // limit
    }


def get_order_details(telegram_id: int, order_id: int) -> Dict[str, Any] | None:
    _ensure_mock_orders(telegram_id)
    for order in _orders[telegram_id]:
        if order['id'] == order_id:
            return order
    return None