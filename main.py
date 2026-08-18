import uvicorn

# This block ensures it only runs if you execute this file directly
if __name__ == "__main__":
    uvicorn.run("app.api:app")
