# 🍳 SaborIA

API Web de geração de receitas utilizando Inteligência Artificial.

O SaborIA recebe os ingredientes disponíveis pelo usuário, além do tipo de refeição, nível de dificuldade e tempo máximo de preparo. A partir dessas informações, a aplicação utiliza a API do Google Gemini para gerar uma receita personalizada.

---

## 🎯 Objetivo

O projeto foi desenvolvido para demonstrar a integração entre uma API Web e um serviço de Inteligência Artificial generativa.

A proposta é solucionar um problema simples do dia a dia:

> "Tenho alguns ingredientes disponíveis. O que posso preparar com eles?"

O SaborIA transforma essas informações em uma sugestão de receita utilizando Inteligência Artificial.

---

## 🤖 Categoria do projeto

**Generation / Geração de conteúdo com Inteligência Artificial**

A aplicação utiliza IA generativa para criar receitas a partir dos dados fornecidos pelo usuário.

---

## 🏗️ Arquitetura

O projeto utiliza uma arquitetura simples, separando a API da comunicação com o provedor de Inteligência Artificial.

```text
Usuário
   │
   ▼
Frontend / Swagger
   │
   ▼
FastAPI
   │
   ├── Validação dos dados
   │
   ├── Regras de negócio
   │
   ▼
Gemini Service
   │
   ▼
Google Gemini API
   │
   ▼
Receita gerada
   │
   ▼
Resposta da API
