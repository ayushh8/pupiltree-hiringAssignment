from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated, List
import operator
from config import GROQ_API_KEY
from app.tools import get_hotel_info, book_hotel_room, reschedule_booking

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

class HotelBookingAgent:
    def __init__(self):
        self.llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-70b-8192")
        self.tools = [get_hotel_info, book_hotel_room, reschedule_booking]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("llm", self._call_llm)
        tool_node = ToolNode(self.tools)
        graph.add_node("tools", tool_node)

        graph.set_entry_point("llm")
        
        graph.add_conditional_edges(
            "llm",
            self._should_call_tools,
            {
                "tools": "tools",
                END: END
            }
        )
        graph.add_edge("tools", "llm")

        return graph.compile()
    
    def _should_call_tools(self, state: AgentState):
        last_message = state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return END

    def _call_llm(self, state: AgentState):
        response = self.llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def run(self, message: str, thread_id: str):
        return self.graph.invoke({"messages": [HumanMessage(content=message)]}, 
                                 config={"configurable": {"thread_id": thread_id}})

agent = HotelBookingAgent() 