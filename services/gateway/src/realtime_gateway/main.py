from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Casino Platform Gateway",
        docs_url="/docs",
    )

    @app.get("/health/live")
    async def live() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()