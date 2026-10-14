import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import get_db
from app.models.user import User

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer



# oauth2_scheme = OAuth2PasswordBearer(
#   tokenUrl="/api/v1/auth/login"
# )

bearer_scheme = HTTPBearer()


def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
  db: Session = Depends(get_db),
) -> User:
  token = credentials.credentials

  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  try:
    payload = jwt.decode(
      token,
      settings.SECRET_KEY,
      algorithms=[ALGORITHM],
    )

    user_id = payload.get("sub")

    if user_id is None:
      raise credentials_exception

    user_id = int(user_id)

  except (InvalidTokenError, ValueError, TypeError):
    raise credentials_exception

  user = db.query(User).filter(User.id == user_id).first()

  if user is None:
    raise credentials_exception

  if not user.is_active:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="User account is inactive",
    )

  return user