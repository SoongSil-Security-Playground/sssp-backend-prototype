import uvicorn

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 8000
    uvicorn.run("SSSP.api.app:apimain", host=HOST, port=PORT, reload=True)
