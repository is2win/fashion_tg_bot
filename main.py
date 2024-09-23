import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config, CONFIG
from keyboards.main_menu import set_main_menu
from handlers import user_handlers
from loguru import logger
from pathlib import Path
import logging


# Отключаем стандартный логгер aiogram и заменяем его на loguru
logging.getLogger('aiogram').handlers = [logging.NullHandler()]  # Отключаем стандартный логгер
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Передаем все логи из aiogram в loguru
        level = logger.level(record.levelname).name if logger.level(record.levelname, None) else record.levelno
        logger.log(level, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)

# Асинхронная функция запуска бота
async def main():
    # Инициализация логгера
    log_path = Path(__file__).parent.absolute() / "applogs"
    log_path.mkdir(exist_ok=True)
    log_path = log_path / "main_{time}.log"
    # Конфигурируем логирование
    logger.add(
        log_path,
        rotation="10 MB",
        backtrace=True,
        diagnose=True,
        level="TRACE",
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.success('Starting bot')

    # Загружаем конфиг в переменную config
    # config: Config = load_config()

    # Инициализация бота и диспетчера
    bot = Bot(
        token=CONFIG.tg_bot.token,
        # default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )
    dp = Dispatcher()

    # Настраиваем главное меню
    await set_main_menu(bot)


    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)


    # Пропускаем накопившиеся апдейты и запускаем  pooling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())