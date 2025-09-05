# 📚 Smart Digital Library

Smart Digital Library é uma plataforma web em Django que moderniza a gestão de livros por instituições e leitores com catálogo interativo, listas e coleções temáticas, recomendações por inteligência artificial e painel administrativo.

---

## 🚀 Funcionalidades
- 🔍 Catálogo de livros com busca e filtros
- 🤖 Recomendação personalizada baseada em IA
- 📑 Criação de listas temáticas e coleções acuradas de leitura
- 👤 Autenticação e perfis de usuários
- 📊 Dashboard administrativo (admin Django)
- 📱 Frontend responsivo com HTML, CSS e JavaScript

---

## 🏗️ Arquitetura
- **Backend**: Django + Django REST Framework (para APIs)
- **Frontend**: Templates Django + JS + HTML + CSS
- **Banco de Dados**: SQLite em dev
- **IA**: Algoritmos de recomendação

![Arquitetura](docs/arquitetura.png)

---

## 📂 Estrutura do Projeto
```bash
smart-digital-library/
│── smart-digital-library/ # Configurações principais do projeto
│── apps/                  # Módulos (catálogo, usuários, recomendação, listas)
│── static/                # Arquivos CSS, JS e imagens
│── templates/             # Templates HTML globais
│── media/                 # Uploads de usuários
│── docs/                  # Documentação (diagramas, requisitos, etc.)
│── manage.py
