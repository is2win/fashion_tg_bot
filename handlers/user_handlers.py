from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from keyboards.universal_creater import create_universal_inline_kb
from services.hf_api_mistral import ask_hf_api
from services.groq_api import ask_groq_api
from vector_db.load_vector import retriever
from services.groq_api_as_open_ai import ask_groq_api_openai
from lexicon.lexicon import LEXICON_HANDLERS_PROMPTS, LEXICON_HANDLERS_CONTEXT
from loguru import logger


router = Router()


# хэндлер для обработки точки входа "/start"
@router.message(CommandStart())
async def process_start_command(message: Message):
    # Логируем сообщение
    logger.info(message)
    context = LEXICON_HANDLERS_CONTEXT["Приветствие для xclusive барбер шопа"]
    # Логирую контекст
    logger.info(context)
    prompt = LEXICON_HANDLERS_PROMPTS["Приветствие для xclusive барбер шопа"]
    text = ask_groq_api_openai(prompt, context)
    # Логирую ответ
    logger.info(text)
    await message.answer(
        text=text,
        reply_markup=create_universal_inline_kb(
            1,
            'hair_cut_variants',
        )
    )


# @router.callback_query(F.data == 'say_your_name')
# async def process_say_bot_name(callback: CallbackQuery):
#     context = LEXICON_HANDLERS_CONTEXT["Приветствие для xclusive барбер шопа"]
#     prompt = LEXICON_HANDLERS_PROMPTS["Приветствие для xclusive барбер шопа"]
#
#     text = ask_groq_api_openai(prompt, context)
#     await callback.message.edit_text(
#         text=text,
#     )

@router.callback_query(F.data == 'hair_cut_variants')
async def process_hair_cut_variants(callback: CallbackQuery):
    # Логирую коллбэк
    logger.info(callback)
    context_ret = retriever.get_relevant_documents(
        LEXICON_HANDLERS_CONTEXT['Предложи несколько вариантов стрижек']
    )
    context = [text.page_content for text in context_ret]
    # Логирую контекст
    logger.info(context)
    prompt = LEXICON_HANDLERS_PROMPTS['Предложи несколько вариантов стрижек']
    text = ask_groq_api_openai(prompt, context)
    # Логирую ответ
    logger.info(text)
    await callback.message.answer(
        text=text,
    )

@router.message()
async def answer_rag(message: Message):
    # Логирую сообщение
    logger.info(message)
    context_ret = retriever.get_relevant_documents(message.text)
    context = [text.page_content for text in context_ret]
    # Логирую контекст
    logger.info(context)
    prompt = message.text
    text = ask_groq_api_openai(prompt, context)
    # Логирую ответ
    logger.info(text)
    await message.answer(text)