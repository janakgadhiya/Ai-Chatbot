from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware before including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],  # Both localhost and IP format
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods 
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Authentication!"}