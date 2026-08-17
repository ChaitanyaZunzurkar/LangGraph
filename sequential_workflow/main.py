from langgraph.graph import StateGraph, START, END
from typing import TypedDict 

class BMICalculator(TypedDict):
    weight_kg: float 
    height_m: float
    bmi: float
    category: str


def calculateBmi(state: BMICalculator) -> BMICalculator: 
    weight = state['weight_kg']
    height = state['height_m']
    bmi = (weight / (height ** 2))

    state['bmi'] = round(bmi, 2)
    return state

def label_bmi(state: BMICalculator) -> BMICalculator:
    bmi = state['bmi']

    if bmi < 18.5: 
        state['category'] = "Underweight"
    elif 18.5 <= bmi <= 24: 
        state['category'] = "Normal"
    elif 25 <= bmi <= 30: 
        state['category'] = "Overweight"
    else: 
        state['category'] = "Obses"

    return state

# define your graph 
graph = StateGraph(BMICalculator)

# define your node 
graph.add_node("calculate_bmi", calculateBmi) 
graph.add_node("label_bmi", label_bmi)

# define your edges 
graph.add_edge(START, 'calculate_bmi')
graph.add_edge('calculate_bmi', 'label_bmi')
graph.add_edge('label_bmi', END)

# compile your graph
workflow = graph.compile()

# execute the graph
result = workflow.invoke({
    'weight_kg': 54.0, 
    'height_m': 1.68,
})

print(result['bmi'])
print(result['category'])
