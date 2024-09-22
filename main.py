import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config, CONFIG
from keyboards.main_menu import set_main_menu
from handlers import user_handlers

# Инициализация логгера
logger = logging.getLogger(__name__)


# Асинхронная функция запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    # config: Config = load_config()

    # Инициализация бота и диспетчера
    bot = Bot(
        token=CONFIG.tg_bot.token,
        # default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
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