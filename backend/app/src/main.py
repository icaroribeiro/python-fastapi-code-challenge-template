import uvicorn

from src import create_app
from src.infrastructure import application_settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=int(application_settings.http_port),
        reload=False,
        access_log=False,
    )
