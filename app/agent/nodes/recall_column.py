from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def recall_column(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"召回字段"})

    return {}
