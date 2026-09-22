from sqlalchemy.ext.asyncio import AsyncSession

class DWMysqlRepository:
    def __init__(self,session:AsyncSession):
        self.session=session


