# Importing Packages
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage 
from langchain.agents import tool, Tool
from langchain_google_community import GoogleSearchAPIWrapper
from mongoDbServices import fetch_chat, save_chat

# Loading OPENAI API_KEY
load_dotenv()

# Paths
currentPath = os.path.dirname(os.path.abspath(__file__))
booksPath = os.path.join(currentPath, 'documents')
chromaPath = os.path.join(currentPath, 'db', 'chromaDB')

# Defining the Embeddings
embeddings = OpenAIEmbeddings(
        model='text-embedding-3-small'
)

# Checking is the chroma path exist or not
if not os.path.exists(chromaPath):
    print('Chroma Path Not Exist. Lets add it: ')

    # Checking is the books path exist or not
    if not os.path.exists(booksPath):
        raise FileExistsError('Books Path Not Find, Please check it & try again.')
    
    # List all the text files.
    booksList = [f for f in os.listdir(booksPath) if f.endswith('.txt')]

    # Reading each book content & loading it using TextLoader & also adding the metadata(Source) with it
    documents = []
    for bookIs in booksList:
        eachBookPath = os.path.join(booksPath, bookIs)
        loader = TextLoader(eachBookPath)
        loadedDataIs = loader.load()
        for doc in loadedDataIs:
            doc.metadata = {'source': bookIs}
            documents.append(doc)

    
    # Splitting the data into chunks
    textSplitter = CharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    docs = textSplitter.split_documents(documents)


    # Chroma DB
    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=chromaPath
    )

    print('Finished!')

else:
    print('Chroma Path Already Exist. No need to add it again.')

# Chroma - DB
chromaDB = Chroma(
    embedding_function=embeddings,
    persist_directory=chromaPath
)

# Let's define some tools for agent.

# Tool # 01 - For Retriveing the relevant data from the vector DB - Chroma
@tool 
def fetch_relevant_documents(userQuery: str):
    """Fetches general documents from the Chroma database for Gynecology, Motherhood, Sex Education, and Psychology."""
    print('------------------------ Agent is in fetch_relevant_documents tool ------------------------')
    retriever = chromaDB.as_retriever(
        search_type="mmr",
        search_kwargs={
            'k': 5, 
            'fetch_k': 20, 
            'lambda_mult': 0.5,
            'filter': {'source': {'$in': ['gynecology.txt', 'psychology.txt', 'motherhood.txt', 'sexEducation.txt']}}  # Only categories books
        }
    )
    retrieverResponse = retriever.invoke(userQuery)
    return "\n\n".join([doc.page_content for doc in retrieverResponse]) if retrieverResponse else 'No Relevant Documents Found.'

# Tool # 02 - For External Searching Using GoogleSearchAPIWrapper
@tool
def external_search(userQuery: str):
    """Search externally for information if no documents are found in Chroma DB."""
    print('------------------------ Agent is in external_search tool ------------------------')
    search = GoogleSearchAPIWrapper()

    
    search_tool = Tool(
    name="Google Search",
    func=search.run, 
    description="Use this tool to search Google for the latest information."
    )

    results = search_tool.invoke(userQuery) 
    return f"External info for '{userQuery}': {results}" 

# Tool # 03 - For Providing Medication Information
@tool
def fetch_medication_info(userQuery: str):
    """Fetches medication-related documents from the Chroma database."""
    print('------------------------ Agent is in fetch_medication_info tool ------------------------')
    retriever = chromaDB.as_retriever(
        search_type="mmr",
        search_kwargs={
            'k': 3, 
            'fetch_k': 20, 
            'lambda_mult': 0.5,
            'filter': {'source': 'medication.txt'}  # Only medication book
        }
    )
    retrieverResponse = retriever.invoke(userQuery)
    return "\n\n".join([doc.page_content for doc in retrieverResponse]) if retrieverResponse else 'No medication information found in the database.'


# Defining the tools in the list for agent.
myTools = [
    fetch_relevant_documents,
    external_search,
    fetch_medication_info
]

# System Prompt
PROMPT = """
You are a chatbot designed to assist females with issues related to Gynecology, Motherhood, Sex Education, and Psychology. You have access to the conversation history, which you should use to maintain context and continuity in your responses.

- If the query is related to these categories, use the `fetch_relevant_documents` tool to retrieve general information from the Chroma database and answer precisely & accurately, incorporating relevant context from the conversation history.
- If the query implies a medical issue that might require medication, use the `fetch_medication_info` tool to search for medication-related data in the Chroma database, explain the issue, suggest appropriate medications, and include a disclaimer: 'Consult a doctor before starting any medication.'
- If no relevant information is found in the Chroma database for either `fetch_relevant_documents` or `fetch_medication_info`:
  - If the query suggests a need for medication, use the `external_search` tool to search externally and suggest medications only from credible medical sources (e.g., Mayo Clinic, WebMD, NIH). If no verified medication info is found, respond with: 'I can’t provide specific medication recommendations without verified data—please consult a healthcare professional.'
  - If the query does not require medication, use the `external_search` tool to search externally and provide a precise answer based on the results.
- If the query is unrelated to these categories, respond with: 'Sorry, I can only assist with Gynecology, Motherhood, Sex Education, and Psychology.'
- When responding, acknowledge relevant parts of the conversation history for coherence and context.
"""

# OpenAI - LLM
openAI = ChatOpenAI(
    model='gpt-4o'
).bind_tools(myTools) 

# Chatbot Function
def chatbot(userID, userQuery):
    # Adding System Message into a list of messages
    messages = [SystemMessage(PROMPT)]

    # Fetching the chat history of the user from the mongodb using user_id & adding it in messages list
    messages.extend(fetch_chat(userID))

    # Adding user query in messages as HumanMessage
    messages.append(HumanMessage(userQuery))
    print(f"--- -- -- - -- - - - After adding messages are: {messages}")

    try:
        # Calling the LLM - OpenAI
        response = openAI.invoke(messages)
        print(f"Initial LLM Response: {response.content}, Tool Calls: {response.tool_calls}")
        # Storing the response in messages as AIMessage
        messages.append(response)
    except Exception as e:
        print(f"Error in invoking LLM: {e}")
        return f"Error in invoking LLM: {e}"
   

    # Handling the tool calls during response
    while response.tool_calls:
        for tool_call in response.tool_calls:
            try:
                if tool_call['name'] == 'fetch_relevant_documents':
                    # Fetching the relevant documents from the DB & Storing in Messagegs as ToolMessage
                    dbResponse = fetch_relevant_documents.invoke(tool_call['args']['userQuery'])
                    messages.append(ToolMessage(dbResponse, tool_call_id=tool_call['id']))
                elif tool_call['name'] == 'fetch_medication_info':
                    # Fetching the medication info from the DB & Storing in Messagegs as ToolMessage
                    medicationInfo = fetch_medication_info.invoke(tool_call['args']['userQuery'])
                    messages.append(ToolMessage(medicationInfo, tool_call_id=tool_call['id']))
                elif tool_call['name'] == 'external_search':
                    # Searching Externally about the user query & Storing in Messagegs as ToolMessage
                    searchResult = external_search.invoke(tool_call['args']['userQuery'])
                    messages.append(ToolMessage(searchResult,tool_call_id=tool_call['id']))
            except Exception as e:
                print(f"Error in invoking tool: {e}")
                return f"Error in invoking tool: {e}"   

            try:
                # Invoking the LLM - OpenAI with updated messages
                response = openAI.invoke(messages)
                messages.append(response)
            except Exception as e:
                print(f"Error in invoking LLM: {e}")
                return f"Error in invoking LLM: {e}"    

    # Saving the chat history in the mongodb for user(user-query)
    save_chat({
        'user_id': userID,
        'role': 'user',
        'content': userQuery
    }) 
   
    # Saving the chat history in the mongodb for assistant(ai-response)
    save_chat({
        'user_id': userID,
        'role': 'assistant',
        'content': response.content
    })

    return response.content