from fastapi import FastAPI, responses
from routes import task, analytics

app = FastAPI()

app.include_router(task.router)
app.include_router(analytics.router, prefix='/analytics')

@app.get('/')
def home():
    return {"Hello": "From Task"}