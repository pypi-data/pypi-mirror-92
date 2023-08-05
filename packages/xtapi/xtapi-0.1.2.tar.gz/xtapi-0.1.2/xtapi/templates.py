"""xtapi templates."""
from fastapi.templating import Jinja2Templates


class Templates(Jinja2Templates):
    """Templates."""

    def render(self, page, context):
        return self.TemplateResponse(page, context)
