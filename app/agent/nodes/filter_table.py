import yaml
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext
from app.agent.llm import llm
from app.agent.state import DataAgentState
from app.core.log import logger
from app.prompt.prompt_loader import load_prompt


# 利用大模型对table_infos进行过滤生成：{表名：[字段名1， 字段名2]}
async def filter_table(state: DataAgentState, runtime: Runtime[DataAgentContext]):
    runtime.stream_writer({"stage": "过滤表"})
    try:
        query = state["query"]
        table_infos = state["table_infos"]

        # 1. 调用模型，过滤掉不需要表和字段，生成需要的表名和字段名的列表的字典
        prompt_template = PromptTemplate(
            template=load_prompt("filter_table_info"),
            input_variables=["query", "table_infos"],
        )
        output_parser = JsonOutputParser()
        chain = prompt_template | llm | output_parser
        result = await chain.ainvoke({
            "query": query,
            "table_infos": yaml.dump(
                table_infos,
                allow_unicode=True, # 保留中文原文，不转换为unicode编码  ‘\u5317\u4eac’
                sort_keys=False, # 不要对数据中的字典中的属性进行排序，保持原来的顺序
            )
        })

        # 指标公式依赖的字段不能由模型裁剪掉。
        required_columns = {
            column_id
            for metric in state["metric_infos"]
            for column_id in metric["relevant_columns"]
        }
        # 2. 去对table_infos中的表和字段进行过滤
        for table_info in table_infos[:]:
            table_name = table_info["name"]
            required_names = {
                column_id.split(".", 1)[1]
                for column_id in required_columns
                if column_id.startswith(f"{table_name}.")
            }
            if table_name not in result and not required_names:
                table_infos.remove(table_info)  # 删除表
            else:
                columns = table_info["columns"]
                for column in columns[:]:
                    column_name = column["name"]
                    if column_name not in result.get(table_name, []) and column_name not in required_names:
                        columns.remove(column)  # 删除字段

        logger.info(f"过滤表完成:{table_infos}")
        return {"table_infos": table_infos}
    except Exception as e:
        logger.error(f"过滤表信息失败：{str(e)}")
        raise  # 抛出全部的错误  方便调试
        # raise e  # 只是抛出当前的
