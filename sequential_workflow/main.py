from langgraph.graph import StateGraph, START, END
from typing import TypedDict 

class BMICalculator(TypedDict):
    weight_kg: float 
    height_m: float
    bmi: float


def calculateBmi(state: BMICalculator) -> BMICalculator: 
    weight = state['weight_kg']
    height = state['height_m']
    bmi = (weight / (height ** 2))

    state['bmi'] = round(bmi, 2)
    return state

# define your graph 
graph = StateGraph(BMICalculator)

# define your node 
graph.add_node("calculate_bmi", calculateBmi) 

# define your edges 
graph.add_edge(START, 'calculate_bmi')
graph.add_edge('calculate_bmi', END)

# compile your graph
workflow = graph.compile()

# execute the graph
result = workflow.invoke({
    'weight_kg': 54.0, 
    'height_m': 1.68,
})

print(result['bmi'])
