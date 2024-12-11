from datetime import datetime, timedelta
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, auth
from .database import engine, get_db, SessionLocal

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales API", description="API for managing sales with OAuth2 authentication")

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/users/api-key/", response_model=schemas.UserApiKey)
async def generate_user_api_key(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    api_key = auth.generate_api_key()
    current_user.api_key = api_key
    current_user.api_key_created_at = datetime.utcnow()
    db.commit()
    return {"api_key": api_key}

@app.get("/sales/", response_model=List[schemas.Sale])
async def read_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user_or_api_key)
):
    sales = db.query(models.Sale).offset(skip).limit(limit).all()
    return sales

@app.get("/sales/{sale_id}", response_model=schemas.Sale)
async def read_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user_or_api_key)
):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@app.post("/sales/", response_model=schemas.Sale)
async def create_sale(
    sale: schemas.SaleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user_or_api_key)
):
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

# Initialize a test user if none exists
@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        # Check if test user exists
        test_user = db.query(models.User).filter(models.User.email == "test@example.com").first()
        if not test_user:
            # Create test user
            hashed_password = auth.get_password_hash("testpassword")
            test_user = models.User(email="test@example.com", hashed_password=hashed_password)
            db.add(test_user)
            db.commit()
            
            # Add sample sales data
            for i in range(100):
                sale = models.Sale(
                    date=datetime.now().date(),
                    product_name=f"Product {i+1}",
                    quantity=i+1,
                    unit_price=10.0,
                    total_amount=(i+1) * 10.0,
                    customer_name=f"Customer {i+1}"
                )
                db.add(sale)
            db.commit()
    finally:
        db.close()
