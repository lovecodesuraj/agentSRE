from graph.state.state import State
from llms.groq import groq_llm
from llms.gemini import gemini_llm
from langchain_core.messages import HumanMessage, AIMessage


def query_generator_node(state: State) -> State:
    # Get the last message and its content
    last_message = state["messages"][-1]
    query = last_message.content if hasattr(last_message, 'content') else str(last_message)
    print("human query: ", query)
    
    prompt = f'''You are a LOGQL query generator. You will be given a query and you will need to generate a LOGQL query for it.
    Query: {query}'''
    
    response = gemini_llm.invoke(prompt)

    # Extract the content from the response if it's a message object
    query = response.content if hasattr(response, 'content') else str(response)
    print("generated query: ", query)
    
    # Add the response as an AIMessage with just the content string
    state["messages"].append(AIMessage(content=query))
    return state


