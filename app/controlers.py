from litestar.exceptions import HTTPException
from typing import List
from litestar import Controller, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData

from app.dtos import (
    AuthorReadDTO,
    AuthorReadFullDTO,
    AuthorUpdateDTO,
    AuthorWriteDTO,
    BookReadDTO,
    BookWriteDTO,
    BookUpdateDTO,
    CategoryDTO,
)
from app.models import Author, Book
from app.repositories import (
    AuthorRepository,
    BookRepository,
    provide_authors_repo,
    provide_books_repo,
)


class AuthorController(Controller):
    path = "/authors"
    tags = ["authors"]
    return_dto = AuthorReadDTO
    dependencies = {"authors_repo": Provide(provide_authors_repo)}

    @get()
    async def list_authors(self, authors_repo: AuthorRepository) -> List[Author]:
        return authors_repo.list()

    @post(dto=AuthorWriteDTO)
    async def create_author(self, data: Author, authors_repo: AuthorRepository) -> Author:
        return authors_repo.add(data)

    @get("/{author_id:int}", return_dto=AuthorReadFullDTO)
    async def get_author(self, author_id: int, authors_repo: AuthorRepository) -> Author:
        try:
            return authors_repo.get(author_id)
        except:
            raise HTTPException(f"El autor no existe", status_code=404)

    @patch("/{author_id:int}", dto=AuthorUpdateDTO)
    async def update_author(
        self, author_id: int, data: DTOData[Author], authors_repo: AuthorRepository
    ) -> Author:
        try: 
            author = authors_repo.get(author_id)
            author = data.update_instance(author)
            return authors_repo.update(author)
        except:
            raise HTTPException(f"El autor no existe", status_code=404)

class BookController(Controller):
    path = "/books"
    tags = ["books"]
    return_dto = BookReadDTO
    dependencies = {"books_repo": Provide(provide_books_repo)}

    @get()
    async def list_books(self, books_repo: BookRepository) -> List[Book]:
        return books_repo.list()

    @post(dto=BookWriteDTO)
    async def create_book(self, data: Book, books_repo: BookRepository) -> Book:
        return books_repo.add(data)

    @get("/{book_id:int}", return_dto=BookReadDTO)
    async def get_book(self, book_id: int, books_repo: BookRepository) -> Book:
        try:
            return books_repo.get(book_id)
        except:
            raise HTTPException(f"El libro no existe", status_code=404)

    @patch("/{book_id:int}", dto=BookUpdateDTO)
    async def update_book(self, book_id: int, data: DTOData[Book], books_repo: BookRepository) -> Book:
        try:
            book = books_repo.get(book_id)
            book = data.update_instance(book)
            return books_repo.update(book)
        except:
            raise HTTPException(f"El libro no existe", status_code=404)