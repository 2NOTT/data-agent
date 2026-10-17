from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

from app.conf.app_config import app_config

def _missing_llm(_input):
    raise RuntimeError("未配置 API_KEY、LLM_API_KEY、SILICONFLOW_API_KEY 或 DEEPSEEK_API_KEY，请设置环境变量或项目根目录的 .env")


if app_config.llm.api_key:
    if app_config.llm.provider in {"siliconflow", "openai-compatible", "openai"}:
        llm = ChatOpenAI(
            model=app_config.llm.model_name,
            api_key=app_config.llm.api_key,
            base_url=app_config.llm.base_url or "https://api.siliconflow.cn/v1",
            temperature=0,
        )
    else:
        llm = init_chat_model(
            model=app_config.llm.model_name,
            api_key=app_config.llm.api_key,
            temperature=0,
        )
else:
    # Keep the API importable for health checks and local tests. The first
    # actual query receives a precise configuration error instead.
    llm = RunnableLambda(_missing_llm)

if __name__ == '__main__':
    for chunk in llm.stream("你是什么模型？"):
        print(chunk.text, end="", flush=True)
