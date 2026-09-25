
from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def filter_metric(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"过滤指标"})

    return {}