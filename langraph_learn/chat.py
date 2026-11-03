from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START , END
from langgraph.graph.message import StateGraph, add_messages

class State(TypedDict):
    #Messages have the type "list". The add_messages function in the annotation defines how this state key should be updated(in this case it appends new messages to the list, rather than overwriting it)
    messages: Annotated[list , add_messages ]

def chatbot(state:State):
    print("\n\nChatBot Node is running with state:", state)
    return {"messages": ["Hi, This is a message from the ChatBot Node"]}

def sampleNode(state:State):
    print("\n\nSample Node is running with state:", state)
    return {"messages": ["Sample message appended to the state"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sampleNode", sampleNode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sampleNode")
graph_builder.add_edge("sampleNode", END)

#(START) -> chatbot -> sampleNode -> (END)

graph = graph_builder.compile()

updated_state=graph.invoke(State({"messages": ["Hey There,I am Yasharth and I am a Software Engineer"]}))

print("\n\nUpdated state after graph execution:", updated_state)

#state={ messages:["Hey There"]}
#node runs : chatbot(state: {"Hey There"})-> ["Hi, This is a message from the ChatBot Node"]
#updated state={ messages:["Hey There", "Hi, This is a message from the ChatBot Node"]}