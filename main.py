# # from db import save

# # # save()
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db, ScrapedPage, Link, Image
from web_scraper import scrape_website
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html file
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

class LinkModel(BaseModel):
    url: str
    text: str

class ImageModel(BaseModel):
    src: str
    alt: str

class PageRequest(BaseModel):
    url: str

class PageResponse(BaseModel):
    url: str
    content: str
    links: List[LinkModel]
    images: List[ImageModel]

@app.post("/scrape/", response_model=PageResponse)
def scrape_page(page: PageRequest, db: Session = Depends(get_db)):
    # Check if the page is already in the database
    db_page = db.query(ScrapedPage).filter(ScrapedPage.url == page.url).first()
    if db_page:
        return PageResponse(
            url=db_page.url, 
            content=db_page.content,
            links=[LinkModel(url=link.url, text=link.text) for link in db_page.links],
            images=[ImageModel(src=image.src, alt=image.alt) for image in db_page.images]
        )

    # If not, scrape the page
    scraped_data = scrape_website(page.url)
    if not scraped_data:
        raise HTTPException(status_code=400, detail="Failed to scrape the page")

    # Save to database
    new_page = ScrapedPage(url=page.url, content=scraped_data["content"])
    db.add(new_page)
    db.flush()  # This assigns an id to new_page

    for link_data in scraped_data["links"]:
        new_link = Link(url=link_data["url"], text=link_data["text"], page_id=new_page.id)
        db.add(new_link)

    for image_data in scraped_data["images"]:
        new_image = Image(src=image_data["src"], alt=image_data["alt"], page_id=new_page.id)
        db.add(new_image)

    db.commit()
    db.refresh(new_page)

    return PageResponse(
        url=new_page.url, 
        content=new_page.content,
        links=[LinkModel(url=link.url, text=link.text) for link in new_page.links],
        images=[ImageModel(src=image.src, alt=image.alt) for image in new_page.images]
    )

@app.get("/pages/", response_model=List[PageResponse])
def get_pages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pages = db.query(ScrapedPage).offset(skip).limit(limit).all()
    return [
        PageResponse(
            url=page.url, 
            content=page.content,
            links=[LinkModel(url=link.url, text=link.text) for link in page.links],
            images=[ImageModel(src=image.src, alt=image.alt) for image in page.images]
        ) for page in pages
    ]

@app.get("/pages/{page_id}", response_model=PageResponse)
def get_page(page_id: int, db: Session = Depends(get_db)):
    page = db.query(ScrapedPage).filter(ScrapedPage.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    return PageResponse(
        url=page.url, 
        content=page.content,
        links=[LinkModel(url=link.url, text=link.text) for link in page.links],
        images=[ImageModel(src=image.src, alt=image.alt) for image in page.images]
    )