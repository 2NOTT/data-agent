from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def recall_metric(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"召回指标"})

    return {}
