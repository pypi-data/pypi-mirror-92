"""xtapi responses."""
from fastapi.responses import (
    HTMLResponse as FastAPIHTMLResponse,
    JSONResponse as FastAPIJSONResponse,
    PlainTextResponse as FastAPIPlainTextResponse,
)


class PlainTextResponse(FastAPIPlainTextResponse):
    """PlainTextResponse"""


class HTMLResponse(FastAPIHTMLResponse):
    """HTMLResponse"""


class JSONResponse(FastAPIJSONResponse):
    """JSONResponse."""
