import uvicorn

# This block ensures it only runs if you execute this file directly
if __name__ == "__main__":
    uvicorn.run("app.api:app", host="127.0.0.1", port=8000, reload=True)
