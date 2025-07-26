from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer
from models import User, TokenData, UserRole
import os
from typing import Optional

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

security = HTTPBearer()

class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        
        if user_id is None:
            raise AuthError("Invalid token")
        
        token_data = TokenData(
            user_id=user_id,
            email=email,
            role=UserRole(role) if role else None
        )
        return token_data
    except jwt.ExpiredSignatureError:
        raise AuthError("Token has expired")
    except jwt.JWTError:
        raise AuthError("Invalid token")

def get_token_from_request(request: Request) -> Optional[str]:
    """Extract token from Authorization header or cookies."""
    # First try Authorization header
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ")[1]
    
    # Then try httpOnly cookie
    token = request.cookies.get("access_token")
    if token:
        return token
    
    return None

async def get_current_user(request: Request) -> TokenData:
    """Get current user from request."""
    token = get_token_from_request(request)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        token_data = verify_token(token)
        return token_data
    except AuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_coach(request: Request) -> TokenData:
    """Get current user and ensure they are a coach."""
    current_user = await get_current_user(request)
    
    if current_user.role != UserRole.COACH:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Coach access required."
        )
    
    return current_user

async def get_current_athlete(request: Request) -> TokenData:
    """Get current user and ensure they are an athlete."""
    current_user = await get_current_user(request)
    
    if current_user.role != UserRole.ATHLETE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Athlete access required."
        )
    
    return current_user