import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.category.models import Category, CategoryKeyword
from app.ocr.models import CategoryOCR, GeneralOCR
from tests.database import TestingSession


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = TestingSession
        sqlalchemy_session_persistence = "commit"


class CategoryFactory(BaseFactory):
    class Meta:
        model = Category

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    description = factory.Faker("sentence")


class CategoryKeywordFactory(BaseFactory):
    class Meta:
        model = CategoryKeyword

    id = factory.Sequence(lambda n: n)
    category = factory.SubFactory(CategoryFactory)
    keyword = factory.Faker("word")


class GeneralOCRFactory(BaseFactory):
    class Meta:
        model = GeneralOCR

    id = factory.Sequence(lambda n: n)
    ocr_api_url = factory.Faker("url")
    ocr_api_key = factory.Faker("uuid4")


class CategoryOCRFactory(BaseFactory):
    class Meta:
        model = CategoryOCR

    id = factory.Sequence(lambda n: n)
    ocr_api_url = factory.Faker("url")
    ocr_api_key = factory.Faker("uuid4")
    category = factory.SubFactory(CategoryFactory)
