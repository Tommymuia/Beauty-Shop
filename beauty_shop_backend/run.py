import uvicorn
import os

if __name__ == "__main__":
    # This looks inside the 'app' folder for 'main.py' and the 'app' variable
    # Disable reload in production (when RENDER env var is set)
    reload = not os.getenv("RENDER", False)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=reload)