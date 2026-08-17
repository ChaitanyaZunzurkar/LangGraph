from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from model import model 

# -----------------------------
# 2. Define the State
# -----------------------------

class LLMState(TypedDict):
    question: str
    answer: str


# -----------------------------
# 3. Define the Node
# -----------------------------

def llm_qa(state: LLMState) -> LLMState:

    question = state["question"]

    prompt = f"Answer the following question: {question}"

    answer = model.invoke(prompt).content

    state["answer"] = answer

    return state


# -----------------------------
# 4. Create the Graph
# -----------------------------

graph = StateGraph(LLMState)

# Add node
graph.add_node("llm_qa", llm_qa)

# START → llm_qa
graph.add_edge(START, "llm_qa")

# llm_qa → END
graph.add_edge("llm_qa", END)

# Compile the graph
app = graph.compile()


# -----------------------------
# 5. Main Function
# -----------------------------

def main():

    print("Question Answer Chatbot")
    print("Type 'exit' to quit.")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Send input to LangGraph
        result = app.invoke({
            "question": user_input,
            "answer": ""
        })

        print("AI:", result["answer"])


# -----------------------------
# 6. Run the program
# -----------------------------

if __name__ == "__main__":
    main()