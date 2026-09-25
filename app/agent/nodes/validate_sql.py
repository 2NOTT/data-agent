from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def validate_sql(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"校验SQL"})

    return {}
