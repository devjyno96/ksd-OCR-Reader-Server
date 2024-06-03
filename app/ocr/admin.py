from sqladmin import ModelView

from app.ocr.models import CategoryOCR, GeneralOCR


class GeneralOCRAdmin(ModelView, model=GeneralOCR):
    column_list = [GeneralOCR.id, GeneralOCR.ocr_api_url, GeneralOCR.ocr_api_key]


class CategoryOCRAdmin(ModelView, model=CategoryOCR):
    column_list = [
        CategoryOCR.id,
        CategoryOCR.category_id,
        "category.name",
        CategoryOCR.ocr_api_url,
        CategoryOCR.ocr_api_key,
    ]

    from_ajax_refs = {
        "category": {
            "fields": ("id", "name", "description"),
            "order_by": ("name"),
        },
    }
