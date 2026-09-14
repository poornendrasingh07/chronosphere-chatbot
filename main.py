from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Chronosphere Chatbot",
    description="AI-powered chatbot for Chronosphere Lab",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# Initialize LLM and memory
llm = ChatOpenAI(
    temperature=0.7,
    model_name="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Store conversations in memory
conversations = {}

def get_or_create_conversation(conversation_id: str):
    """Get or create a conversation chain"""
    if conversation_id not in conversations:
        memory = ConversationBufferMemory()
        conversations[conversation_id] = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )
    return conversations[conversation_id]

# Routes
@app.get("/")
def read_root():
    return {
        "message": "Chronosphere Chatbot API",
        "status": "running",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "conversations": "/conversations"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint that processes user messages and returns AI responses
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get or create conversation
        conversation = get_or_create_conversation(request.conversation_id)
        
        # Get AI response
        response = conversation.predict(input=request.message)
        
        return ChatResponse(
            response=response,
            conversation_id=request.conversation_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations")
def list_conversations():
    """List all active conversations"""
    return {
        "conversations": list(conversations.keys()),
        "count": len(conversations)
    }

@app.delete("/conversations/{conversation_id}")
def clear_conversation(conversation_id: str):
    """Clear a specific conversation"""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": f"Conversation {conversation_id} cleared"}
    else:
        raise HTTPException(status_code=404, detail="Conversation not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
