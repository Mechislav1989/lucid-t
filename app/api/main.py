from fastapi import FastAPI

from api.endpoints import router as main_router



def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI service-sun",
        docs_url='/api/docs',
        description="Lucid FastApi MVC with DDD principles",
    )
    app.include_router(main_router, prefix='/')

    return app
