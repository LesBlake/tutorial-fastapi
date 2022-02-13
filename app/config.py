from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str
    secret_key: str
    algorithm: str
    access_token_ttl: int


settings = Settings()
