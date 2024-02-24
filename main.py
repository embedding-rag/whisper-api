import uvicorn
# from server.api_server import app


if __name__ == "__main__":
    uvicorn.run(
        app="server.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=4
    )
