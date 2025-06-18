from datetime import timedelta

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi.responses import RedirectResponse
from httpx_oauth.oauth2 import OAuth2


from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.database import get_async_db
from app.models import TraktUserAuth, User
from app.schemas import Token, TokenData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession # For async DB operations

from app.database import get_async_db # Will be created in database.py
from app.models import User, TraktUserAuth # We'll need these
from httpx_oauth.oauth2 import OAuth2Token # For type hinting and expires_at

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_async_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.email == token_data.email))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user

trakt_oauth_client = OAuth2(
    client_id=settings.TRAKT_CLIENT_ID,
    client_secret=settings.TRAKT_CLIENT_SECRET,
    authorize_endpoint="https://trakt.tv/oauth/authorize",
    access_token_endpoint="https://api.trakt.tv/oauth/token",
    base_scopes=None,
)

@router.get("/trakt/login", name="auth:trakt-login")
async def trakt_login(request: Request, current_user: User = Depends(get_current_user)):
    redirect_uri = request.url_for("auth:trakt-callback")
    state = str(current_user.id)
    authorization_url = await trakt_oauth_client.get_authorization_url(
        redirect_uri=str(redirect_uri), state=state
    )
    return RedirectResponse(authorization_url)

@router.get("/trakt/callback", name="auth:trakt-callback")
async def trakt_callback(request: Request, code: str, state: str, db: AsyncSession = Depends(get_async_db)):
    redirect_uri = request.url_for("auth:trakt-callback")
    try:
        token_data = await trakt_oauth_client.get_access_token(code, redirect_uri=str(redirect_uri))
    except Exception as e:
        print(f"Error exchanging Trakt token: {e}")
        return {"error": "Failed to authenticate with Trakt", "details": str(e)}

    # The user_id is passed via the state parameter
    user_id_to_update = int(state)

    result = await db.execute(select(TraktUserAuth).where(TraktUserAuth.user_id == user_id_to_update))
    trakt_auth = result.scalar_one_or_none()

    # Extract all required fields from the Trakt response
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")
    created_at = token_data.get("created_at")
    scope = token_data.get("scope", "")
    scope_str = " ".join(scope) if isinstance(scope, list) else str(scope)
    token_type = token_data.get("token_type", "bearer")

    if trakt_auth:
        # Update existing record
        trakt_auth.access_token = access_token
        trakt_auth.refresh_token = refresh_token
        trakt_auth.expires_in = expires_in
        trakt_auth.created_at = created_at
        trakt_auth.scope = scope_str
        trakt_auth.token_type = token_type
        db.add(trakt_auth)
        message = f"Trakt tokens for user {user_id_to_update} updated."
    else:
        # Create new record
        trakt_auth = TraktUserAuth(
            user_id=user_id_to_update,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            created_at=created_at,
            scope=scope_str,
            token_type=token_type,
        )
        db.add(trakt_auth)
        message = f"Trakt tokens for user {user_id_to_update} created."

    await db.commit()
    await db.refresh(trakt_auth)

    return {"message": message, "user_id": user_id_to_update}

# Include this router in your main FastAPI app
