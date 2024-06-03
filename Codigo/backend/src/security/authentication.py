from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.dependencies import session
from src.services.authentication import AuthenticationService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login",
)


def get_current_user(db_session: Session = Depends(session.get_db), token: str = Depends(oauth2_scheme)):
    try:
        user = AuthenticationService().decode_token(token=token, db=db_session)
        yield user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
