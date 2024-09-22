from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Если у вас нет видеокарты, укажите 'device': 'cpu'
hf_embeddings_model = HuggingFaceEmbeddings(
    model_name="cointegrated/LaBSE-en-ru", model_kwargs={"device": "cpu"}
)

db = FAISS.load_local(
    "./vector_db/db_files/some_articles_about_barber",
    hf_embeddings_model,
    allow_dangerous_deserialization=True
)

# Самый частый кейс - использование векторного хранилища и его методов для получения документов
retriever = db.as_retriever(
    search_type="similarity",  # тип поиска похожих документов
    k=10,  # количество возвращаемых документов (Default: 4)
    score_threshold=0.8,  # минимальный порог для поиска "similarity_score_threshold"
)