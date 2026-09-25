from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def merge_retrieved_info(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"合并召回"})

    return {}
