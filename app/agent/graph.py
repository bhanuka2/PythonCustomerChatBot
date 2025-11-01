
from langgraph.graph import StateGraph, START, END

from app.agent.node.execute_database_query import execute_database_query
from app.agent.node.calling_node import calling_node
from app.agent.node.chatbot_node import chatbot_node
from app.agent.node.db_node import db_node
from app.agent.state import State


def gen_graph():

    workflow = StateGraph(State)
    workflow.add_node("chatbot_node", chatbot_node)
    workflow.add_node("calling_node", calling_node)
    workflow.add_node("db_node", db_node)
    workflow.add_node("execute_database_query", execute_database_query)

    def route_after_calling_node (state: State) -> str:
        decision = state.get("decision")

        if decision == "database":
            return "db_node"
        else:
            return "chatbot_node"

    workflow.set_entry_point( "calling_node")

    workflow.add_conditional_edges(
        "calling_node",
        route_after_calling_node,
        {
            "db_node": "db_node",
            "chatbot_node": "chatbot_node",
        }
    )

    workflow.add_edge("chatbot_node", END)
    workflow.add_edge("db_node", "execute_database_query")
    workflow.add_edge("execute_database_query", END)

    return workflow.compile()




