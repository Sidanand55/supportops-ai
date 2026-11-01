from fastapi import FastAPI


app= FastAPI(
    title="SupportOps AI",
    description="Multi-agent AI Customer Support Platform",
)

@app.get("/")
async def root():
    return{
        "message" : "Welcome to SupportOps AI",
        "status" : "running"        
    }
    
@app.get("/health")
async def health():
    return{
        "status": "healthy"
    }