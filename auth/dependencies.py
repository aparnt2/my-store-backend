from fastapi import Depends, HTTPException, status
from auth.token_utils import get_current_user

def admin_only(current_user=Depends(get_current_user)):
    if current_user.sr_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access only"
        )
    return current_user

def admin_or_employee(current_user=Depends(get_current_user)):
    if current_user.sr_id not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Employee access only"
        )
    return current_user
