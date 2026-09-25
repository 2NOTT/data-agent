from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def filter_table(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"过滤表"})

    return {}
