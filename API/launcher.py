def app():
    from fastapi import FastAPI
    from fastapi.openapi.utils import get_openapi
    from fastapi.openapi.docs import (
        get_redoc_html,
        get_swagger_ui_html,
        get_swagger_ui_oauth2_redirect_html,
    )
    from fastapi.staticfiles import StaticFiles

    app = FastAPI(title="Title", docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_css_url="static/swagger-ui.css",
            swagger_js_url="static/swagger-ui-bundle.js",
            swagger_favicon_url="static/favicon.png",
        )
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_css_url="static/swagger-ui.css",
            swagger_js_url="static/swagger-ui-bundle.js",
            swagger_favicon_url="static/favicon.png",
        )

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="static/redoc-standalone.js",
            redoc_favicon_url="static/favicon.png",
        )

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="API Docs.",
            version="3.2.0",
            description="OpenAPI schema",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "/static/logo.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi