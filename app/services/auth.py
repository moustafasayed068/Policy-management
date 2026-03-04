from fastapi import HTTPException, status
from app.models.user import RoleEnum 

def verify_admin_access(user):
    # This function checks if the user has HR or Admin role before allowing access to certain endpoints.
    if user.role not in [RoleEnum.hr, RoleEnum.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: This action requires HR or Admin privileges."
        )