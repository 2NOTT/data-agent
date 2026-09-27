# 定义yaml文件的路径
from dataclasses import dataclass
import os
from pathlib import Path

from omegaconf import OmegaConf

#===================日志配置===================
# 定义日志配置的模型
@dataclass
class File:
    enable: bool
    level: str
    path: str
    rotation: str
    retention: str

@dataclass
class Console:
    enable: bool
    level: str

@dataclass
class LoggingConfig:
    file: File
    console: Console

# ==================== database配置模型 ====================

@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

# ==================== Qdrant 配置模型 ====================

@dataclass
class QdrantConfig:
    host: str
    port: int
    embedding_size: int


# ==================== Embedding 配置模型 ====================

@dataclass
class EmbeddingConfig:
    host: str
    port: int
    model: str


# ==================== ES 配置模型 ====================

@dataclass
class ESConfig:
    host: str
    port: int
    index_name: str


# ==================== LLM 配置模型 ====================

@dataclass
class LLMConfig:
    provider: str
    model_name: str
    api_key: str
    base_url: str


# ==================== 应用总配置模型 ====================

@dataclass
class AppConfig:
    logging: LoggingConfig
    db_meta: DBConfig
    db_dw: DBConfig
    qdrant: QdrantConfig
    embedding: EmbeddingConfig
    es: ESConfig
    llm: LLMConfig



yaml_path = Path(__file__).resolve().parents[2] / "conf" / "app_config.yaml"

# 加载yaml文件
yaml_data = OmegaConf.load(yaml_path)

#将_yaml_data转换为指定类型AppConfig的对象
app_config : AppConfig=OmegaConf.to_object(OmegaConf.merge(AppConfig, yaml_data))

# Prefer explicit generic settings, then provider-specific environment
# variables. This keeps the same config file usable with DeepSeek or an
# OpenAI-compatible provider such as SiliconFlow.
siliconflow_key = os.getenv("SILICONFLOW_API_KEY", "")
generic_key = os.getenv("API_KEY", "")
generic_base_url = os.getenv("BASE_URL", "")
generic_model = os.getenv("MODEL", "")

if os.getenv("LLM_API_KEY"):
    app_config.llm.api_key = os.environ["LLM_API_KEY"]
elif siliconflow_key:
    app_config.llm.api_key = siliconflow_key
    app_config.llm.provider = os.getenv("LLM_PROVIDER", "siliconflow")
    app_config.llm.model_name = os.getenv("SILICONFLOW_MODEL", "deepseek-ai/DeepSeek-V3")
    app_config.llm.base_url = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
elif generic_key:
    # Support the common API_KEY / BASE_URL / MODEL naming used by local
    # environment managers and OpenAI-compatible providers such as SiliconFlow.
    app_config.llm.api_key = generic_key
    app_config.llm.provider = os.getenv("LLM_PROVIDER", "openai-compatible")
    app_config.llm.model_name = generic_model or "deepseek-ai/DeepSeek-V3"
    app_config.llm.base_url = generic_base_url or "https://api.siliconflow.cn/v1"
elif os.getenv("DEEPSEEK_API_KEY"):
    app_config.llm.api_key = os.environ["DEEPSEEK_API_KEY"]



if __name__ == "__main__":
    print(app_config, type(app_config))
    print(app_config.logging.file.path)
