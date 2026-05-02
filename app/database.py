from langchain_community.utilities import SQLDatabase
from .config import settings

_db: SQLDatabase | None = None


def get_db() -> SQLDatabase:
    global _db
    if _db is None:
        _db = SQLDatabase.from_uri(settings.SUPABASE_DB_URL)
    return _db


def get_schema() -> str:
    return get_db().get_table_info()
