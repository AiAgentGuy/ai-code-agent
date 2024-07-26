from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os

# Set up the OpenAI API key
os.environ['OPENAI_API_KEY'] = 'your_actual_openai_api_key'

# Initialize the language model
llm = OpenAI(temperature=0)

# Define a prompt template
prompt = PromptTemplate(input_variables=['question'], template='Answer the following question: {question}')

# Define a tool that uses human input
def human_input_tool(query):
    return input(query)

human_tool = Tool(
    name='Human',
    func=human_input_tool,
    description='Use human input to answer questions'
)

# Initialize the agent with the human tool
agent = initialize_agent(
    tools=[human_tool],
    llm=llm,
    prompt=prompt,
    verbose=True
)

# Example usage
question = 'What is the capital of France?'
response = agent.run(question)
print(response)