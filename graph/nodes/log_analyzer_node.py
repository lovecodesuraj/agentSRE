from graph.state.state import State
from llms.gemini import gemini_llm
from langchain_core.messages import AIMessage
import matplotlib.pyplot as plt
import pandas as pd
import json
import os


def generate_charts_from_analysis(analysis_data: dict, output_dir: str = 'charts'):
    """Generate visualization charts from analysis data"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Time series chart if available
    if 'time_series' in analysis_data:
        plt.figure(figsize=(12, 6))
        time_data = analysis_data['time_series']
        plt.plot(time_data['timestamps'], time_data['values'])
        plt.title('Log Activity Over Time')
        plt.xlabel('Time')
        plt.ylabel('Event Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/time_series.png')
        plt.close()
    
    # Error distribution chart
    if 'error_distribution' in analysis_data:
        plt.figure(figsize=(10, 6))
        error_data = analysis_data['error_distribution']
        plt.bar(error_data['types'], error_data['counts'])
        plt.title('Error Type Distribution')
        plt.xlabel('Error Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/error_distribution.png')
        plt.close()
    
    # Severity pie chart
    if 'severity_distribution' in analysis_data:
        plt.figure(figsize=(8, 8))
        severity_data = analysis_data['severity_distribution']
        plt.pie(severity_data['counts'], labels=severity_data['levels'], autopct='%1.1f%%')
        plt.title('Log Severity Distribution')
        plt.savefig(f'{output_dir}/severity_distribution.png')
        plt.close()


def log_analyzer_node(state: State) -> State:
    # Get the last message (logs) and its content
    last_message = state["messages"][-1]
    logs = last_message.content if hasattr(last_message, 'content') else str(last_message)
    print("Analyzing logs...")
    
    # First prompt to get structured analysis and chart data
    analysis_prompt = f'''You are a log analysis expert. Analyze the following logs and provide:
    1. Key findings and patterns
    2. Statistical analysis of log types
    3. Trend analysis
    4. Potential issues or anomalies
    5. Security concerns
    
    Additionally, provide the following data in JSON format for visualization:
    {{
        "time_series": {{
            "timestamps": ["timestamp1", "timestamp2", ...],
            "values": [count1, count2, ...]
        }},
        "error_distribution": {{
            "types": ["error_type1", "error_type2", ...],
            "counts": [count1, count2, ...]
        }},
        "severity_distribution": {{
            "levels": ["critical", "error", "warning", "info"],
            "counts": [count1, count2, count3, count4]
        }}
    }}
    
    Logs to analyze:
    {logs}
    '''
    
    response = gemini_llm.invoke(analysis_prompt)
    analysis_text = response.content if hasattr(response, 'content') else str(response)
    
    # Extract JSON data from the response
    try:
        # Find JSON data in the response
        json_start = analysis_text.find('{')
        json_end = analysis_text.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            chart_data = json.loads(analysis_text[json_start:json_end])
            generate_charts_from_analysis(chart_data)
            # Remove JSON from the analysis text
            analysis_text = analysis_text[:json_start] + analysis_text[json_end:]
    except Exception as e:
        print(f"Error processing chart data: {str(e)}")
    
    # Add chart information to analysis
    analysis_text += "\n\nVisualization charts have been generated in the 'charts' directory."
    print("Analysis complete")
    
    # Add the analysis as a new message
    state["messages"].append(AIMessage(content=analysis_text))
    return state 