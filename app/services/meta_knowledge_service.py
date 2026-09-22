from app.core.log import logger
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.conf.meta_config import MetaConfig, TableConfig, MetricConfig
from app.models.mysql.column_info_mysql import ColumnInfoMySQL
from app.models.mysql.metric_info_mysql import MetricInfoMySQL
from app.repositories.es.value_es_repository import ValueESRepository
from app.repositories.mysql.dw_mysql_repository import DWMysqlRepository
from app.repositories.mysql.meta_mysql_repository import MetaMysqlRepository
from app.repositories.qdrant.column_qdrant_repository import ColumnQdrantRepository
from app.repositories.qdrant.metric_qdrant_repository import MetricQdrantRepository





class MetaKnowledgeService:
    def __init__(self,
                 dw_mysql_repo: DWMysqlRepository,
                 meta_mysql_repo: MetaMysqlRepository,
                 value_es_repo: ValueESRepository,
                 column_qdrant_repo: ColumnQdrantRepository,
                 metric_qdrant_repo: MetricQdrantRepository,
                 embedding_repo: HuggingFaceEndpointEmbeddings,
                 ):
        self.dw_mysql_repo = dw_mysql_repo
        self.meta_mysql_repo = meta_mysql_repo
        self.value_es_repo = value_es_repo
        self.column_qdrant_repo = column_qdrant_repo
        self.metric_qdrant_repo = metric_qdrant_repo
        self.embedding_repo = embedding_repo


    """
    # 1.处理表相关的信息
    # 1.1将表的信息和字段的信息保存到meta库（tableinfo和column_info表）
    # 1.2对所有字段信息建立向量索引
    # 1.3对象字段取值建立全文索引
    # 2.处理指标信息
    # 2.1将指标信息数据保存到meta库（metric_inf和column_metric表）
    # 2.2将指标信息建立向量索引
    """
    async def build(self,config:MetaConfig):
        logger.info("开始构建业务")
        # 1.处理表相关的信息
        if config.tables:

            # 1.1将表的信息和字段的信息保存到meta库（tableinfo和column_info表）
            column_infos : list[ColumnInfoMySQL] = await self._save_table_infos_to_meta_db(config.tables)
            logger.info("保存表信息和字段信息到meta库成功")

            # 1.2对所有字段信息建立向量索引
            await self._save_column_infos_to_qdrant(column_infos)
            logger.info("保存字段信息到qdrant向量库成功")
            # 1.3对象字段取值建立全文索引
            await self._save_column_values_to_es(column_infos,config.tables)
            logger.info("保存字段取值到es全文索引库成功")

        # 2.处理指标信息
        if config.metrics:

            # 2.1将指标信息数据保存到meta库（metric_inf和column_metric表）
            metric_infos: list[MetricInfoMySQL] = await self._save_metric_infos_to_meta_db(config.metrics)
            logger.info("保存指标信息到meta库成功")

            # 2.2将指标信息建立向量索引
            await self._save_metric_infos_to_qdrant(metric_infos)
            logger.info("保存指标信息到qdrant向量库成功")

    async def _save_table_infos_to_meta_db(self, tables:list[TableConfig]) -> list[ColumnInfoMySQL]:
        """将表的信息和字段的信息保存到meta库（tableinfo和column_info表）"""
        pass

    async def _save_column_infos_to_qdrant(self, column_infos:list[ColumnInfoMySQL]):
        """对所有字段建立向量索引库"""
        pass

    async def _save_column_values_to_es(self, column_infos:list[ColumnInfoMySQL], tables:list[TableConfig]):
        """对象字段取值建立全文索引"""
        pass

    async def _save_metric_infos_to_meta_db(self, metrics:list[MetricConfig]) -> list[MetricInfoMySQL]:
        """将指标信息数据保存到meta库（metric_inf和column_metric表）"""
        pass

    async def _save_metric_infos_to_qdrant(self, metric_infos:list[MetricInfoMySQL]):
        """将指标信息建立向量索引"""
        pass




