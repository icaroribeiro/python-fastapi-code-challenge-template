import uvicorn
from src import create_app
from src.infrastructure import application_settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=int(application_settings.http_port),
        reload=False,
        access_log=False,
    )
