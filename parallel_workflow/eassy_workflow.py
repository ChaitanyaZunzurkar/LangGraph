import sys
import os

# Add LangGraph project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from model import model

from operator import add
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, START, END


# ============================================================
# STATE
# ============================================================

class EssayState(TypedDict):
    essay: str

    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str

    overall_feedback: str

    # Reducer combines scores from parallel nodes
    individual_score: Annotated[list[int], add]


# ============================================================
# LANGUAGE EVALUATION
# ============================================================

def evaluate_language(state: EssayState):

    prompt = f"""
Evaluate the LANGUAGE of the following essay.

Essay:
{state['essay']}

Focus on:

1. Grammar
2. Vocabulary
3. Sentence construction
4. Spelling
5. Overall language quality

Give detailed and constructive feedback.

At the end, give a score out of 10.

Use exactly this format:

FEEDBACK:
<detailed feedback>

SCORE:
<number from 0 to 10>
"""

    result = model.invoke(prompt)

    return {
        "language_feedback": result.content,

        # Temporary score for reducer demonstration.
        # We will use a fixed placeholder here because this
        # Hugging Face model does not provide structured output.
        "individual_score": [0]
    }


# ============================================================
# ANALYSIS EVALUATION
# ============================================================

def evaluate_analysis(state: EssayState):

    prompt = f"""
Evaluate the ANALYSIS and CONTENT of the following essay.

Essay:
{state['essay']}

Focus on:

1. Relevance to the topic
2. Depth of analysis
3. Quality of arguments
4. Supporting points
5. Logical reasoning
6. Accuracy of ideas

Give detailed and constructive feedback.

At the end, give a score out of 10.

Use exactly this format:

FEEDBACK:
<detailed feedback>

SCORE:
<number from 0 to 10>
"""

    result = model.invoke(prompt)

    return {
        "analysis_feedback": result.content,
        "individual_score": [0]
    }


# ============================================================
# CLARITY EVALUATION
# ============================================================

def evaluate_clarity(state: EssayState):

    prompt = f"""
Evaluate the CLARITY and STRUCTURE of the following essay.

Essay:
{state['essay']}

Focus on:

1. Organization
2. Flow of ideas
3. Clarity
4. Coherence
5. Introduction
6. Conclusion
7. Ease of understanding

Give detailed and constructive feedback.

At the end, give a score out of 10.

Use exactly this format:

FEEDBACK:
<detailed feedback>

SCORE:
<number from 0 to 10>
"""

    result = model.invoke(prompt)

    return {
        "clarity_feedback": result.content,
        "individual_score": [0]
    }


# ============================================================
# OVERALL EVALUATION
# ============================================================

def overall_evaluation(state: EssayState):

    prompt = f"""
Provide an overall evaluation of this essay.

Essay:
{state['essay']}

Here are the three independent evaluations:

LANGUAGE:
{state['language_feedback']}

ANALYSIS:
{state['analysis_feedback']}

CLARITY AND STRUCTURE:
{state['clarity_feedback']}

Give an overall assessment.

Include:

1. Major strengths
2. Major weaknesses
3. Specific improvements
4. Overall score out of 10

Use exactly this format:

OVERALL FEEDBACK:
<detailed overall feedback>

OVERALL SCORE:
<number from 0 to 10>
"""

    result = model.invoke(prompt)

    return {
        "overall_feedback": result.content
    }


# ============================================================
# CREATE GRAPH
# ============================================================

graph = StateGraph(EssayState)


# Add nodes
graph.add_node(
    "evaluate_language",
    evaluate_language
)

graph.add_node(
    "evaluate_analysis",
    evaluate_analysis
)

graph.add_node(
    "evaluate_clarity",
    evaluate_clarity
)

graph.add_node(
    "overall_evaluation",
    overall_evaluation
)


# ============================================================
# PARALLEL EDGES
# ============================================================

graph.add_edge(
    START,
    "evaluate_language"
)

graph.add_edge(
    START,
    "evaluate_analysis"
)

graph.add_edge(
    START,
    "evaluate_clarity"
)


# ============================================================
# JOIN
# ============================================================

graph.add_edge(
    "evaluate_language",
    "overall_evaluation"
)

graph.add_edge(
    "evaluate_analysis",
    "overall_evaluation"
)

graph.add_edge(
    "evaluate_clarity",
    "overall_evaluation"
)


graph.add_edge(
    "overall_evaluation",
    END
)


# ============================================================
# COMPILE
# ============================================================

app = graph.compile()


# ============================================================
# INPUT
# ============================================================

essay = """
Artificial intelligence is becoming increasingly important in modern society.
It is used in healthcare, education, transportation and many other fields.
AI can improve productivity and make many tasks easier. However, it can also
create problems such as job displacement, privacy concerns and misuse of
technology.

Therefore, society should focus on using artificial intelligence responsibly.
Governments should create appropriate regulations, while companies should
ensure that AI systems are safe and transparent. Humans should also remain
involved in important decisions.
"""


# ============================================================
# INVOKE GRAPH
# ============================================================

result = app.invoke({

    "essay": essay,

    "language_feedback": "",
    "analysis_feedback": "",
    "clarity_feedback": "",

    "overall_feedback": "",

    "individual_score": []
})


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n================ LANGUAGE EVALUATION ================\n")
print(result["language_feedback"])


print("\n================ ANALYSIS EVALUATION ================\n")
print(result["analysis_feedback"])


print("\n================ CLARITY EVALUATION ================\n")
print(result["clarity_feedback"])


print("\n================ INDIVIDUAL SCORES ================\n")
print(result["individual_score"])


print("\n================ OVERALL EVALUATION ================\n")
print(result["overall_feedback"])