import logging
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory="resources/templates")
logger = logging.getLogger(__name__)

@router.get("/", response_class=HTMLResponse)
async def get_auth_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="auth_template.html")


@router.post("/get-verification-code")
async def send_verification_code(user_email: str) -> None:
    logger.warning("Got %s user email. Sending verification code", user_email)


@router.post("/check-verification-code")
async def check_verification_code(verification_code: int) -> bool:
    return JSONResponse({"status": True})
