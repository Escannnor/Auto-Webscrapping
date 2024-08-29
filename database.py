# from sqlalchemy import create_engine, Column, Integer, String, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./scrape_data.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# class ScrapedPage(Base):
#     __tablename__ = "scraped_pages"

#     id = Column(Integer, primary_key=True, index=True)
#     url = Column(String, unique=True, index=True)
#     content = Column(Text)
#     analysis = Column(Text)

# Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./scrape_data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ScrapedPage(Base):
    __tablename__ = "scraped_pages"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    content = Column(Text)
    links = relationship("Link", back_populates="page")
    images = relationship("Image", back_populates="page")

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    text = Column(String)
    page_id = Column(Integer, ForeignKey("scraped_pages.id"))
    page = relationship("ScrapedPage", back_populates="links")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    src = Column(String)
    alt = Column(String)
    page_id = Column(Integer, ForeignKey("scraped_pages.id"))
    page = relationship("ScrapedPage", back_populates="images")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()