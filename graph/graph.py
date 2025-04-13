from graph.state.state import State
from langgraph.graph import StateGraph
from graph.nodes.query_generator_node import query_generator_node
from graph.nodes.logs_fetcher_node import logs_fetcher_node
from graph.nodes.log_analyzer_node import log_analyzer_node
from graph.nodes.log_recommender_node import log_recommender_node
from langgraph.graph import StateGraph, START, END


graph_builder = StateGraph(State)


graph_builder.add_node("query_generator_node", query_generator_node)
graph_builder.add_node("logs_fetcher_node", logs_fetcher_node)
graph_builder.add_node("log_analyzer_node", log_analyzer_node)
graph_builder.add_node("log_recommender_node", log_recommender_node)

graph_builder.add_edge(START, "query_generator_node")
graph_builder.add_edge("query_generator_node", "logs_fetcher_node")
graph_builder.add_edge("logs_fetcher_node", "log_analyzer_node")
graph_builder.add_edge("log_analyzer_node", "log_recommender_node")
graph_builder.add_edge("log_recommender_node", END)    

graph = graph_builder.compile()

__all__ = ['graph']