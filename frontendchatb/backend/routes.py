from fastapi import APIRouter, HTTPException, Depends
from fastapi import Request 
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import UserCreate, UserOut
from db import users_collection
from auth import hash_password, verify_password, create_jwt_token, verify_jwt_token,create_reset_token, verify_reset_token
from datetime import timedelta
from pydantic import BaseModel, EmailStr

router = APIRouter()

@router.get("/")
async def home():
    return {"message": "API is working!"}

@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ Ensure password is hashed correctly (Use async functions if needed)
    hashed_password =  hash_password(user.password)

    # ✅ Store user securely
    user_data = {"email": user.email, "password": hashed_password}
    await users_collection.insert_one(user_data)

    # ✅ Generate JWT Token
    token = create_jwt_token({"sub": user.email}, expires_delta=timedelta(hours=1))
    return {"email": user.email, "token": token}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # ✅ Fix OAuth2PasswordRequestForm issue (username = email)
    db_user = await users_collection.find_one({"email": form_data.username})
    
    if not db_user or not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Generate JWT Token
    token = create_jwt_token({"sub": db_user["email"]}, expires_delta=timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected")
async def protected_route(current_user_email: str = Depends(verify_jwt_token)):
    return {"message": f"Hello, {current_user_email}. You have access to this route."}

class ForgotPasswordRequest(BaseModel):
    email: EmailStr  # Ensures it's a valid email format

from pydantic import BaseModel, EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr  # Ensures it's a valid email format

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    email = request.email
    user = await users_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = create_reset_token(email)
    reset_link = f"http://127.0.0.1:5500/reset-password?token={reset_token}"

    # TODO: Send the email (for now, just print)
    print(f"Reset Link: {reset_link}")

    return {"message": "Password reset link sent!"}


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    
@router.get("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    email = verify_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    hashed_password = hash_password(request.new_password)
    await users_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})

    return {"message": "Password reset successful!"}