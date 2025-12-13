import logging
from typing import Annotated, Any
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user_manager import UserManager, get_user_manager
from app.api.utils import generate_verification_code
from app.models.base import get_fapi_db

router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory="resources/templates")
logger = logging.getLogger(__name__)


def get_default_context(user_manager: UserManager) -> dict[str, Any]:
    return {"user_email": user_manager.user_email}


@router.get("/", response_class=HTMLResponse)
async def get_auth_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="auth_template.html")


@router.post("/get-verification-code", response_class=HTMLResponse)
async def send_verification_code(
    request: Request,
    user_manager: Annotated[UserManager, Depends(get_user_manager)],
) -> HTMLResponse:
    await user_manager.get_user()
    verification_code = generate_verification_code()
    await user_manager.set_verification_code(verification_code=verification_code)
    logger.warning(
        "Got %s user email. Sending verification code %s",
        user_manager.user_email,
        verification_code,
    )

    return templates.TemplateResponse(
        request=request,
        name="verification_code_template.html",
        context=get_default_context(user_manager),
    )


@router.post("/check-verification-code")
async def check_verification_code(
    request: Request,
    user_manager: Annotated[UserManager, Depends(get_user_manager)],
    verification_code: int = Form(...),
) -> HTMLResponse:
    if await user_manager.check_verification_code(verification_code):
        return templates.TemplateResponse(
            request=request,
            context=get_default_context(user_manager),
            name="base_template.html",
        )
    return templates.TemplateResponse(
        request=request,
        context=get_default_context(user_manager),
        name="not_valid_verification_code.html",
    )
