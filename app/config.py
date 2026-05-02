from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    SUPABASE_DB_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
