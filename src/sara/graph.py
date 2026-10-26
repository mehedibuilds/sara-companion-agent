from langgraph.graph import END, START, StateGraph
from sara.agents.registry import SpecialistRegistry
from sara.memory import MemoryStore
from sara.models import Intent, Turn

def classify(text: str) -> Intent:
    lowered = text.lower()
    keywords = {
        Intent.CODE: ("code", "bug", "python", "api"),
        Intent.RESEARCH: ("search", "research", "find"),
        Intent.SEO: ("seo", "keyword", "rank"),
        Intent.IMAGE: ("image", "generate image", "draw"),
        Intent.VIDEO: ("youtube", "video"),
    }
    return next((kind for kind, words in keywords.items() if any(word in lowered for word in words)), Intent.CHAT)

def build_graph(memory: MemoryStore, specialists: SpecialistRegistry):
    async def perceive(state: Turn) -> dict:
        return {"intent": classify(state["text"]).value, "memories": await memory.context_for(state["user_id"], state["text"])}
    async def companion(state: Turn) -> dict:
        return {"specialist_result": await specialists.execute(Intent(state["intent"]), state["text"], state.get("memories", []))}
    async def synthesize(state: Turn) -> dict:
        answer = state.get("specialist_result") or "I’m here. What would you like to work through?"
        await memory.record_turn(state["user_id"], f"user: {state['text']}\nassistant: {answer}")
        return {"response": answer}
    graph = StateGraph(Turn)
    graph.add_node("perception", perceive)
    graph.add_node("companion", companion)
    graph.add_node("synthesis", synthesize)
    graph.add_edge(START, "perception")
    graph.add_edge("perception", "companion")
    graph.add_edge("companion", "synthesis")
    graph.add_edge("synthesis", END)
    return graph.compile()