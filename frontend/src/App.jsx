import { useState } from "react";
import {
  ChefHat,
  Clock,
  Sparkles,
  Utensils,
  AlertCircle,
} from "lucide-react";
import "./index.css";

function App() {
  const [ingredients, setIngredients] = useState("");
  const [meal, setMeal] = useState("almoço");
  const [difficulty, setDifficulty] = useState("fácil");
  const [maxTime, setMaxTime] = useState(40);

  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleGenerateRecipe() {
    setError("");
    setRecipe(null);

    if (!ingredients.trim()) {
      setError("Informe pelo menos um ingrediente.");
      return;
    }

    const ingredientsList = ingredients
      .split(",")
      .map((item) => item.trim())
      .filter((item) => item.length > 0);

    if (ingredientsList.length === 0) {
      setError("Informe pelo menos um ingrediente válido.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/recipes",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ingredients: ingredientsList,
            meal,
            difficulty,
            max_time: maxTime,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Não foi possível gerar a receita."
        );
      }

      setRecipe(data.recipe);
    } catch (error) {
      setError(
        error.message ||
          "Ocorreu um erro ao conectar com o SaborIA."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <ChefHat size={32} />
          <span>SaborIA</span>
        </div>

        <div className="header-subtitle">
          <Sparkles size={18} />
          <span>Receitas inteligentes com IA</span>
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div className="hero-icon">
            <ChefHat size={32} />
          </div>

          <h1>O que temos na cozinha?</h1>

          <p>
            Informe os ingredientes que você tem e deixe a
            Inteligência Artificial criar uma receita para você.
          </p>
        </section>

        <section className="recipe-form">
          <div className="form-group">
            <label htmlFor="ingredients">
              Ingredientes
            </label>

            <textarea
              id="ingredients"
              placeholder="Ex: frango, batata, cenoura, cebola..."
              value={ingredients}
              onChange={(event) =>
                setIngredients(event.target.value)
              }
            />

            <small>
              Separe os ingredientes por vírgula.
            </small>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="meal">
                <Utensils size={18} />
                Refeição
              </label>

              <select
                id="meal"
                value={meal}
                onChange={(event) =>
                  setMeal(event.target.value)
                }
              >
                <option value="café da manhã">
                  Café da manhã
                </option>
                <option value="almoço">Almoço</option>
                <option value="jantar">Jantar</option>
                <option value="lanche">Lanche</option>
                <option value="sobremesa">
                  Sobremesa
                </option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="difficulty">
                Dificuldade
              </label>

              <select
                id="difficulty"
                value={difficulty}
                onChange={(event) =>
                  setDifficulty(event.target.value)
                }
              >
                <option value="fácil">Fácil</option>
                <option value="médio">Médio</option>
                <option value="difícil">Difícil</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="maxTime">
              <Clock size={18} />
              Tempo máximo: {maxTime} minutos
            </label>

            <input
              id="maxTime"
              type="range"
              min="5"
              max="120"
              step="5"
              value={maxTime}
              onChange={(event) =>
                setMaxTime(Number(event.target.value))
              }
            />
          </div>

          {error && (
            <div className="error-message">
              <AlertCircle size={20} />
              <span>{error}</span>
            </div>
          )}

          <button
            type="button"
            onClick={handleGenerateRecipe}
            disabled={loading}
          >
            {loading ? (
  <>
    <span className="loading-spinner"></span>
    Criando sua receita...
  </>
) : (
              <>
                <Sparkles size={20} />
                Gerar minha receita
              </>
            )}
          </button>
        </section>

        {recipe && (
          <section className="recipe-result">
            <div className="recipe-header">
              <div>
                <span className="recipe-label">
                  SUA RECEITA
                </span>

                <h2>{recipe.nome}</h2>
              </div>

              <div className="recipe-info">
                <span>
                  <Clock size={16} />
                  {recipe.tempo_preparo} min
                </span>

                <span>
                  {recipe.dificuldade}
                </span>
              </div>
            </div>

            <div className="recipe-content">
              <div>
                <h3>Ingredientes</h3>

                <ul>
                  {recipe.ingredientes.map(
                    (ingredient, index) => (
                      <li key={index}>{ingredient}</li>
                    )
                  )}
                </ul>
              </div>

              <div>
                <h3>Modo de preparo</h3>

                <ol>
                  {recipe.modo_preparo.map(
                    (step, index) => (
                      <li key={index}>{step}</li>
                    )
                  )}
                </ol>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;