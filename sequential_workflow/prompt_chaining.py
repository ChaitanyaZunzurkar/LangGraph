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