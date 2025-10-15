from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tourist Safety AI System"
    API_V1_STR: str = "/v1"

    # Server settings
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    # Database settings
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_SERVER: str = "db"
    POSTGRES_DB: str = "tourist_safety"
    DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

    # External API Keys
    GOOGLE_MAPS_API_KEY: str = "YOUR_GOOGLE_MAPS_API_KEY"
    NEWSDATA_API_KEY: str = "YOUR_NEWSDATA_API_KEY"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
