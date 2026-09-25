from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def generate_sql(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"生成SQL"})

    return {}
