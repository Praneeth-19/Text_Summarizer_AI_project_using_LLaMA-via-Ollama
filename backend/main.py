from fastapi import FastAPI, Form, HTTPException
import requests

app = FastAPI()

@app.post("/summarize/")
def summarize(text: str = Form(...)):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": f"Summarize this:\n\n{text}",
                "stream": False
            }
        )
        response.raise_for_status()  # Raise an exception for bad HTTP status codes
        
        result = response.json()
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
            
        if "response" not in result:
            raise HTTPException(status_code=500, detail="Unexpected API response format")
            
        return {"summary": result["response"]}
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)