from sqlalchemy import Column, Integer, String, ForeignKey
from database import base
from sqlalchemy.orm import relationship, mapped_column


class Category(base):
    __tablename__ = "categories"

    id = mapped_column(Integer, primary_key=True)
    title: str = Column(String(200), nullable=False)
    color: str = Column(String(100), nullable=False)

    video = relationship("Video", back_populates="category")

class Video(base):
    __tablename__ = "videos"
     
    id: int = Column(Integer, primary_key=True)
    category_id = mapped_column(ForeignKey("categories.id"))
    title: str = Column(String(100), nullable=False)
    desc_video: str = Column(String(300), nullable=False)
    url: str = Column(String(300), nullable=False)

    category = relationship("Category", back_populates="video")

class user(base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(40), nullable=False)
    user_password: str = Column(String(30), nullable=False)


