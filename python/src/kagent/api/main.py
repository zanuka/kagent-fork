from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .mcp import router as mcp_router
from .tools import router as tools_router
from .modelconfigs import router as modelconfigs_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mcp_router, prefix="/api/mcp")
app.include_router(tools_router, prefix="/api")
app.include_router(modelconfigs_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083) 
