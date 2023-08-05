"""xtapi main."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


class MainApp(FastAPI):
    """main api."""

    def mount(self, path, directory, name=None):
        super().mount(path, StaticFiles(directory=directory), name=name)

    def run(self, name='main:app', reload=True, host='0.0.0.0', port=7000):
        import uvicorn
        uvicorn.run(name, reload=reload, host=host, port=port)

    def register_routers(self, router_config: list):
        """register routers"""
        for router, config in router_config:
            self.include_router(router, **config)

    def register_exception_handlers(self, handlers_config: list):
        for code, handler in handlers_config:
            self.add_exception_handler(code, handler)
