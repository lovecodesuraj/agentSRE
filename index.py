try:
    from graph.visualize_graph import visualize_graph
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Note: Graph visualization is not available in this environment")

from graph.graph import graph


if __name__ == "__main__":
    print("Starting the application...")
    
    if VISUALIZATION_AVAILABLE:
        print("Attempting to visualize graph...")
        try:
            visualize_graph()
            print("Graph visualization complete")
        except Exception as e:
            print(f"Graph visualization failed: {str(e)}")
    else:
        print("Skipping graph visualization")

    def stream_graph_updates(user_input: str):
        print(f"\nProcessing input: {user_input}")
        try:
            for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
                for value in event.values():
                    print("Assistant:", value["messages"][-1].content)
        except Exception as e:
            print(f"Error processing input: {str(e)}")

    print("\nEnter your message (or type 'quit', 'exit', or 'q' to end):")
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Using fallback input...")
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break
