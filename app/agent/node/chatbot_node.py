from http.client import responses

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.agent.state import State
from app.core.config import settings


def chatbot_node(state: State )-> State:
    chatGPT = ChatOpenAI(model_name="gpt-5-nano", temperature=0,openai_api_key=settings.OPENAI_API_KEY)

    system_message = (
        "You are a helpful assistant that helps users find information about flights. "
        "Use the user's query to provide accurate and concise information."
        "If it is a greeting or casual remark, respond in a friendly manner but keep it brief."
    )

    user_message = state.get("user_query", "")

    messages_LLM = [SystemMessage(content=system_message),HumanMessage(content=user_message)]
    response = chatGPT.invoke(messages_LLM)

    state["response"] = response.content
    return state

