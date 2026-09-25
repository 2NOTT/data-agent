from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def add_extra_context(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"添加额外信息"})

    return {}
