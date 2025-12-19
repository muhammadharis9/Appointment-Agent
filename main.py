import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

async def check_calendar(date: str):
    """
    Checks if a slot is available. 
    (Currently mocked to always say YES so we can test the voice flow first)
    """
    print(f"🔎 AI is asking about availability on: {date}")
    # TODO: In Sprint 4, we will uncomment the real Cal.com API call here.
    return {"status": "available", "message": f"Yes, we have openings on {date} at 2 PM and 4 PM."}



@app.post("/")
async def handle_vapi_request(request: Request):
    """
    Vapi calls this URL whenever the AI wants to use a tool.
    """
    payload = await request.json()
    message = payload.get("message", {})
    
    # 1. Handle Tool Calls (The AI wants to do something)
    if message.get("type") == "tool-calls":
        tool_calls = message.get("toolCalls", [])
        results = []
        
        for tool in tool_calls:
            function_name = tool["function"]["name"]
            tool_id = tool["id"]
            args = json.loads(tool["function"]["arguments"])
            
            print(f"🛠️ Tool Triggered: {function_name}")
            
            result = {}
            if function_name == "checkCalendar":
                result = await check_calendar(args.get("date"))
            
            results.append({
                "toolCallId": tool_id,
                "result": json.dumps(result)
            })
            
        # Send the result back to Clara so she can speak it
        return JSONResponse(content={
            "results": results
        })

    # 2. Handle Status Updates (Call ended, Started, etc.)
    # We just acknowledge these for now.
    return JSONResponse(content={"status": "ok"})

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)