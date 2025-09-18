# 📚 Smart Digital Library

Smart Digital Library é uma plataforma web em Django que moderniza a gestão de livros por instituições e leitores com catálogo interativo, listas e coleções temáticas, recomendações por inteligência artificial e painel administrativo.

---

## 🚀 Funcionalidades
- 🔍 Catálogo de livros com busca e filtros
- 🤖 Recomendação personalizada baseada em IA
- 📑 Criação de listas temáticas e coleções acuradas de leitura
- 👤 Autenticação e perfis de usuários
- 📊 Dashboard administrativo (admin Django)
- 📱 Frontend responsivo com HTML, CSS

---

## 🏗️ Arquitetura
- **Backend**: Django
- **Frontend**: Templates Django + HTML + CSS
- **Banco de Dados**: SQLite em dev
- **IA**: Algoritmos de recomendação

---

## 📂 Estrutura do Projeto
```bash
smart-digital-library/
│── smart-digital-library/ # Configurações principais do projeto
│── virtuallibrary/                  # Módulos (catálogo, usuários, recomendação, listas)
│── static/                # Arquivos CSS, JS e imagens
│── templates/             # Templates HTML globais
│── media/                 # Uploads de usuários
│── manage.py
