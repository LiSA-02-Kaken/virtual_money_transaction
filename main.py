from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"result":"ok"}

@app.get("/aiueo")
def aiueo():
    return {"result":"AIUEO"}