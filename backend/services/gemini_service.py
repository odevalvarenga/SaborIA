import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

class AIServiceUnavailableError(Exception):
    pass

class AIInvalidResponseError(Exception):
    pass

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
fallback_model = os.getenv(
    "GEMINI_FALLBACK_MODEL",
    "gemini-3.5-flash-lite"
)

if not api_key:
    raise RuntimeError("GEMINI_API_KEY não foi configurada.")


client = genai.Client(api_key=api_key)


def build_prompt(
    ingredients: list[str],
    meal: str,
    difficulty: str,
    max_time: int
) -> str:

    ingredients_text = ", ".join(ingredients)

    return f"""
Você é o SaborIA, um assistente especializado em culinária.

Sua tarefa é criar uma receita utilizando os ingredientes
informados pelo usuário.

INGREDIENTES DISPONÍVEIS:
{ingredients_text}

TIPO DE REFEIÇÃO:
{meal}

NÍVEL DE DIFICULDADE:
{difficulty}

TEMPO MÁXIMO:
{max_time} minutos

REGRAS:
1. Crie uma receita compatível com os ingredientes disponíveis.
2. Respeite o tipo de refeição solicitado.
3. Respeite o nível de dificuldade.
4. Respeite o tempo máximo informado.
5. Priorize os ingredientes fornecidos pelo usuário.
6. Não invente ingredientes obrigatórios incompatíveis com a receita.
7. O tempo de preparo não pode ultrapassar {max_time} minutos.
8. Não forneça informações médicas ou nutricionais.
9. Retorne SOMENTE um JSON válido.
10. Não utilize Markdown.
11. Não coloque o JSON dentro de ```json.

O JSON deve obrigatoriamente seguir esta estrutura:

{{
    "nome": "Nome da receita",
    "tempo_preparo": 30,
    "dificuldade": "fácil",
    "ingredientes": [
        "ingrediente 1",
        "ingrediente 2"
    ],
    "modo_preparo": [
        "Passo 1",
        "Passo 2",
        "Passo 3"
    ]
}}
"""


def request_recipe(model: str, prompt: str) -> str:

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return response.text


def generate_recipe(
    ingredients: list[str],
    meal: str,
    difficulty: str,
    max_time: int
) -> dict:

    prompt = build_prompt(
        ingredients=ingredients,
        meal=meal,
        difficulty=difficulty,
        max_time=max_time
    )

    try:
        response_text = request_recipe(
            model=model_name,
            prompt=prompt
        )

    except ServerError:

        print(
            f"Modelo principal indisponível ({model_name}). "
            f"Tentando modelo de fallback ({fallback_model})."
        )

        try:
            response_text = request_recipe(
                model=fallback_model,
                prompt=prompt
            )

        except Exception as fallback_error:

            print(
                f"Erro no modelo de fallback: {fallback_error}"
            )

            raise AIServiceUnavailableError(
    "O serviço de Inteligência Artificial está "
    "temporariamente indisponível."
            ) from fallback_error

    try:
        return json.loads(response_text)

    except json.JSONDecodeError as error:

        print("A IA retornou um conteúdo que não é JSON válido.")
        print(response_text)

        raise AIInvalidResponseError(
    "A Inteligência Artificial retornou uma resposta "
    "em formato inválido."
) from error