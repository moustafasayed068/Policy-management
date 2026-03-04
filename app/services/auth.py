from fastapi import HTTPException, status

def verify_admin_access(user):
    if user.role not in ["hr", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR or admin can perform this action"
        )