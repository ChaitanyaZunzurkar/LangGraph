from model import model
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class BlogState(TypedDict): 
    title: str
    outline: str
    content: str

def create_outline(state: BlogState) -> BlogState: 
    title = state['title']

    prompt = f'Generate the outline for a blog on the topic:- {title}'

    outline = model.invoke(prompt).content

    state['outline'] = outline
    return state

def create_blog(state: BlogState) -> BlogState: 
    title = state['title']
    outline = state['outline']

    prompt = f'Write a professional blog on the given topic: {title} using the following outline \n {outline}'

    content = model.invoke(prompt).content

    state['content'] = content

    return state

graph = StateGraph(BlogState)

graph.add_node('create_outline', create_outline)
graph.add_node('create_blog', create_blog)

graph.add_edge(START, 'create_outline')
graph.add_edge('create_outline', 'create_blog')
graph.add_edge('create_blog', END)

app = graph.compile()

def main():

    print("Blog Writer")
    print("Type 'exit' to quit.")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        result = app.invoke({
            "title": user_input,
            "outline": "",
            "content": ""
        })

        print("AI:", result["title"])
        print(result['outline'])
        print(result["content"])

if __name__ == "__main__":
    main()