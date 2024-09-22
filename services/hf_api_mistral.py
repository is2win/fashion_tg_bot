from huggingface_hub import InferenceClient
from config_data.config import CONFIG


def ask_hf_api(text_for_api: str, context: str | None = None):
    client = InferenceClient(
        # "mistralai/Mistral-Nemo-Instruct-2407",
        # "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "mistralai/Mistral-7B-Instruct-v0.3",
        token=CONFIG.tg_bot.hf_token
    )
    text_for_api = f""" Ты выступаешь в роли эксперта барбершопа \<\<X'clusive\>\>.
    Ты используешь для ответа только РУССКИЙ язык. 
    Ты используешь emoji для ответа, чтобы текст был красиво оформлен.
    Ты структурируешь ответ по пунктам. 
    Ты используешь HTML разметки для формирования ответов. 
    Ты можешь отвечать только на текст, который приходит внутри контекста 
    который указан внутри ### ###. 
    Если информации  в контексте для ответа недостаточно - ты пишешь такую фразу: 
    "Извините, я не могу на такое ответить" и более ничего не пишешь.
    Отвечай на вопрос ниже
    ### 
    Контекст:  {context}
    ###
    Вопрос: {text_for_api}

    """
    answer = []
    try:
        for message in client.chat_completion(
            messages=[{"role": "user", "content": text_for_api}],
            max_tokens=1000,
            stream=True,
        ):
            answer.append(message.choices[0].delta.content)
    except:
        pass

    text_answer = ''.join(answer)
    print(text_answer)
    return text_answer
