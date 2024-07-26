import streamlit as st
import os
import uuid
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import END, StateGraph
import requests
from bs4 import BeautifulSoup
from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables from a .env file
load_dotenv()

# Initialize Streamlit app with a title and layout configuration
st.set_page_config(page_title="AI Codeing Agent", layout="wide")
st.title("Code Generation Visualization")

# Sidebar input area for the user to enter their coding question
st.sidebar.header("Input")
user_question = st.sidebar.text_area("Enter your coding question:", height=100)

# Define the main content area with two columns
col1, col2 = st.columns(2)

# Left column for process visualization
with col1:
    st.header("Process Visualization")
    process_status = st.empty()
    current_step = st.empty()

# Right column for displaying the generated code output
with col2:
    st.header("Code Output")
    code_output = st.empty()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Load API keys from environment variables
tavily_api_key = os.getenv("TAVILY_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize Tavily search tool and OpenAI language model
tavily_tool = TavilySearchResults(max_results=3)
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=openai_api_key)

# Define the prompt template for generating code solutions
code_gen_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a coding assistant. Ensure any code you provide can be executed with all required imports and variables 
    defined. Structure your answer: 1) a prefix describing the code solution, 2) the imports, 3) the functioning code block.
    \n Here is the user question:"""),
    ("placeholder", "{messages}"),
])

# Define the schema for the code solution using Pydantic
class Code(BaseModel):
    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")
    description = "Schema for code solutions to questions about LCEL."

# Create a language model chain with structured output
code_gen_chain = llm.with_structured_output(Code, include_raw=False)


# Define a typed dictionary for the graph state
class GraphState(TypedDict):
    error: str
    messages: Annotated[list[AnyMessage], add_messages]
    generation: str
    iterations: int
    web_search_attempts: int


# Set maximum iterations and web search attempts
max_initial_iterations = 1
max_web_search_attempts = 5


# Function to generate code solution
def generate(state: GraphState):
    messages = state["messages"]
    iterations = state["iterations"]
    code_solution = code_gen_chain.invoke(messages)
    messages.append(AIMessage(content=f"Here is my attempt to solve the problem: {code_solution.prefix} \n Imports: {code_solution.imports} \n Code: {code_solution.code}"))
    iterations += 1
    return {"generation": code_solution, "messages": messages, "iterations": iterations, "web_search_attempts": state["web_search_attempts"]}

# Function to check the generated code for errors
def code_check(state: GraphState):
    messages = state["messages"]
    code_solution = state["generation"]
    iterations = state["iterations"]
    imports = code_solution.imports
    code = code_solution.code

    try:
        exec(imports)
    except Exception as e:
        error_message = f"Your solution failed the import test. Here is the error: {e}. Reflect on this error and your prior attempt to solve the problem. (1) State what you think went wrong with the prior solution and (2) try to solve this problem again. Return the FULL SOLUTION. Use the code tool to structure the output with a prefix, imports, and code block:"
        messages.append(HumanMessage(content=error_message))
        
         # Perform web search based on the error
        search_results = tavily_tool.invoke({"query": str(e)})
        
        return {"generation": code_solution, "messages": messages, "iterations": iterations, "error": "yes", "web_search_attempts": state["web_search_attempts"]}

    try:
        combined_code = f"{imports}\n{code}"
        global_scope = {}
        exec(combined_code, global_scope)
    except Exception as e:
        error_message = f"Your solution failed the code execution test: {e}"
        messages.append(HumanMessage(content=error_message))
        
        search_results = tavily_tool.invoke({"query": str(e)})
                
        return {"generation": code_solution, "messages": messages, "iterations": iterations, "error": "yes", "web_search_attempts": state["web_search_attempts"]}

    return {"generation": code_solution, "messages": messages, "iterations": iterations, "error": "no", "web_search_attempts": state["web_search_attempts"]}


# Function to fetch the full content of a webpage
def fetch_full_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        text_elements = []
        for element in soup.descendants:
            if element.name in ['p', 'code', 'textarea']:
                text = element.get_text(separator=' ', strip=True)
                if text:
                    text_elements.append(text)
        
        full_content = ' '.join(text_elements)
        
        return full_content
    except Exception as e:
        return ""

# Function to perform web search and update state
def web_search(state: GraphState):
    user_message = next((msg for msg in state["messages"] if isinstance(msg, HumanMessage)), None)
    if not user_message:
        return state

    question = user_message.content
    search_results = tavily_tool.invoke({"query": question})
    
    
    state["iterations"] = 0
    state["web_search_attempts"] += 1
    return state


def decide_to_finish(state: GraphState):
    error = state["error"]
    iterations = state["iterations"]
    web_search_attempts = state["web_search_attempts"]
    
    if error == "no":
        return "end"
    
    if web_search_attempts < max_web_search_attempts:
        return "web_search"
    
    if iterations < max_initial_iterations or (web_search_attempts > 0 and iterations < max_web_search_attempts):
        return "generate"
    
    return "end"


# Build the state graph for the code generation process
builder = StateGraph(GraphState)
builder.add_node("generate", generate)
builder.add_node("check_code", code_check)
builder.add_node("web_search", web_search)

builder.set_entry_point("generate")
builder.add_edge("generate", "check_code")
builder.add_conditional_edges(
    "check_code",
    decide_to_finish,
    {
        "end": END,
        "generate": "generate",
        "web_search": "web_search"
    }
)
builder.add_edge("web_search", "generate")


# Function to run the code generation process
def run_code_generation(question: str):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    events = builder.compile().stream({"messages": [HumanMessage(content=question)], "iterations": 0, "web_search_attempts": 0}, config, stream_mode="values")
    return list(events)

# Run button in the sidebar to start code generation
if st.sidebar.button("Generate Code"):
    if user_question:
        st.session_state.messages = []  # Clear previous messages
        events = run_code_generation(user_question)
        
        for i, event in enumerate(events):
            if 'generation' in event:
                process_status.text(f"Step {i+1}: Generating code solution")
                current_step.text("Current step: Code generation")
                code_solution = event['generation']
                code_output.code(f"{code_solution.imports}\n\n{code_solution.code}", language="python")
            elif 'error' in event:
                if event['error'] == 'yes':
                    process_status.text(f"Step {i+1}: Code check failed")
                    current_step.text("Current step: Error handling")
                else:
                    process_status.text(f"Step {i+1}: Code check passed")
                    current_step.text("Current step: Code verification")
            elif 'web_search_attempts' in event and event['web_search_attempts'] > 0:
                process_status.text(f"Step {i+1}: Performing web search")
                current_step.text("Current step: Web search")
            
            if 'messages' in event:
                # Filter out web search results from the messages
                filtered_messages = [msg for msg in event['messages'] if not msg.content.startswith("Web search results:")]
                st.session_state.messages.extend(filtered_messages)
        
        process_status.text("Process completed")
        current_step.text("Final step: Code generation complete")
    else:
        st.sidebar.warning("Please enter a coding question.")

# Display conversation history
st.header("Conversation History")
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.info(msg.content)
    elif isinstance(msg, AIMessage):
        st.success(msg.content)