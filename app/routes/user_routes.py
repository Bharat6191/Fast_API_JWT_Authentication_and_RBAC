from fastapi import APIRouter, Depends, HTTPException,status
from model.user_model import User
from schemas.user_schema import UserCreate,UserLogin
from fastapi.responses import JSONResponse
from jwt_auth.token_security import sign_jwt
import re

router = APIRouter()

def is_strong_password(password: str) -> bool:
    if (len(password) >= 8 and 
        re.search(r'\d', password) and 
        re.search(r'[a-z]', password) and 
        re.search(r'[A-Z]', password) and 
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    else:
        return False

def is_correct_username(username:str):
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username must only contain letters, numbers, and underscores."
            )


@router.post('/register',tags=['user'])
def register(user:UserCreate):
    try:
        if not user.username or not user.password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username and password are required."
            )
        
        is_correct_username(user.username)

        normalize_username = user.username.lower()
        normalize_role = user.role.lower() if user.role else 'user'
        if normalize_role not in ('admin','user'):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="user role either be admin or user"
            )
        if not is_strong_password(user.password):
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=("Password must be at least 8 characters long, "
                    "contain at least one digit, one lowercase letter, "
                    "one uppercase letter, and one special character.")
            )
        
        existing_user=User.objects(username=normalize_username).first() # type: ignore
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User already exists")
        
        new_user=User(username=normalize_username,role=normalize_role)
        new_user.set_password(user.password)
        new_user.save()
        return JSONResponse(
            status_code=201,
            content={'message':'User register successfully'})
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the request: {str(e)}"
        )

@router.post('/login',tags=['user'])
def login(user:UserLogin):
    try:
        if not user.username or not user.password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Username and password are required."
            )
        normalize_username=user.username.lower()
        existing_user=User.objects(username=normalize_username).first() # type: ignore
        if not existing_user or not existing_user.verify_password(user.password):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid username and password"
        )
        return sign_jwt(str(existing_user.id))
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the request: {str(e)}"
        )


