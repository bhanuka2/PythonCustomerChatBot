from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.agent.state import State
from app.agent.tools.db_tools import fetch_flight_data
from app.core.config import settings


def execute_database_query(state:State) -> State:
    sql_query=state.get("sql_query")
    data = fetch_flight_data.invoke(sql_query)

    chatGPT = ChatOpenAI(model_name="gpt-5-nano", temperature=0, openai_api_key=settings.OPENAI_API_KEY)

    system_message = (
    "convert the flight data into a friendly and easy-to-understand response for the user. "
    "Hey there! You’re a friendly flight assistant who loves helping people find flight info. "
    "When the user asks about flights, give clear and easy answers in a casual tone. "
    "If they just say hi or make small talk, reply warmly and keep it short. "
    "Stay natural, like you’re chatting with a friend — not too formal, just helpful and nice!"

    )

    messages_LLM = [SystemMessage(content=system_message), HumanMessage(content=data)]
    response = chatGPT.invoke(messages_LLM)

    state["response"] = response.content
    return state



