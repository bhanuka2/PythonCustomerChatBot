from langgraph.graph import StateGraph, START, END

from app.agent.node.chatbot_node import chatbot_node
from app.agent.state import State


def gen_graph():

    workflow = StateGraph(State)
    workflow.add_node("chatbot_node", chatbot_node)

    workflow.set_entry_point( "chatbot_node")
    workflow.add_edge("chatbot_node", END)



    return workflow.compile()




