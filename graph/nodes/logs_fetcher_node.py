from graph.state.state import State
from llms.groq import groq_llm
from llms.gemini import gemini_llm
from langchain_core.messages import HumanMessage, AIMessage

def logs_fetcher_node(state: State) -> State:
    # Get the last message and its content
    last_message = state["messages"][-1]
    query = last_message.content if hasattr(last_message, 'content') else str(last_message)
    print("generated query: ", query)
    
    logs = gemini_llm.invoke(query)
    print("logs: ", logs)
    logs=logs.content if hasattr(logs, 'content') else str(logs)    
    
    # Add the response as an AIMessage
    state["messages"].append(AIMessage(content=logs))
    return state


