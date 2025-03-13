from fastapi import FastAPI

def make_web_app():
    app = FastAPI()

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

    return app
