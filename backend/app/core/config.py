from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application settings loaded from environment variables in .env file.
    app_name: str = "Library Management API"
    database_url: str = "mysql+pymysql://user:password@localhost:3306/library_db"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
