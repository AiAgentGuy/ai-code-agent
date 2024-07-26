# AI Coding Agent

Welcome to the AI Coding Agent repository! This Streamlit-based web application provides a powerful visualization tool for generating and validating code solutions using advanced language models. By integrating cutting-edge technologies such as LangChain, Tavily, and OpenAI's GPT-4 model, our application assists users in solving a wide range of coding challenges.

## Features

- **Intuitive Streamlit UI**: A clean, user-friendly interface with input fields and real-time process visualization.
- **Advanced Code Generation**: Leverages OpenAI's GPT-4 model to produce high-quality code solutions.
- **Robust Error Handling**: Implements sophisticated mechanisms to detect and address errors in generated code.
- **Intelligent Web Search Integration**: Utilizes Tavily for supplementary web search results when encountering errors or requiring additional context.
- **Efficient Session Management**: Maintains a comprehensive conversation history for improved context and user experience.

## How It Works

1. **User Input**: Users input their coding questions through the sidebar.
2. **Code Generation**: The application generates a code solution using the GPT-4 model.
3. **Error Detection and Handling**: The generated code undergoes thorough error checking. If issues are detected, they are addressed, potentially using additional web searches for context.
4. **Real-time Process Visualization**: Each step of the process is visualized in real-time, providing users with clear status updates.
5. **Conversation History**: A complete session history is displayed for user reference and context continuity.

## Installation

Follow these steps to set up and run the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AiAgentGuy/ai-coding-agent.git
   cd ai-coding-agent
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # For Unix or MacOS
   python3 -m venv venv
   source venv/bin/activate

   # For Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project's root directory and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Requirements

The project relies on the following key packages:

- streamlit
- langchain
- langchain_core
- langchain_community
- langchain_openai
- langgraph
- requests
- beautifulsoup4
- python-dotenv
- tavily-python

For a complete list of dependencies, refer to the `requirements.txt` file.

## Running the Streamlit App

To start the Streamlit app, ensure you're in the project directory with your virtual environment activated, then run:

```bash
streamlit run app.py
```

This command will start the Streamlit server and automatically open the application in your default web browser. If it doesn't open automatically, you can access the app by navigating to the URL provided in the terminal (usually `http://localhost:8501`).

## Contributing

We welcome contributions to the AI Coding Agent project! Please feel free to submit issues, fork the repository and send pull requests!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository. We're here to help!
