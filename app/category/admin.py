from sqladmin import ModelView

from app.category.models import Category, CategoryKeyword


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.description]


class CategoryKeywordAdmin(ModelView, model=CategoryKeyword):
    column_list = [CategoryKeyword.id, CategoryKeyword.category_id, "category.name", CategoryKeyword.keyword]
