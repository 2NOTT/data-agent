from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mysql.table_info_mysql import TableInfoMySQL
from app.models.mysql.column_info_mysql import ColumnInfoMySQL


class MetaMysqlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    #向table_info表插入多条数据
    async def save_table_infos(self, table_infos: list[TableInfoMySQL]):
        for table_info in table_infos:
            await self.session.merge(table_info)

    #向column_info表插入多条数据
    async def save_column_infos(self, column_infos: list[ColumnInfoMySQL]):
        for column_info in column_infos:
            await self.session.merge(column_info)
