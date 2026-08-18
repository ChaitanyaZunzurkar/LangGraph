from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class BatsmanState(TypedDict): 
    runs: int
    balls: int
    fours: int
    sixes: int

    strike_rate: float
    boundary_per_balls: float
    boundary_percent: float

    summary: str


def calculate_strike_rate(state: BatsmanState):
    runs = state['runs']
    balls = state['balls']

    return {
        "strike_rate": (runs / balls) * 100 if balls > 0 else 0
    }

def calculate_boundary_per_balls(state: BatsmanState):
    fours = state['fours']
    sixes = state['sixes']
    balls = state['balls']

    boundary = fours + sixes

    return {
        "boundary_per_balls": balls / boundary if boundary > 0 else 0
    }

def calculate_boundary_percent(state: BatsmanState):
    runs = state['runs']
    fours = state['fours']
    sixes = state['sixes']

    boundary_runs = (fours * 4) + (sixes * 6)

    return {
        "boundary_percent": (
            boundary_runs / runs
        ) * 100 if runs > 0 else 0
    }

def summary(state: BatsmanState) -> BatsmanState:
    result = f"""
    Runs: {state['runs']}
    Balls: {state['balls']}
    Fours: {state['fours']}
    Sixes: {state['sixes']}
    Strike Rate: {state['strike_rate']:.2f}
    Balls per Boundary: {state['boundary_per_balls']:.2f}
    Boundary Percent: {state['boundary_percent']:.2f}%
    """

    return {
        "summary": result
    }

graph = StateGraph(BatsmanState)

graph.add_node('calculate_strike_rate', calculate_strike_rate)
graph.add_node('calculate_boundary_per_balls', calculate_boundary_per_balls)
graph.add_node('calculate_boundary_percent', calculate_boundary_percent)
graph.add_node('summary', summary)

graph.add_edge(START, 'calculate_strike_rate')
graph.add_edge(START, 'calculate_boundary_per_balls')
graph.add_edge(START, 'calculate_boundary_percent')

graph.add_edge('calculate_strike_rate', 'summary')
graph.add_edge('calculate_boundary_per_balls', 'summary')
graph.add_edge('calculate_boundary_percent', 'summary')

graph.add_edge('summary', END)

app = graph.compile()

result = app.invoke({
    "runs": 50,
    "balls": 40,
    "fours": 5,
    "sixes": 2,
    "strike_rate": 0,
    "boundary_per_balls": 0,
    "boundary_percent": 0,
    "summary": ""
})

print(result["summary"])