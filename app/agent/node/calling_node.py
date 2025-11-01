from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.agent.state import State
from app.core.config import settings


def calling_node(state: State):


    chatGPT = ChatOpenAI(model_name="gpt-5-nano", temperature=0, openai_api_key=settings.OPENAI_API_KEY)

    system_message = (
        "You are a smart decision maker. "
        "Your task is to analyze the user's query and decide whether it is related to a database. "
        "If the query involves data storage, retrieval, tables, MySQL, SQL, CRUD, or anything about databases, output exactly 'database'. "
        "Otherwise, output exactly 'other'. "
        "Do not explain your reasoning or output anything else."
        
        "These are datils of database"
        """ Database name: `flight_update`
    Table name: `flight_tracer`

    Table schema:
    - flight_number (String, primary key)
    - airline (String)
    - origin (String)
    - destination (String)
    - departure (DateTime)
    - arrival (DateTime)
    - ticket_price (Float)"""
    )

    user_message = state.get("user_query", "")

    messages_LLM = [SystemMessage(content=system_message), HumanMessage(content=user_message)]
    response = chatGPT.invoke(messages_LLM)

    state["decision"] = response.content
    return state

