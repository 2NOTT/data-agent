from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class DWMysqlRepository:
    def __init__(self,session:AsyncSession):
        self.session=session

    async def get_column_types(self, table_name:str) -> dict[str, str]:
        """获取当前表的所有字段的类型"""
        #定义查询sql
        sql=f"show columns from {table_name}"
        #执行sql
        result=await self.session.execute(text(sql))
        #整理数据并返回
        return {row.Field:row.Type for row in result.all()}

    async def get_column_values(self,table_name:str ,column_name:str ,limit:int=10)->list:
        """查询指定字段的前limit个字段值"""
        # 定义查询sql
        sql=f"select distinct {column_name} from {table_name} limit {limit}"
        # 执行sql
        result = await self.session.execute(text(sql))
        # 整理数据并返回
        return result.scalars().all()


