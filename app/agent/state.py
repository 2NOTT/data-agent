from typing import TypedDict

from app.models.es.value_info_es import ValueInfoES
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant
from app.models.qdrant.metric_info_qdrant import MetricInfoQdrant

class MetricInfoState(TypedDict):
    name:str
    description:str
    relevant_columns:list
    alias:list

class ColumnInfoState(TypedDict):
    name: str
    type:str
    role: str
    examples:list
    description:str
    alias: list

class TableInfoState(TypedDict):
    name:str
    role:str
    description:str
    columns: list[ColumnInfoState]

# 自定义State模型
class DataAgentState(TypedDict):
    query: str # 提问
    keywords: list[str] # 提问分词产生的多个关键字
    sql: str # 生成的sql
    error: str # 存储校验SQL产生的错误信息
    recall_columns: list[ColumnInfoQdrant] # 列信息对象列表
    recall_metrics: list[MetricInfoQdrant] # 指标信息对象列表
    recall_values: list[ValueInfoES] # 字段值信息对象列表
    table_infos: list[TableInfoState] # 合并3路召回产生的相关表及其字段信息状态列表
    metric_infos: list[MetricInfoState] # 指标信息状态对象列表