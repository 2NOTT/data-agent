from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def execute_sql(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"执行SQL"})

    return {}
