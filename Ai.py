# Ai.py

from langchain_community.chat_models import GigaChat
from config import GigaChatKey
import asyncio
from langchain.schema import SystemMessage, HumanMessage


class AI:
    def __init__(self):

        self.llm = GigaChat(
            model="GigaChat",
            credentials=GigaChatKey,   # Ваш закодированный ключ base64(client_id:client_secret)
            scope="GIGACHAT_API_PERS", # Требуемый scope
            verify_ssl_certs=False,    # Отключаем проверку SSL (для теста)
            streaming=False,           # Если не хотим стриминговой выдачи
            temperature=0.5            # Креативность (0...1+)
        )

    async def chat(self, user_message: str) -> str:

        system_msg = SystemMessage(content=(
            "Вы — специалист по йоге. "
            "Вы отвечаете только на вопросы, связанные с йогой, асанами, дыхательными техниками, "
            "медитацией и фитнес-аспектом йоги. "
            "На каждый вопрос по теме йога отвечай развёрнуто и не задавай вопросы"
            "Если вопрос не связан с йогой, ответьте коротко, что вы можете отвечать только по теме йоги."
            "Не надо спрашивать 'Могу ли я помочь вам с другим вопросом?'"
        ))
        user_msg = HumanMessage(content=user_message)
        messages = [system_msg, user_msg]

        # Вызываем LLM.invoke(...) в отдельном потоке, чтобы не блокировать asyncio
        response = await asyncio.to_thread(self.llm.invoke, messages)
        return response.content
