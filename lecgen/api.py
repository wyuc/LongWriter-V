from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from lecgen.generator import polish

app = FastAPI()

class PolishRequest(BaseModel):
    imgs: List[str] = Field(..., description="List of base64 encoded images")
    scripts: List[str] = Field(..., description="List of corresponding scripts")

class PolishResponse(BaseModel):
    success: bool
    script: str | None = None
    error: str | None = None

@app.post("/polish", response_model=PolishResponse)
async def polish_endpoint(request: PolishRequest):
    try:
        if len(request.imgs) == 0 or len(request.scripts) == 0:
            raise ValueError("Images and scripts lists cannot be empty")
            
        if len(request.imgs) != len(request.scripts) + 1:
            raise ValueError("Number of images should be equal to number of scripts + 1")

        result = polish(
            imgs=request.imgs,
            scripts=request.scripts,
        )
        return PolishResponse(success=True, script=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
