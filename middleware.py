from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from auth_utils import verify_token
from database import SessionLocal, User
import os

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to handle authentication via cookies."""
    
    def __init__(self, app, protected_paths: list = None):
        super().__init__(app)
        self.protected_paths = protected_paths or ["/admin"]
    
    async def dispatch(self, request: Request, call_next):
        # Check if the path requires authentication
        if any(request.url.path.startswith(path) for path in self.protected_paths):
            # Get token from cookie
            token = request.cookies.get("access_token")
            
            if not token:
                # Redirect to login page
                from fastapi.responses import RedirectResponse
                return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
            
            # Remove "Bearer " prefix if present
            if token.startswith("Bearer "):
                token = token[7:]
            
            # Verify token
            payload = verify_token(token)
            if not payload:
                # Invalid token, redirect to login
                from fastapi.responses import RedirectResponse
                return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
            
            # Get user from database
            db = SessionLocal()
            try:
                username = payload.get("sub")
                user = db.query(User).filter(User.username == username).first()
                
                if not user or not user.is_active:
                    # User not found or inactive, redirect to login
                    from fastapi.responses import RedirectResponse
                    return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
                
                # Add user to request state for use in route handlers
                request.state.current_user = user
                
            finally:
                db.close()
        
        response = await call_next(request)
        return response

def get_current_user_from_cookie(request: Request) -> User:
    """Get current user from request state (set by middleware)."""
    if not hasattr(request.state, 'current_user'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return request.state.current_user

def get_current_admin_user(request: Request) -> User:
    """Get current admin user from request state."""
    user = get_current_user_from_cookie(request)
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user
