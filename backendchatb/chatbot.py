from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from instructions import information

# ✅ Directly adding API key instead of using .env
OPENAI_API_KEY = "your_openai_api_key_here"

# Enhanced web search tool for general queries
@tool(description="Provides information for general queries beyond CHARUSAT university topics")
def web_search(query: str) -> str:
    return (
        "I can help you with general information based on my training. "
        "While I specialize in CHARUSAT university information, I can also "
        "provide helpful insights on general topics while maintaining accuracy."
    )

tools = [web_search]

# ✅ Initialize LangChain AI Client with adjusted temperature
client = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0.7,  # Increased for more flexible responses
    api_key="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"
)

# ✅ Enhanced chatbot prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", information),
    ("system", """
    You are a versatile AI assistant that can handle both CHARUSAT-related and general queries.
    For CHARUSAT queries, use the provided university information.
    For general queries, provide helpful and accurate information based on your training.
    Always maintain a professional and friendly tone.
    If unsure, acknowledge limitations and be honest about it.
    """),
    ("placeholder", "{messages}"),
    ("placeholder", "{agent_scratchpad}"),
])

# ✅ Create chatbot agent
agent = create_tool_calling_agent(client, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

# ✅ Temporary chat history storage
demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="messages",
    output_messages_key="output",
)

def run_agent(messages, session_id):
    """
    Process user messages and return responses using the conversational agent.
    
    Args:
        messages: The user's input message
        session_id: Unique identifier for the chat session
    
    Returns:
        The agent's response
    """
    response = conversational_agent_executor.invoke(
        {"messages": [messages]},
        {"configurable": {"session_id": session_id}},
    )   
    return response

# Make sure run_agent is available for import
__all__ = ['run_agent']