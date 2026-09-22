import asyncio
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings
from qdrant_client import AsyncQdrantClient
from app.conf.app_config import EmbeddingConfig, app_config


class EmbeddingClientManager:
    """
    进行向量存储和搜索的qdrant的客户端管理器
    """

    def __init__(self, config: EmbeddingConfig):
        self.config = config
        self.client: Optional[AsyncQdrantClient] = None

    def _get_url(self):
        return f"http://{self.config.host}:{self.config.port}"

    def init(self):
        self.client = HuggingFaceEndpointEmbeddings(model=self._get_url())



# 创建客户端管理器
embedding_client_manager = EmbeddingClientManager(app_config.embedding)

if __name__ == "__main__":
    async def test():
        embedding_client_manager.init()

        #对指定文本进行向量化
        text="hello"
        query_result=embedding_client_manager.client.embed_query(text)
        print(query_result)#包含1024个点数据的数组
        print(len(query_result))

    asyncio.run(test())
