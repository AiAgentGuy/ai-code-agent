# AI Coding Agent

Welcome to the AI Coding Agent repository! This project is a Streamlit-based web application that provides a visualization tool for generating and validating code solutions using language models. The application integrates various technologies, including LangChain, Tavily, and OpenAI's GPT-4o model, to assist users in solving coding questions.

## Features

- **Streamlit UI**: A user-friendly interface with input fields and process visualization.
- **Code Generation**: Uses OpenAI's GPT-4o model to generate code solutions.
- **Error Handling**: Includes mechanisms to check for errors in the generated code.
- **Web Search Integration**: Utilizes Tavily for additional web search results when errors occur.
- **Session Management**: Maintains conversation history for better context and user experience.

## How It Works

1. **User Input**: The user enters a coding question in the sidebar.
2. **Code Generation**: The app generates a code solution using the GPT-4 model.
3. **Error Checking**: The generated code is checked for errors. If errors are detected, they are handled and possibly corrected using additional web searches.
4. **Process Visualization**: The process is visualized in real-time, showing each step's status.
5. **Conversation History**: The session history is displayed for user reference.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/AiAgentGuy/ai-coding-agent.git>
   cd <ai-coding-agent>
Create a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root directory of the project.
Add your API keys for OpenAI and Tavily as follows:
makefile
Copy code
OPENAI_API_KEY=<your_openai_api_key>
TAVILY_API_KEY=<your_tavily_api_key>
Run the application:

bash
Copy code
streamlit run app.py
Requirements
The project requires the following packages, as specified in the requirements.txt file:

streamlit
langchain
langchain_core
langchain_community
langchain_openai
langgraph
requests
beautifulsoup4
python-dotenv
tavily-python

License
This project is licensed under the MIT License. See the LICENSE file for more details.

