from typing import Annotated, Any, Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.api.recipe_manager import RecipeManager, get_recipe_manager


router = APIRouter()
templates = Jinja2Templates(directory="resources/templates")


@router.get("/")
async def index(
    request: Request,
    recipe_manager: Annotated[RecipeManager, Depends(get_recipe_manager)],
) -> HTMLResponse:
    context: dict[str, Any] = {}
    all_recipes = await recipe_manager.get_all_recipes()
    context["all_recipes"] = all_recipes
    if recipe_manager.user_manager is not None:
        context["user_email"] = recipe_manager.user_manager.user_email

    return templates.TemplateResponse(
        request=request,
        name="recipes.html",
        context=context,
    )


@router.get("/recipe/{recipe_id}")
async def recipe_detail(
    request: Request,
    recipe_id: int,
    recipe_manager: Annotated[RecipeManager, Depends(get_recipe_manager)],
) -> HTMLResponse:
    recipe = await recipe_manager.get_recipe_by_id(recipe_id)
    context: dict[str, Any] = {"recipe": recipe}
    if recipe_manager.user_manager is not None:
        context["user_email"] = recipe_manager.user_manager.user_email

    return templates.TemplateResponse(
        request=request,
        name="recipe_detail.html",
        context=context,
    )

@router.post("/add")
async def add_recipe(
    request: Request,
    recipe_manager: Annotated[RecipeManager, Depends(get_recipe_manager)],
    recipe_desc: str,
) -> JSONResponse:
    await recipe_manager.add_new_recipe(recipe_desc)
    return JSONResponse({"status": "OK"})
