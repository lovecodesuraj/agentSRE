from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate, SystemMessagePromptTemplate
from langchain_google_vertexai import ChatVertexAI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tool_agent(llm: ChatVertexAI, tools: list, system_prompt: str):
    """Helper function to create agents with custom tools and system prompt
    Args:
        llm (ChatVertexAI): LLM for the agent
        tools (list): list of tools the agent will use
        system_prompt (str): text describing specific agent purpose
    Returns:
        executor (AgentExecutor): Runnable for the agent created.
    """
    
    logger.info(f"Creating agent with tools: {[tool.name for tool in tools]}")
    
    system_prompt_template = PromptTemplate(
                template= system_prompt + """
                ONLY respond to the part of query relevant to your purpose.
                IGNORE tasks you can't complete. 
                Use the following context to answer your query 
                if available: \n {agent_history} \n
                """,
                input_variables=["agent_history"],
            )
    
    logger.info("System prompt template created")
    
    system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt_template)
    prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt,
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    
    logger.info("Creating tool calling agent")
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    logger.info("Creating agent executor")
    executor = AgentExecutor(agent=agent, tools=tools, 
                return_intermediate_steps=True, verbose=True)
    
    logger.info("Agent setup complete")
    return executor