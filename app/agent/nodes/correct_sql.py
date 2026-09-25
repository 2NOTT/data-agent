from langgraph.runtime import Runtime

from app.agent.context import DataAgentContext



def correct_sql(state,runtime:Runtime[DataAgentContext]):
    runtime.stream_writer({"state":"修正SQL"})

    return {}
