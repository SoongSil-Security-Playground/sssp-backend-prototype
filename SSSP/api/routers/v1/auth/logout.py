from fastapi import APIRouter, Response, HTTPException

# directory dependency

router = APIRouter()


@router.post("/logout")
def logout(response: Response):
    try:
        response.delete_cookie("access_token")
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Invalid token or already logged out."
        )
