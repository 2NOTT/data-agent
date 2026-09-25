from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def extract_keywords(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"提取关键字"})

    return {}