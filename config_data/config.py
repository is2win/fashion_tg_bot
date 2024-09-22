from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str # Токен доступа к боту
    hf_token: str # Токен для API HF
    groq_token: str # Токен для API Groq
    proxy_token: str # Токен для proxy


@dataclass
class Config:
    tg_bot: TgBot


# Функция для инициализации бота
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env("BOT_TOKEN"),
            hf_token=env("HF_TOKEN"),
            groq_token=env("GROQ_TOKEN"),
            proxy_token=env("PROXY_TOKEN"),
        )
    )


CONFIG = load_config()
print('загрузка конфига произошла')