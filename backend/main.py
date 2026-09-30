from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

from services.gemini_service import (
    generate_recipe,
    AIServiceUnavailableError,
    AIInvalidResponseError
)


app = FastAPI(
    title="SaborIA",
    description="API de geração de receitas com Inteligência Artificial",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecipeRequest(BaseModel):
    ingredients: List[str] = Field(
        ...,
        min_length=1,
        max_length=15,
        description="Lista de ingredientes disponíveis"
    )
    meal: str = Field(
        ...,
        min_length=2,
        max_length=30,
        description="Tipo de refeição"
    )
    difficulty: str = Field(
        ...,
        min_length=4,
        max_length=15,
        description="Nível de dificuldade"
    )
    max_time: int = Field(
        ...,
        ge=5,
        le=300,
        description="Tempo máximo de preparo em minutos"
    )


class RecipeResponse(BaseModel):
    nome: str
    tempo_preparo: int
    dificuldade: str
    ingredientes: List[str]
    modo_preparo: List[str]


@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "message": "SaborIA API funcionando!"
    }


@app.post("/api/recipes")
def create_recipe(request: RecipeRequest):

    try:
        recipe = generate_recipe(
            ingredients=request.ingredients,
            meal=request.meal,
            difficulty=request.difficulty,
            max_time=request.max_time
        )

        validated_recipe = RecipeResponse(**recipe)

        return {
            "message": "Receita gerada com sucesso!",
            "recipe": validated_recipe
        }

    except AIServiceUnavailableError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except AIInvalidResponseError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )