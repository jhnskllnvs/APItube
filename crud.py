from sqlalchemy.orm import Session
import models, schemas

def get_all_videos(db: Session, skip: int = 0):
    return db.query(models.Video).offset(skip).all()

def get_free_videos(db: Session, skip: int = 0):
    return db.query(models.Video).offset(skip).all()

def get_video(db: Session, id: int):
    return db.query(models.Video).filter(models.Video.id == id).first()
 
def add_video(db: Session,  video: schemas.videosCreate) -> models.Video:
    db_video = models.Video(title = video.title, desc_video = video.desc_video, url = video.url, category_id = video.category_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def get_video_by_title(db: Session, title: str):
    return db.query(models.Video).filter(models.Video.title == title).first()

def update_video(db: Session, video: models.Video, update: schemas.videosUpdate) -> models.Video:
        update.model_dump(exclude_unset=True)
        for key, value in update:
                setattr(video, key, value)
        db.merge(video)
        db.commit()
        db.refresh(video)
        return video

def delete_video(db: Session, db_video: models.Video):
     db.delete(db_video)
     db.commit()
     status = {"Status": "Deleted"}
     return status

def read_categories(db: Session, skip: int = 0):
     return db.query(models.Category).offset(skip).all()

def read_category(db: Session, id: int):
    return db.query(models.Category).filter(models.Category.id == id).first()

def add_category(db: Session,  category: schemas.categoryCreate):
    db_category = models.Category(title=category.title, color=category.color)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, db_category: models.Category):
     db.delete(db_category)
     db.commit()
     status = {"Status": "Deleted"}
     return status

def update_category(db: Session, category: models.Category, update: schemas.categoryUpdate) -> models.Category:
        update.model_dump()
        for key, value in update:
            if value is None:
                pass
            else:
                setattr(category, key, value)
        db.merge(category)
        db.commit()
        db.refresh(category)
        return category

def get_videos_by_category(db: Session, category: models.Category):
     return db.query(models.Video).filter(category.id == models.Video.category_id).all()

def get_category_by_name(db: Session, title: str):
     return db.query(models.Category).filter(models.Category.title == title).first()
     
def get_user_token(token: str):
     return schemas.userTokenCreator(username = token + "notdecoded")

def get_user_from_name(db: Session, username: str):
    return db.query(models.user).filter(models.user.username == username).first()

def check_user_psswd(db: Session, user_password: str):
     return db.query(models.user).filter(models.user.user_password == user_password).first()

def create_user(db: Session, user: schemas.userCreate):
    db_user = models.user(username=user.username, user_password = user.user_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"Status": "User has been created"}
    
def delete_user(db: Session, user: schemas.UserBase):
    db.delete(user)
    db.commit()
    return {"Status": "User has been deleted"}



