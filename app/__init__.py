import traceback

# sometimes we pull version info before dispatch is totally installed
try:
    from app.category.models import Category  # noqa lgtm[py/unused-import]
    from app.category.models import CategoryKeyword  # noqa lgtm[py/unused-import]
    from app.naver_clova_ocr.models import NaverClovaOCR  # noqa lgtm[py/unused-import]
    from app.ocr.models import GeneralOCR  # noqa lgtm[py/unused-import]
    from app.ocr.models import CategoryOCR  # noqa lgtm[py/unused-import]
except Exception:
    traceback.print_exc()
