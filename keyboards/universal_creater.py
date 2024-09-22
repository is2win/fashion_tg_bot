from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


# Функция генерации клавиатуры на лету
def create_universal_inline_kb(
        width: int,
        *args: str,
        **kwargs: str) -> InlineKeyboardMarkup:

    # Инициалиазция билдера
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопок из аргов и кваргов
    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=LEXICON[button] if button in LEXICON else button,
                    callback_data=button
                )
            )
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=button
                )
            )
    # распаковываем список с кнопками в билдер методом row с параметром width
    kb_builder.row(*buttons, width=width)
    # возвращаем объект клавиатуры
    return kb_builder.as_markup()
