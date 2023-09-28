from fastapi import Depends, FastAPI, HTTPException, Form, Query
from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict
from sqlalchemy import select
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
import crud, schemas, models
from database import SessionLocal, engine, base

base.metadata.create_all(bind=engine)


Page = Page.with_custom_options(size=Query(5, ge=1, le=5))


app = FastAPI()



psswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

key = "6d6b410063ba81ca359a874859d7735db8fd4d9d2891266b01d085d6b3fc13e1"

algorithm = "HS256"

token_expiration = 20

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---- USERS/AUTHENTICATION -------------------------------------------------------------------------------------

@app.get("/auth/")
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=401,
        detail="Access denied, unable to validate credentials.",
        headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        username: str = payload.get("Sub")
        if not username:
            raise credential_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = crud.get_user_from_name(db=db, username=username)
    if user is None:
        raise credential_exception
    return user


@app.get("/users/me/")
async def read_user(current_user: Annotated[schemas.UserBase, Depends (get_current_user)]):
    return current_user


def get_user(db: Session, username: str):
    db_user = crud.get_user_from_name(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return username


def hash_password(user_password: str):
    return psswd_context.hash(user_password)

def verify_password(user_password, hash_password):
    return psswd_context.verify(user_password, hash_password)


def decode_token(token):
    payload = jwt.decode(token, key, algorithms=[algorithm])
    return payload

def authenticate_user(db: Session, username: str, user_password: str):
     user = get_user(username=username, db=db)
     db_password = crud.get_user_from_name(username=username, db=db)
     check_password = db_password.user_password
     if user is None:
        return False
     if verify_password(user_password, check_password) is None:
        return False
     return user


@app.post("/token", response_model= schemas.token)
async def login(form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(username=form_data.username, user_password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", 
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    token_expiration_time = timedelta(minutes=token_expiration)
    access_token = create_token(data={"Sub": user}, expiration = token_expiration_time)
    return {"access_token": access_token, "token_type": "bearer"}

def create_token(data: dict, expiration: timedelta | None = None):
    to_encode = data.copy()
    if expiration:
        expire = datetime.utcnow() + expiration
    else:
        expire = datetime.uctnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded_jwt


@app.post("/users/", response_model=dict)
def create_user(username: Annotated[str, Form()], user_password: Annotated[str, Form()], db: Session = Depends(get_db)):
    hashed_password = hash_password(user_password=user_password)
    db_user = schemas.userCreate(username=username, user_password=hashed_password)
    check = crud.get_user_from_name(db=db, username=username)
    if check:
        raise HTTPException(status_code=400, detail="Username is already taken")
    return crud.create_user(db=db, user=db_user)

@app.delete("/users/", response_model=dict)
def delete_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_from_name(db=db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, user=db_user)

# ---- VIDEOS ---------------------------------------------------------------------------------------------------------

@app.get("/videos/free/", response_model=Page[schemas.video])
def read_free_videos(db: Session = Depends(get_db)):
    return paginate(db, select(models.Video).where(models.Video.category_id == 1))

@app.get ("/videos/", response_model=Page[schemas.video])
def read_videos(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    return paginate(db, select(models.Video).order_by(models.Video.category_id))

@app.get("/videos/{id}", response_model=schemas.video)
def read_video(token: Annotated[str, Depends(oauth2_scheme)], id: int, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_video = crud.get_video(db, id=id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video

@app.post("/videos/", response_model=schemas.video)
def add_video(token: Annotated[str, Depends(oauth2_scheme)], video: schemas.videosCreate, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.add_video(db=db, video=video)

@app.patch("/videos/{id}", response_model=schemas.video)
def update_video(token: Annotated[str, Depends(oauth2_scheme)], id: int , video: schemas.videosUpdate, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_video = crud.get_video(db, id=id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return crud.update_video(db=db, video=db_video , update=video)

@app.delete("/videos/{id}", response_model=dict)
def delete_video(token: Annotated[str, Depends(oauth2_scheme)], id:int, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_video = crud.get_video(db, id=id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return crud.delete_video(db=db, db_video=db_video, id=id)

# ---- CATEGORIES --------------------------------------------------------------------------------------------------

@app.get("/categories/{title}/", response_model=list[schemas.video])
def get_videos_by_category(token: Annotated[str, Depends(oauth2_scheme)], title: str,  db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_category = crud.get_category_by_name(db=db, title=title)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.get_videos_by_category(db=db, category=db_category)

@app.get("/categories/", response_model=list[schemas.category])
def get_all_categories(token: Annotated[str, Depends(oauth2_scheme)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    return crud.read_categories(db=db, skip=skip)

@app.get("/categories/{id}", response_model=schemas.category)
def get_category(token: Annotated[str, Depends(oauth2_scheme)], id: int, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_category = crud.read_category(db=db, id=id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.post("/categories/", response_model=schemas.category)
def add_category(token: Annotated[str, Depends(oauth2_scheme)], category: schemas.categoryCreate, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_category = crud.get_category_by_name(db=db, title=category.title)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud.add_category(db=db, category=category)

@app.patch("/categories/", response_model=schemas.category)
def update_category(token: Annotated[str, Depends(oauth2_scheme)], id:int, category: schemas.categoryUpdate, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_category = crud.read_category(db=db, id=id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.update_category(db=db, category=db_category, update=category)

@app.delete("/categories/", response_model=dict)
def delete_category(token: Annotated[str, Depends(oauth2_scheme)], id:int, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_category = crud.read_category(db=db, id=id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.delete_category(db=db, db_category=db_category)

@app.get("/video/", response_model=schemas.video)
def search_video(token: Annotated[str, Depends(oauth2_scheme)], title: str, db: Session = Depends(get_db)):
    auth = decode_token(token)
    if not auth:
        raise HTTPException(status_code=401, detail="Not authorized")
    db_video = crud.get_video_by_title(db=db, title=title)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video



add_pagination(app)