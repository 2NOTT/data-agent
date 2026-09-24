from typing import TypedDict

# 自定义State模型
class DataAgentState(TypedDict):
    query: str # 提问
    keywords: list[str] # 提问分词产生的多个关键字
    sql: str # 生成的sql
    error: str # 存储校验SQL产生的错误信息