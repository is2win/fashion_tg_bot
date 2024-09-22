from groq import Groq
from config_data.config import CONFIG


client = Groq(api_key=CONFIG.tg_bot.groq_token)


def ask_groq_api(text_for_api: str, context: str | None = None):
    text_for_api = f""" <|start_header_id|>system<|end_header_id|>
        Ты выступаешь в роли эксперта барбершопа 'Xclusive'.
        Ты используешь для ответа только РУССКИЙ язык, остальное ты не пишешь. 
        Ты используешь emoji для ответа, чтобы текст был красиво оформлен.
        Ты пишешь структурированный ответ по пунктам. 
        Ты можешь отвечать только на текст, который приходит внутри контекста который указан как "контекст". 
        Если информации  в контексте для ответа недостаточно - ты пишешь такую фразу: 
        "Извините, я не могу на такое ответить" и более ничего не пишешь.
        Только если пользователь захочет записаться к барберу на прием - 
        пришли ему ссылку смайлами: http://xclusive-barber.ru иначе не предлагай контакт.
        Отвечай на вопрос ниже!
        Будь креативным
        <|eot_id|>
        <|start_header_id|>контекст<|end_header_id|>
        Контекст:  {context}
        <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        Вопрос: {text_for_api}
        <|eom_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """
    # model = "llama-3.1-70b-versatile"
    # model = "llama-3.1-8b-instant"
    model = "llama3-groq-70b-8192-tool-use-preview"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text_for_api,
            }
        ],
        max_tokens=500,
        model=model,
    )

    return chat_completion.choices[0].message.content