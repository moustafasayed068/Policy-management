# app/services/llm.py

import cohere
from app.core.config import settings
from fastapi.concurrency import run_in_threadpool

COHERE_EMBED_BATCH_SIZE = 96

class LLMService:
    def __init__(self):
        # Initializing Cohere Client V2
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
        """Used for embedding documents during upload."""
        all_embeddings = []
        for i in range(0, len(text_inputs), COHERE_EMBED_BATCH_SIZE):
            batch = text_inputs[i: i + COHERE_EMBED_BATCH_SIZE]
            
            response = await run_in_threadpool(
                self.client.embed,
               
                model=settings.EMB_MODEL, 
                texts=batch,
                input_type="search_document", 
                embedding_types=["float"]
            )
            all_embeddings.extend(response.embeddings.float)
        return all_embeddings

    async def emb_query(self, text: str) -> list[float]:
        """Used for embedding the user's question during chat search."""
        try:
            response = await run_in_threadpool(
                self.client.embed,
               
                model=settings.EMB_MODEL, 
                texts=[text],
                input_type="search_query",
                embedding_types=["float"]
            )
            return response.embeddings.float[0]
        except Exception as e:
            raise RuntimeError(f"Embedding query error: {e}") from e

llm_service = LLMService()