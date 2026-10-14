
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
  create_access_token,
  hash_password,
  verify_password,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse

from app.core.dependencies import get_current_user

router = APIRouter()


@router.post(
  "/register",
  response_model=UserResponse,
  status_code=status.HTTP_201_CREATED,
)
def register_user(
  user_data: UserCreate,
  db: Session = Depends(get_db),
):
  existing_user = (
    db.query(User)
    .filter(User.email == user_data.email)
    .first()
  )

  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="Email is already registered.",
    )

  new_user = User(
    username=user_data.username,
    email=user_data.email,
    password_hash=hash_password(user_data.password),
    role="sales_staff",
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user


@router.post("/login")
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
  user = (
    db.query(User)
    .filter(User.email == user_data.email)
    .first()
  )

  if not user or not verify_password(
    user_data.password,
    user.password_hash,
  ):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid email or password",
      headers={"WWW-Authenticate": "Bearer"},
    )

  if not user.is_active:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="User account is inactive",
    )

  access_token = create_access_token(subject=str(user.id))

  return {
    "access_token": access_token,
    "token_type": "bearer",
  }


@router.get("/me", response_model=UserResponse)
def read_current_user(
  current_user: User = Depends(get_current_user),
):
  return current_user
