#Importing Packages
from pymongo import MongoClient, ASCENDING
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# from dotenv import load_dotenv

# Importing the MongoDB Connection link from .env file
# load_dotenv()

connection_link = 'mongodb+srv://mamamate_user:mamamate_1234@mycluster.p7jte.mongodb.net/'

def save_chat(data: dict):
    data['timestamp'] = datetime.now()
    with MongoClient(connection_link) as client:
        client['mamamate']['messages'].insert_one(data)



def fetch_chat(user_id: str):
    with MongoClient(connection_link) as client:
        data = list(client['mamamate']['messages'].find({'user_id': user_id}).sort('timestamp', ASCENDING))

    messages = []

    for message in data:
        if message['role'] == 'assistant':
                messages.append(AIMessage(message['content']))
        elif message['role'] == 'user':
                messages.append(HumanMessage(message['content']))

    print('-------------------------- Fetched Chats Are: \n', messages)

    return messages