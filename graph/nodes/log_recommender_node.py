from graph.state.state import State
from llms.gemini import gemini_llm
from langchain_core.messages import AIMessage


def log_recommender_node(state: State) -> State:
    # Get the last message (analysis) and its content
    last_message = state["messages"][-1]
    analysis = last_message.content if hasattr(last_message, 'content') else str(last_message)
    print("Generating recommendations...")
    
    prompt = f'''Based on the following log analysis, provide:
    1. Specific actionable recommendations
    2. Priority levels for each recommendation
    3. Expected impact of implementing each recommendation
    4. Required resources or changes
    
    Analysis:
    {analysis}
    '''
    
    response = gemini_llm.invoke(prompt)
    recommendations = response.content if hasattr(response, 'content') else str(response)
    print("Recommendations generated")
    
    # Add the recommendations as a new message
    state["messages"].append(AIMessage(content=recommendations))
    return state 