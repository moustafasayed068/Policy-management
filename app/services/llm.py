
import cohere
from app.core.config import settings
from fastapi.concurrency import run_in_threadpool


class LLMService:
    def __init__(self):
        self.client = cohere.ClientV2(settings.COHERE_API_KEY)

    async def chat(self, messages: list, file_url: str | None = None) -> str:
        try:
            if file_url:
                last_message = messages[-1]["content"]
                messages[-1]["content"] = [
                    {"type": "document", "document": {"url": file_url}},
                    {"type": "text", "text": last_message}
                ]

            response = await run_in_threadpool(
                self.client.chat,
                model=settings.LLM_MODEL,
                messages=messages
            )
            return response.message.content[0].text

        except Exception as e:
            raise RuntimeError(f"LLM error: {e}") from e

    async def emb(self, text_inputs: list[str]) -> list[list[float]]:
        response = await run_in_threadpool(
            self.client.embed,
            model=settings.EMB_MODEL,
            texts=text_inputs,
            input_type="classification",
            embedding_types=["float"]
        )
        return response.embeddings.float

        
llm_service = LLMService()