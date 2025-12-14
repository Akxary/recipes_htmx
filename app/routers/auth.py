import logging
from typing import Annotated, Any, Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user_manager import (
    UserManager,
    VerificationResult,
    get_user_manager,
    error_code_map,
)
from app.api.utils import generate_verification_code, get_current_time
from app.models.base import get_fapi_db
from resources.config import VERIFICATION_CODE_LIMIT

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="resources/templates")
logger = logging.getLogger(__name__)


def get_default_context(user_manager: UserManager) -> dict[str, Any]:
    return {
        "user_email": user_manager.user_email,
        "expire_time": (get_current_time() + VERIFICATION_CODE_LIMIT).timestamp(),
    }


@router.get("/", response_class=HTMLResponse)
async def get_auth_page(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_fapi_db)],
    user_email: Optional[str] = None,
) -> HTMLResponse:
    context: dict[str, Any] = {"user_email": user_email}
    if user_email is not None:
        user_manager = UserManager(user_email, session)
        send_code_limit = await user_manager.check_send_code_limit()
        if send_code_limit > get_current_time():
            context["expire_time"] = send_code_limit.timestamp()
    return templates.TemplateResponse(
        request=request,
        name="auth_template.html",
        context=context,
    )


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
    expire_time: Optional[float] = Form(default=None),
) -> HTMLResponse:
    match await user_manager.check_verification_code(verification_code):
        case VerificationResult.SUCCESS:
            return templates.TemplateResponse(
                request=request,
                context=get_default_context(user_manager),
                name="base_template.html",
            )
        case ver_res:
            error_code = error_code_map[ver_res]
    context = {
        **get_default_context(user_manager),
        "error_code": error_code,
        "verification_code": verification_code,
    }
    if expire_time:
        context["expire_time"] = expire_time
    return templates.TemplateResponse(
        request=request,
        context=context,
        name="verification_code_template.html",
    )
