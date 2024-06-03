from sqladmin import ModelView

from app.category.models import Category, CategoryKeyword


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.description]


class CategoryKeywordAdmin(ModelView, model=CategoryKeyword):
    column_list = [CategoryKeyword.id, CategoryKeyword.category_id, "category.name", CategoryKeyword.keyword]

    column_details_list = [CategoryKeyword.id, CategoryKeyword.category_id, "category.name", CategoryKeyword.keyword]
    column_labels = {
        CategoryKeyword.id: "ID",
        CategoryKeyword.category_id: "Category ID",
        "category.name": "Category Name",
        CategoryKeyword.keyword: "keyword",
    }

    form_columns = [
        CategoryKeyword.category,
        CategoryKeyword.keyword,
    ]
    from_ajax_refs = {
        "category": {
            "fields": ("id", "name", "description"),
            "order_by": ("id"),
        },
    }
