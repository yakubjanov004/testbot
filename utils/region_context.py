from typing import List

from config import get_admin_regions
from database.region_config import get_region_codes
from database.core_queries import get_user_role as get_role_in_region


async def detect_user_regions(user_id: int, role: str) -> List[str]:
    """Detect regions assigned to the user for the given role.

    - Adminlar uchun: .env dagi ADMIN_IDS_<REGION> ro'yxatlari BILAN BIRGA
      regional DB'lardagi `role='admin'` mos tushgan regionlar ham birgalikda olinadi.
    - Boshqa rollar uchun: faqat regional DB'dagi rol mos kelgan regionlar qaytariladi.
    """
    role = (role or "").lower()

    regions = get_region_codes()
    assigned: List[str] = []

    # DB bo'yicha rolni tekshirib chiqamiz
    for region in regions:
        try:
            r = await get_role_in_region(region, user_id)
            if r and str(r).lower() == role:
                assigned.append(region)
        except Exception:
            # Ignore per-region errors to keep /start fast
            continue

    # Adminlar uchun .env dagi regionlar bilan union
    if role == "admin":
        env_regions = set(get_admin_regions(user_id))
        assigned = sorted(set(assigned) | env_regions)

    return assigned