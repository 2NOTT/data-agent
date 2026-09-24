import uuid

from aiohttp import payload
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.conf.meta_config import MetaConfig, TableConfig, MetricConfig
from app.core.log import logger
from app.models.mysql.column_info_mysql import ColumnInfoMySQL
from app.models.mysql.metric_info_mysql import MetricInfoMySQL
from app.models.mysql.table_info_mysql import TableInfoMySQL
from app.models.qdrant.column_info_qdrant import ColumnInfoQdrant
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
                 embedding_client: HuggingFaceEndpointEmbeddings):
        self.dw_mysql_repo = dw_mysql_repo
        self.meta_mysql_repo = meta_mysql_repo
        self.value_es_repo = value_es_repo
        self.column_qdrant_repo = column_qdrant_repo
        self.metric_qdrant_repo = metric_qdrant_repo
        self.embedding_client = embedding_client

    """
    # 1. 处理表相关的信息
    # 1.1 将表的信息和字段的信息保存到meta库（tableinfo和column_info表）
    # 1.2 对所有字段信息建立向量索引
    # 1.3 对象字段取值建立全文索引
    # 2. 处理指标信息
    # 2.1 将指标信息数据保存到meta库（metric_info和culumn_metric表）
    # 2.2 对指标信息建立向量索引
    """
    async def build(self, config: MetaConfig):
        logger.info("开始构建业务")
        # 1. 处理表相关的信息
        if config.tables:
            # 1.1 将表的信息和字段的信息保存到meta库（tableinfo和column_info表）
            column_infos:list[ColumnInfoMySQL] = await self._save_table_infos_to_meta_db(config.tables)
            logger.info("保存表信息和字段信息到meta库成功")

            # 1.2 对所有字段信息建立向量索引
            await self._save_column_infos_to_qdrant(column_infos)
            logger.info("保存字段信息到qdrant向量库成功")

            # 1.3 对象字段取值建立全文索引
            await self._save_column_values_to_es(column_infos, config.tables)
            logger.info("保存字段取值到es全文索引库成功")
        # 2. 处理指标信息
        if config.metrics:
            # 2.1 将指标信息数据保存到meta库（metric_info和culumn_metric表）
            metric_infos: list[MetricInfoMySQL] = await self._save_metric_infos_to_meta_db(config.metrics)
            logger.info("保存指标信息到meta库成功")

            # 2.2 对指标信息建立向量索引
            await self._save_metric_infos_to_qdrant(metric_infos)
            logger.info("保存指标信息到qdrant向量库成功")

    """
    遍历tables中所有表的信息数据，封装成表信息对象的数组table_infos  调用持久层保存到table_info表
    遍历所有表中字段的信息数据，封装成字段信息对象的数组column_infos  调用持久层保存到column_info表
    """
    async def _save_table_infos_to_meta_db(self, tables: list[TableConfig])->list[ColumnInfoMySQL]:
        """将表的信息和字段的信息保存到meta库（tableinfo和column_info表）"""
        # 准备容器
        table_infos: list[TableInfoMySQL] = []
        column_infos:list[ColumnInfoMySQL] = []
        # 遍历, 创建对象，添加到列表
        for table in tables:
            table_info = TableInfoMySQL(
                id=table.name,
                name=table.name,
                role=table.role,
                description=table.description
            )
            table_infos.append(table_info)
            # 查询dw中指定表的所有字段类型 dict[字段名:字段类型]
            column_type_dict: dict[str,str] = await self.dw_mysql_repo.get_column_types(table_info.name)

            # 遍历字段信息, 创建ORM对象
            for column in table.columns:
                # 查询dw库，取出指定字段的前10条数据
                examples: list = await self.dw_mysql_repo.get_column_values(table_info.name, column.name)

                column_info = ColumnInfoMySQL(
                    id=f"{table.name}.{column.name}",
                    name=column.name,
                    type=column_type_dict[column.name],  # 需要检查表中字段类型
                    role=column.role,
                    examples=examples, # 需要查表
                    description=column.description,
                    alias=column.alias,
                    table_id=table_info.id
                )
                column_infos.append(column_info)

        # 保存到数据库
        await self.meta_mysql_repo.save_table_infos(table_infos)
        await self.meta_mysql_repo.save_column_infos(column_infos)
        # 返回column_infos
        return column_infos

    """
    遍历每个column_info,对其name,description,alias中每个alia生成向量
    为每个向量生成对应的id和payload(是包含所有column_info中所有数据的字典对象)
    调用持久层保存到向量库
    """
    async def _save_column_infos_to_qdrant(self, column_infos: list[ColumnInfoMySQL]):
        # 准备一个数组容器，存储一个字典对象（id, payload, 待向量化文本）
        data_dict_list: list[dict] = []
        # 遍历column_infos，创建一个字典对象，指定相应的属性，添加到数组中
        for column_info in column_infos:
            column_info_qdrant = ColumnInfoQdrant(
                id=column_info.id,
                name=column_info.name,
                type=column_info.type,
                role=column_info.role,
                examples=column_info.examples,
                description=column_info.description,
                alias=column_info.alias,
                table_id=column_info.table_id
            )
            # name
            data_dict_list.append({
                "id": uuid.uuid4(),
                "embedding_text": column_info.name,
                "payload": column_info_qdrant
            })
            # description
            data_dict_list.append({
                "id": uuid.uuid4(),
                "embedding_text": column_info.description,
                "payload": column_info_qdrant
            })
            # alias
            for alia in column_info.alias:
                data_dict_list.append({
                    "id": uuid.uuid4(),
                    "embedding_text": alia,
                    "payload": column_info_qdrant
                })

        # 取出所有待向量化的文本对其进行批量向量化（需要分处理），得到包含所有向量列表： vectors: list[list[float]]
        embeddint_texts = [data_dict["embedding_text"] for data_dict in data_dict_list]
        batch_size = 32
        vectors: list[list[float]] = []
        for i in range(0, len(embeddint_texts), batch_size):
            batch_embeddint_texts = embeddint_texts[i:i+batch_size]
            batch_vectors: list[list[float]] = await self.embedding_client.aembed_documents(batch_embeddint_texts)
            # vectors.append(batch_vectors)  # 不可以，多了一层嵌套
            vectors.extend(batch_vectors)

        # 从上面的数组容器中取出所有id组成数组：ids: list[str]
        ids: list[str] = [data_dict["id"] for data_dict in data_dict_list]

        # 从上面的数组容器中取出所有payload组成数组：payloads: list[dict]
        payloads: list[dict] = [data_dict["payload"] for data_dict in data_dict_list]

        # 调用持久层保存到向量库
        await self.column_qdrant_repo.upsert_column_vectors(vectors, payloads, ids)


    async def _save_column_values_to_es(self, column_infos: list[ColumnInfoMySQL], tables: list[TableConfig]):
        """对象字段取值建立全文索引"""
        pass

    async def _save_metric_infos_to_meta_db(self, metrics: list[MetricConfig])->list[MetricInfoMySQL]:
        """将指标信息数据保存到meta库（metric_info和culumn_metric表）"""
        pass

    async def _save_metric_infos_to_qdrant(self, metric_infos:list[MetricInfoMySQL]):
        """对指标信息建立向量索引"""
        pass
