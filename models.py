from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, server_default='TRUE')
    rating = Column(Integer, nullable=True)
    # Класс статьи

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    name = Column(String, nullable=False)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    text = Column(String, nullable=False)
