from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import UserCreate, UserLogin
from model.user_model import User
from schemas.user_schema_response_models import SuccessResponse, LoginResponse, ErrorResponse, UserRegistrationResponse
from exceptions.user_exception import *
from fastapi.responses import JSONResponse
from jwt_auth.token_security import sign_jwt
import re

router = APIRouter()

# Password strength check function
def is_strong_password(password: str) -> bool:
    if (
        len(password) >= 8
        and re.search(r"\d", password)
        and re.search(r"[a-z]", password)
        and re.search(r"[A-Z]", password)
        and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    ):
        return True
    else:
        raise WeakPasswordException()

# Username validation function
def is_correct_username(username: str):
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        raise InvalidUsernameException()

@router.post("/register", response_model=UserRegistrationResponse, responses={
        400: {"description": "Bad Request", "model": ErrorResponse},
        422: {"description": "Validation Error", "model": ErrorResponse},
    },tags=['users']
)
def register(user: UserCreate):
    if not user.username or not user.password:
        raise UsernameAndPasswordRequired()
    is_correct_username(user.username)
    normalize_username = user.username.lower()
    normalize_role = user.role.lower() if user.role else "user"
    if normalize_role not in ("admin", "user"):
        raise InvalidRoleException()
    is_strong_password(user.password)
    existing_user = User.objects(username=normalize_username).first()  # type: ignore
    if existing_user:
        raise UserAlreadyExistsException()

    new_user = User(username=normalize_username, role=normalize_role)
    new_user.set_password(user.password)
    new_user.save()

    return UserRegistrationResponse(
        id=str(new_user.id),  # type: ignore
        username=new_user.username,  # type: ignore
        role=new_user.role,  # type: ignore
        message="User registered successfully.",
    )

@router.post("/login", response_model=LoginResponse,responses={
        400: {"description": "Invalid Credentials", "model": ErrorResponse},
        404: {"description": "User Not Found", "model": ErrorResponse},
    },tags=['users']
)
def login(user: UserLogin):
    if not user.username or not user.password:
        raise UsernameAndPasswordRequired()

    normalize_username = user.username.lower()
    existing_user = User.objects(username=normalize_username).first()  # type: ignore
    if not existing_user:
        raise UserNotFoundException()

    if not existing_user.verify_password(user.password):
        raise InvalidCredentialsException()

    token = sign_jwt(str(existing_user.id))
    return LoginResponse(message="Login successful.", token=token) 

