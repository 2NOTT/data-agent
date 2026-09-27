from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.state import DataAgentState
from app.core.log import logger
from app.core.sql_guard import SQLValidationError, validate_read_only_sql


async def validate_sql(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    runtime.stream_writer({"state": "校验SQL"})

    sql = ''
    try:
        sql = validate_read_only_sql(state["sql"])
        dw_mysql_repo = runtime.context["dw_mysql_repo"]

        # 检查SQL语法是否合法
        await dw_mysql_repo.validate_sql(sql)

        logger.info(f"校验SQL成功：{sql}")
        return {"sql": sql, "error": None}
    except SQLValidationError as e:
        logger.warning(f"SQL安全校验失败：{e}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"校验SQL失败：{sql}")
        return {"error": f"SQL语法错误：{str(e)}"}
        # raise

    return {}
