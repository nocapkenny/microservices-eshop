import pytest
from django.db import connections
from django.db.utils import OperationalError

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Включает доступ к БД для всех тестов
    """
    pass