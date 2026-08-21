from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# --------------------------------------------------
# 1. Define the State
# --------------------------------------------------

class State(TypedDict):
    age: int
    result: str


# --------------------------------------------------
# 2. Define Nodes
# --------------------------------------------------

def check_age(state: State):
    """Check whether the person is an adult or minor."""

    if state["age"] >= 18:
        return {"result": "adult"}
    else:
        return {"result": "minor"}


def adult_node(state: State):
    """Runs when age >= 18."""
    print("Person is an adult")
    return {}


def minor_node(state: State):
    """Runs when age < 18."""
    print("Person is a minor")
    return {}


# --------------------------------------------------
# 3. Define Conditional Routing Function
# --------------------------------------------------

def decide_next(state: State):
    """
    This function decides which node should execute next.
    """

    if state["result"] == "adult":
        return "adult"

    return "minor"


# --------------------------------------------------
# 4. Create Graph
# --------------------------------------------------

graph = StateGraph(State)


# Add nodes
graph.add_node("check_age", check_age)
graph.add_node("adult", adult_node)
graph.add_node("minor", minor_node)


# --------------------------------------------------
# 5. Add Edges
# --------------------------------------------------

# START -> check_age
graph.add_edge(START, "check_age")


# Conditional edge
graph.add_conditional_edges(
    "check_age",
    decide_next,
    {
        "adult": "adult",
        "minor": "minor"
    }
)


# Both branches -> END
graph.add_edge("adult", END)
graph.add_edge("minor", END)


# --------------------------------------------------
# 6. Compile
# --------------------------------------------------

app = graph.compile()


# --------------------------------------------------
# 7. Run
# --------------------------------------------------

result = app.invoke({
    "age": 20,
    "result": ""
})

print(result)