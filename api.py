# Importing Packages
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from main import chatbot

#FastAPI Instance
app = FastAPI(
    title="MamaMate AI",
    description="A Medical Chatbot API - which is expert in Gynecology, Motherhood, Sex Education, and Psychology.",
    version="1.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],    
)

# API Route
@app.post("/ask")
def handle_query(userID: str, userQuery: str):
    try:
        response = chatbot(userID, userQuery)

        # Check if the response is an error message (as per chatbot function)
        if isinstance(response, str) and response.startswith("Error"):
            return JSONResponse(content={"status": "error", "message": response}, status_code=500)

        return JSONResponse(content={"status": "success", "message": "Response generated successfully", "response": response}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": f"Unexpected error: {str(e)}"}, status_code=500)