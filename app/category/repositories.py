from sqlalchemy.orm import Session

from app.category.models import Category
from app.category.schemas import CategoryCreate, CategoryUpdate
from app.repositories import BaseRepository


class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def get_by_name(self, db_session: Session, name: str) -> Category | None:
        return db_session.query(Category).filter(Category.name == name).first()


category_repository = CategoryRepository(Category)
