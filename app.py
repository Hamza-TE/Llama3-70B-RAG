from langchain_community.chat_models.azureml_endpoint import (
    AzureMLEndpointApiType,
    CustomOpenAIChatContentFormatter,
    AzureMLChatOnlineEndpoint
)
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Azure Cognitive Search endpoint and key
SEARCH_ENDPOINT = os.environ["SEARCH_ENDPOINT"]
SEARCH_KEY = os.environ["SEARCH_KEY"]
SEARCH_INDEX_NAME = os.environ["SEARCH_INDEX_NAME"]

# Function to query Azure Cognitive Search
def query_azure_search(query):
    search_url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX_NAME}/docs/search?api-version=2021-04-30-Preview"
    headers = {
        'Content-Type': 'application/json',
        'api-key': SEARCH_KEY
    }
    search_payload = {
        "search": query,
        "top": 1
    }
    response = requests.post(search_url, headers=headers, json=search_payload)
    response.raise_for_status()
    results = response.json()
    return results['value'][0]['content'] if results['value'] else ""

# Create an instance of the CustomOpenAIChatContentFormatter
content_formatter_instance = CustomOpenAIChatContentFormatter()

# Initialize the AzureMLChatOnlineEndpoint with the content formatter instance
chat = AzureMLChatOnlineEndpoint(
    endpoint_url="https://Llama-2-70b-chat-RAG-serverless.eastus.inference.ai.azure.com/v1/chat/completions",
    endpoint_api_type=AzureMLEndpointApiType.serverless,
    endpoint_api_key=os.environ["LLAMA2_KEY"],
    content_formatter=content_formatter_instance,
)

# Initialize Flask app
app = Flask(__name__)
message_history=[
    SystemMessage(content="You are a helpful assistant that helps by answering questions in detail. You provide answer with strictly only with the content provided and not your own knowledge")
]
# Initiate Flask routes for chatbot
@app.route('/')
def index():
    return render_template('index.html')

# Chatbot route--main route for chatbot--handels both GET and POST requests
@app.route('/chat', methods=['GET', 'POST'])
def chatbot():
    user_message = request.form.get('message')
    # Query Azure Cognitive Search
    search_results = query_azure_search(user_message)
    
    # If search results are found, add them to the message history
    if search_results:
        message_history.append(HumanMessage(content=f'{user_message}' + 'Use the context to answer the question. Context:' + f"Search results: {search_results}"))
        # Invoke the chat endpoint
        response = chat.invoke(message_history)
        message_history.append(AIMessage(content=response.content))
        return jsonify({"response": response.content})
    else:
        message_history.append(HumanMessage(content=user_message))
        message_history.append(AIMessage(content="No Match found in the documents try with some different prompt."))
        return jsonify({"response": "No Match found in the documents try with some different prompt."})
    

if __name__ == '__main__':
    app.run(debug=True)
