from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.core.log import logger


async def execute_sql(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"执行SQL"})

    try:
        sql = state["sql"]
        dw_mysql_repo=runtime.context["dw_mysql_repo"]

        #执行SQL
        result =await dw_mysql_repo.execute_sql(sql)

        #将查询结果写给调用者
        runtime.stream_writer({"type": "result", "sql": sql, "result": result})
        logger.info(f"执行SQL成功 result={result}")
        return {"result": result}
    except Exception as e:
        logger.error(f"执行SQL失败")
        raise
