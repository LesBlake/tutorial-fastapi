from pydantic import BaseSettings


class Settings(BaseSettings):
    fastapi_db_url: str
    fastapi_db_port: str
    fastapi_db_user: str
    fastapi_db_password: str
    fastapi_db_name: str
    fastapi_secret_key: str
    fastapi_access_token_algorithm: str
    fastapi_access_token_ttl: int

    class Config:
        env_file = ".env"


settings = Settings()
