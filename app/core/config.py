from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    
    GEMINI_MODEL: str = "gemini-2.5-flash"
    LEETCODE_GRAPHQL: str = "https://leetcode.com/graphql"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()