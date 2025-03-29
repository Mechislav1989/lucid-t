from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated, List

from domain.users.model import User
from domain.posts.model import Post
from application.users.use_cases import SignupUseCase, LoginUseCase
from application.posts.use_cases import CreatePostUseCase, GetPostsUseCase, DeletePostUseCase
from infrastructure.caching import PostCache
from api.schemas import TokenResponse, PostCreateRequest, PostResponse, UserResponse
from punq import Container
from infrastructure.repositories.users import UserRepository
from infrastructure.security import Security
from project.containers import get_container


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# DI
def get_container_dep() -> Container:
    return get_container()


def get_security(container: Container = Depends(get_container_dep)):
    return container.resolve(Security)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    security: Security = Depends(get_security)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )
    try:
        payload = security.verify_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_repo = get_container().resolve(UserRepository)
    user = await user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user


# Endpoints
@router.post("/signup", response_model=UserResponse)
async def signup(
    email: Annotated[str, Body()],
    password: Annotated[str, Body()]
):
    try:
        use_case = get_container().resolve(SignupUseCase)
        user = await use_case.execute(email, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        use_case = get_container().resolve(LoginUseCase)
        user = await use_case.execute(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    security = get_container().resolve(Security)
    access_token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/posts", response_model=PostResponse)
async def add_post(
    request: PostCreateRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        use_case = get_container().resolve(CreatePostUseCase)
        post = await use_case.execute(request.text, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return PostResponse(
        id=post.id,
        text=post.text,
        user_id=post.user_id,
        created_at=post.created_at
    )


@router.get("/posts", response_model=List[PostResponse])
async def get_posts(
    current_user: User = Depends(get_current_user)
):
    use_case = get_container().resolve(GetPostsUseCase)
    posts = await use_case.execute(current_user.id)
    
    return [
        PostResponse(
            id=post.id,
            text=post.text,
            user_id=post.user_id,
            created_at=post.created_at
        ) for post in posts
    ]


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user)
):
    try:
        use_case = get_container().resolve(DeletePostUseCase)
        success = await use_case.execute(post_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {"message": "Post deleted successfully"}