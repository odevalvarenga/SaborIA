from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List


app = FastAPI(
    title="SaborIA",
    description="API de geração de receitas com Inteligência Artificial",
    version="1.0.0"
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


@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "message": "SaborIA API funcionando!"
    }


@app.post("/api/recipes")
def create_recipe(request: RecipeRequest):
    return {
        "message": "Dados recebidos com sucesso!",
        "ingredients": request.ingredients,
        "meal": request.meal,
        "difficulty": request.difficulty,
        "max_time": request.max_time
    }