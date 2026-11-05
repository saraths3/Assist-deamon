from fastapi import FastAPI
from pydantic import BaseModel, Field
from decouple import config
from google import genai

app = FastAPI()

GEMINI_API_KEY = config('GEMINI_API_KEY')
client = genai.Client(api_key=GEMINI_API_KEY)
model = 'gemini-3.1-flash-lite'

class Ask(BaseModel):
    question: str
    sys_inst: str | None = Field(default=None, description= 'Optional rules for gemini.')
    json_mode: bool = Field(default=False, description='True for strict json output.')

@app.post('/api/ask/')
async def ask_gemini(ask: Ask):
    gemini_config = {}

    if ask.sys_inst:
        gemini_config['system_instruction'] = ask.sys_inst

    if ask.json_mode:
        gemini_config['response_mime_type'] = 'application/json'
        

    try:
        response = client.models.generate_content(
            model=model,
            contents=ask.question,
            config= gemini_config if gemini_config else None
        )
    except Exception as e:
        error_str = str(e)
        
        if '429' in error_str or 'resource_exhausted' in error_str:
            return {"error": "Rate limit exceeded. Please slow down and try again.", "details": error_str}
        elif '503' in error_str or 'service_unavailable' in error_str:
            return {"error": f"The model {model} is currently overloaded.", "details": error_str}
        elif '404' in error_str or 'not_found' in error_str:
            return {"error": f"The model {model} is unavailable.", "details": error_str}
        elif '401' in error_str or '403' in error_str or 'permission_denied' in error_str:
            return {"error": "Authentication failed. Check your GEMINI_API_KEY.", "details": error_str}
        elif '400' in error_str or 'invalid_argument' in error_str:
            return {"error": "Invalid request format.", "details": error_str}
        else:
            return {'error': error_str}
        
    return {'answer': response.text}


class ChatRequest(BaseModel):
    message: str
    history: list | None = Field(default=None, description="Previous conversation turns")
    sys_inst: str | None = Field(default=None, description="Optional system instructions")
    json_mode: bool = Field(default=False, description="True for strict json output")

@app.post('/api/chat/')
async def chat_endpoint(req: ChatRequest):
    gemini_config = {}

    if req.sys_inst:
        gemini_config['system_instruction'] = req.sys_inst

    if req.json_mode:
        gemini_config['response_mime_type'] = 'application/json'

    try:
        chat_session = client.chats.create(
            model=model,
            history=req.history if req.history else None,
            config=gemini_config if gemini_config else None
        )
        
        response = chat_session.send_message(req.message)
        
    except Exception as e:
        error_str = str(e)
        if '429' in error_str or 'resource_exhausted' in error_str:
            return {"error": "Rate limit exceeded. Please slow down.", "details": error_str}
        elif '503' in error_str or 'service_unavailable' in error_str:
            return {"error": f"The model {model} is overloaded.", "details": error_str}
        else:
            return {'error': error_str}
        
    return {
        'response': response.text,
        'history': chat_session.get_history()
    }