from typing import List

from config import get_admin_regions
from database.region_config import get_region_codes
from database.core_queries import get_user_role as get_role_in_region


async def detect_user_regions(user_id: int, role: str) -> List[str]:
    """Detect regions assigned to the user for the given role.

    - For admins: read from ADMIN_IDS_<REGION> mapping (env).
    - For other roles: scan configured regions and check user role in each
      regional DB. Regions where the role matches are returned.
    """
    role = (role or "").lower()
    if role == "admin":
        return get_admin_regions(user_id)

    regions = get_region_codes()
    assigned: List[str] = []
    for region in regions:
        try:
            r = await get_role_in_region(region, user_id)
            if r and str(r).lower() == role:
                assigned.append(region)
        except Exception:
            # Ignore per-region errors to keep /start fast
            continue
    return assigned