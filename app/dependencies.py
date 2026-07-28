from fastapi import Depends, HTTPException, status

from app.models import User
from app.oauth2 import get_current_user


def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )
    return current_user


def transport_manager_or_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ["Admin", "Transport Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Transport Manager or Admin access required."
        )
    return current_user


def parent_only(current_user: User = Depends(get_current_user)):
    if current_user.role != "Parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Parent access required."
        )
    return current_user


def authenticated_user(
    current_user: User = Depends(get_current_user),
):
    return current_user