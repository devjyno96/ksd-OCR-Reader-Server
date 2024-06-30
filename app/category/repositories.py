from sqlalchemy.orm import Session

from app.category.models import Category, CategoryKeyword
from app.category.schemas import CategoryCreate, CategoryKeywordCreate, CategoryKeywordUpdate, CategoryUpdate
from app.repositories import BaseRepository


class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    def get_by_name(self, db_session: Session, name: str) -> Category | None:
        return db_session.query(Category).filter(Category.name == name).first()


class CategoryKeywordRepository(BaseRepository[CategoryKeyword, CategoryKeywordCreate, CategoryKeywordUpdate]):
    def bulk_remove_by_category(self, db_session: Session, category: Category, is_commit: bool = True):
        db_session.query(CategoryKeyword).filter(CategoryKeyword.category == category).delete()
        if is_commit:
            db_session.commit()

    def bulk_create(self, db_session: Session, category_keywords: list[CategoryKeywordCreate], is_commit: bool = True):
        model_objs = [CategoryKeyword(**category_keyword.model_dump()) for category_keyword in category_keywords]

        db_session.add_all(model_objs)

        if is_commit:
            db_session.commit()

        return model_objs


category_repository = CategoryRepository(Category)
category_keyword_repository = CategoryKeywordRepository(CategoryKeyword)
